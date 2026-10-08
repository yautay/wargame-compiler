"""M8: job store (glu.store) and the state machines of Job and Build (glu.states, GLU §3, ADR-0023)."""
from __future__ import annotations

import sqlite3
from collections import Counter, deque
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

from glu import states, store as store_mod
from glu.states import BUILD_RULES, JOB_RULES, IllegalTransition
from glu.store import SCHEMA_VERSION, Store, StoreError, db_path
from wgc import contracts

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "contracts" / "fixtures" / "valid" / "glu.job.yaml"

CACHE_KEY = {"task": "logic.rule.extract", "task_version": "0", "output_schema": "wgc/logic@0#rule",
             "input_hash": "sha256:" + "0" * 16, "context_hash": "sha256:" + "1" * 16}
ALLOW_FALLBACK = {"fallback": {"self_hosted_unavailable": "queue", "allow_premium_fallback": True}}


class Ids:
    """Deterministic IDs: build_000001, job_000001, att_000001, …"""

    def __init__(self, scripted: dict[str, list[str]] | None = None):
        self.n = Counter()
        self.scripted = {k: deque(v) for k, v in (scripted or {}).items()}

    def __call__(self, prefix: str) -> str:
        if self.scripted.get(prefix):
            return self.scripted[prefix].popleft()
        self.n[prefix] += 1
        return f"{prefix}_{self.n[prefix]:06d}"


class Clock:
    """Fixed clock; `now` can be moved by the test."""

    def __init__(self, start: str = "2026-10-05T10:00:00Z"):
        self.now = datetime.fromisoformat(start.replace("Z", "+00:00"))

    def __call__(self) -> datetime:
        return self.now


def open_store(root: Path, **kwargs) -> Store:
    kwargs.setdefault("clock", Clock())
    kwargs.setdefault("new_id", Ids())
    return Store.at_root(root, **kwargs)


def shortest_paths(kind: str) -> dict[str, list[states.Rule]]:
    """state → shortest list of rules from the initial state (BFS over the transition table)."""
    initial = states.JOB_INITIAL if kind == "job" else states.BUILD_INITIAL
    rules = JOB_RULES if kind == "job" else BUILD_RULES
    paths = {initial: []}
    queue = deque([initial])
    while queue:
        src = queue.popleft()
        for rule in rules:
            if rule.src == src and rule.dst not in paths:
                paths[rule.dst] = paths[src] + [rule]
                queue.append(rule.dst)
    return paths


JOB_PATHS = shortest_paths("job")
BUILD_PATHS = shortest_paths("build")


def job_params(rule: states.Rule) -> dict:
    """Parameters that satisfy the rule's guard (jobs start at tier `local`)."""
    return {"tier": "premium"} if rule.guard == "tier_raised" else {}


def new_job(s: Store, *, policy: dict | None = ALLOW_FALLBACK, tier: str = "local") -> str:
    build = s.create_build("bench-minigame", "stage1", scope="chapter:5", policy=policy)
    return s.create_job(build, "logic.rule.extract", ["SEG-mg.3.1"], CACHE_KEY, tier=tier)


def drive_job(s: Store, state: str, **kwargs) -> str:
    job = new_job(s, **kwargs)
    for rule in JOB_PATHS[state]:
        s.transition_job(job, rule.dst, **job_params(rule))
    assert s.job(job)["state"] == state
    return job


def drive_build(s: Store, state: str) -> str:
    build = s.create_build("bench-minigame", "stage1")
    for rule in BUILD_PATHS[state]:
        s.transition_build(build, rule.dst)
    assert s.build(build)["state"] == state
    return build


# --- the tables themselves -----------------------------------------------------------------------------------

def _enum(kind: str, field: str) -> list:
    return contracts.schema_for("glu/exec@0")["$defs"][kind]["properties"][field]["enum"]


def test_states_match_contract():
    assert list(states.JOB_STATES) == _enum("job", "state")
    assert list(states.BUILD_STATES) == _enum("build", "state")
    assert list(states.TIERS) == contracts.schema_for("glu/exec@0")["$defs"]["tier"]["enum"]


@pytest.mark.parametrize("kind", ["job", "build"])
def test_table_is_well_formed(kind):
    all_states, rules, _ = states.MACHINES[kind]
    terminal = states.JOB_TERMINAL if kind == "job" else states.BUILD_TERMINAL
    pairs = [(r.src, r.dst) for r in rules]
    assert len(pairs) == len(set(pairs)), "duplicate rule"
    assert {s for p in pairs for s in p} <= set(all_states)
    assert not [r for r in rules if r.src in terminal], "terminal states have no outgoing transitions"
    assert set(shortest_paths(kind)) == set(all_states), "every state reachable from the initial one"
    assert all(r.guard is None or r.guard in states.GUARDS for r in rules)
    assert all(r.effect is None or r.effect in states.EFFECTS for r in rules)
    assert all(p in states.PARAM_FIELDS for r in rules for p in r.params)


def test_waiting_inference_round_trip_and_cancel_from_every_active_state():
    index = states.rule_index(JOB_RULES)
    assert ("running", "waiting_inference") in index and ("waiting_inference", "running") in index
    assert ("stale", "pending") in index and ("done", "stale") in index and ("accepted", "stale") in index
    active = set(states.JOB_STATES) - states.JOB_TERMINAL - {"accepted", "done", "stale"}
    assert {s for s, d in index if d == "cancelled"} == active


# --- every legal transition ----------------------------------------------------------------------------------

@pytest.mark.parametrize("rule", JOB_RULES, ids=lambda r: f"{r.src}->{r.dst}")
def test_job_legal_transition(tmp_path, rule):
    with open_store(tmp_path) as s:
        job = drive_job(s, rule.src)
        new = s.transition_job(job, rule.dst, reason="test", **job_params(rule))
        assert new["state"] == rule.dst
        assert s.job(job) == new
        assert s.history(job)[-1] == {"src": rule.src, "dst": rule.dst, "at": "2026-10-05T10:00:00Z",
                                      "reason": "test"}


@pytest.mark.parametrize("rule", BUILD_RULES, ids=lambda r: f"{r.src}->{r.dst}")
def test_build_legal_transition(tmp_path, rule):
    with open_store(tmp_path) as s:
        build = drive_build(s, rule.src)
        new = s.transition_build(build, rule.dst)
        assert new["state"] == rule.dst
        assert ("finished_at" in new) == (rule.dst in states.BUILD_TERMINAL)
        assert s.history(build)[-1]["dst"] == rule.dst


# --- every illegal transition --------------------------------------------------------------------------------

@pytest.mark.parametrize("src", states.JOB_STATES)
def test_job_illegal_transitions(tmp_path, src):
    index = states.rule_index(JOB_RULES)
    with open_store(tmp_path) as s:
        job = drive_job(s, src)
        before = (s.job(job), s.history(job))
        illegal = [dst for dst in states.JOB_STATES if (src, dst) not in index]
        assert illegal
        for dst in illegal:
            with pytest.raises(IllegalTransition, match=f"niedozwolone przejście joba {job}: {src} → {dst}"):
                s.transition_job(job, dst)
            assert (s.job(job), s.history(job)) == before


@pytest.mark.parametrize("src", states.BUILD_STATES)
def test_build_illegal_transitions(tmp_path, src):
    index = states.rule_index(BUILD_RULES)
    with open_store(tmp_path) as s:
        build = drive_build(s, src)
        before = s.build(build)
        for dst in [d for d in states.BUILD_STATES if (src, d) not in index]:
            with pytest.raises(IllegalTransition, match=f"niedozwolone przejście buildu {build}: {src} → {dst}"):
                s.transition_build(build, dst)
            assert s.build(build) == before


def test_unknown_state_and_unexpected_parameter(tmp_path):
    with open_store(tmp_path) as s:
        job = drive_job(s, "ready")
        with pytest.raises(IllegalTransition, match="nieznany stan joba: 'launched'"):
            s.transition_job(job, "launched")
        with pytest.raises(IllegalTransition, match="nie przyjmuje parametrów: tier"):
            s.transition_job(job, "running", tier="premium")
        with pytest.raises(IllegalTransition, match="nie przyjmuje parametrów: accepted_records"):
            s.transition_job(job, "running", accepted_records=["R-3.1"])
        assert s.job(job)["state"] == "ready"


# --- guards and effects --------------------------------------------------------------------------------------

def test_cache_hit_goes_from_ready_to_accepted_without_attempts(tmp_path):
    with open_store(tmp_path) as s:
        job = drive_job(s, "ready")
        new = s.transition_job(job, "accepted", accepted_records=["R-3.1"])
        assert new["cache_hit"] is True and new["accepted_records"] == ["R-3.1"]
        assert "attempts" not in new and s.quality_attempts(job) == 0


def test_dispatch_marks_cache_miss(tmp_path):
    with open_store(tmp_path) as s:
        job = drive_job(s, "running")
        assert s.job(job)["cache_hit"] is False


def test_premium_fallback_needs_explicit_policy(tmp_path):
    with open_store(tmp_path) as s:
        job = drive_job(s, "waiting_inference", policy=None)
        with pytest.raises(IllegalTransition, match="allow_premium_fallback: false"):
            s.transition_job(job, "escalated")
        assert s.job(job)["state"] == "waiting_inference"
        allowed = drive_job(s, "waiting_inference", policy=ALLOW_FALLBACK)
        assert s.transition_job(allowed, "escalated")["state"] == "escalated"


def test_escalation_must_raise_the_tier(tmp_path):
    with open_store(tmp_path) as s:
        job = drive_job(s, "escalated")
        with pytest.raises(IllegalTransition, match="wymagany parametr tier"):
            s.transition_job(job, "ready")
        with pytest.raises(IllegalTransition, match="eskalacja musi podnieść tier: local → local"):
            s.transition_job(job, "ready", tier="local")
        with pytest.raises(IllegalTransition, match="local → deterministic"):
            s.transition_job(job, "ready", tier="deterministic")
        assert s.transition_job(job, "ready", tier="premium")["tier"] == "premium"
        assert s.job(job)["tier"] == "premium"


def test_waiting_inference_does_not_consume_quality_attempts(tmp_path):
    with open_store(tmp_path) as s:
        job = drive_job(s, "running")
        s.add_attempt(job, "local", "unavailable", error_class="network", endpoint="ai-node", wall_seconds=3)
        s.transition_job(job, "waiting_inference")
        s.transition_job(job, "running")
        s.add_attempt(job, "local", "unavailable", error_class="model_loading", endpoint="ai-node")
        assert s.quality_attempts(job) == 0
        s.add_attempt(job, "local", "retry", schema_valid=False, error_class="bad_output")
        s.add_attempt(job, "local", "escalate", schema_valid=True, domain_valid=True)
        s.add_attempt(job, "premium", "accepted", cost_usd=0.04)
        assert s.quality_attempts(job) == 3
        assert s.quality_attempts(job, "local") == 2 and s.quality_attempts(job, "premium") == 1
        assert len(s.job(job)["attempts"]) == 5


def test_build_finish_records_time_and_metrics(tmp_path):
    clock = Clock()
    with open_store(tmp_path, clock=clock) as s:
        build = drive_build(s, "running")
        clock.now += timedelta(minutes=4)
        done = s.transition_build(build, "done", metrics={"jobs_total": 3, "cache_hits": 0})
        assert done["started_at"] == "2026-10-05T10:00:00Z" and done["finished_at"] == "2026-10-05T10:04:00Z"
        assert done["metrics"] == {"jobs_total": 3, "cache_hits": 0}
        with pytest.raises(IllegalTransition, match="nie przyjmuje parametrów: metrics"):
            s.transition_build(drive_build(s, "planning"), "running", metrics={"x": 1})


# --- store-level checks --------------------------------------------------------------------------------------

def test_records_are_validated_before_write(tmp_path):
    with open_store(tmp_path) as s:
        job = drive_job(s, "running")
        with pytest.raises(StoreError, match="niezgodny z glu/exec@0"):
            s.add_routing_decision(job, "routing@0", "premium", {"risk_class": "high"}, ["test"])
        assert s.routing_decisions(job) == []
        with pytest.raises(StoreError, match="niezgodny z glu/exec@0"):
            s.add_attempt(job, "local", "unavailable", error_class="dns")
        assert s.attempts(job) == []
        with pytest.raises(StoreError, match="kind"):
            s.add_attempt(job, "local", "accepted", kind="job")
        with pytest.raises(StoreError, match="niezgodny z glu/exec@0"):
            s.create_job(s.job(job)["build"], "t", ["not-an-id"], CACHE_KEY)


def test_dependencies_closed_builds_and_unknown_ids(tmp_path):
    with open_store(tmp_path) as s:
        build = s.create_build("bench-minigame", "stage1")
        other = s.create_build("bench-minigame", "stage1")
        first = s.create_job(build, "a.task", ["SEG-mg.1"], CACHE_KEY)
        second = s.create_job(build, "b.task", ["SEG-mg.2"], CACHE_KEY, depends_on=[first])
        assert s.job(second)["depends_on"] == [first]
        with pytest.raises(StoreError, match=f"zależność {first} nie jest jobem buildu {other}"):
            s.create_job(other, "c.task", ["SEG-mg.3"], CACHE_KEY, depends_on=[first])
        s.transition_build(other, "cancelled")
        with pytest.raises(StoreError, match="jest zakończony"):
            s.create_job(other, "c.task", ["SEG-mg.3"], CACHE_KEY)
        with pytest.raises(StoreError, match="nie ma joba job_999999"):
            s.transition_job("job_999999", "ready")
        with pytest.raises(StoreError, match="nie ma buildu build_999999"):
            s.build("build_999999")
        s.transition_job(first, "cancelled")
        with pytest.raises(StoreError, match="nie można dodać próby"):
            s.add_attempt(first, "local", "error")


def test_default_ids_and_timestamps():
    ids = {store_mod.new_id("job") for _ in range(500)}
    assert len(ids) == 500
    pattern = contracts.schema_for("glu/exec@0")["$defs"]["xid"]["pattern"]
    import re
    assert all(re.match(pattern, i) and len(i) == 4 + 26 for i in ids)
    assert store_mod.timestamp(datetime(2026, 10, 5, 12, 0, tzinfo=timezone(timedelta(hours=2)))) \
        == "2026-10-05T10:00:00Z"
    with pytest.raises(StoreError, match="bez strefy"):
        store_mod.timestamp(datetime(2026, 10, 5))


# --- persistence and migrations ------------------------------------------------------------------------------

def _schema_objects(path: Path) -> list:
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT type, name, sql FROM sqlite_master ORDER BY name").fetchall()
    finally:
        conn.close()


def test_migration_from_empty_and_reopen_without_changes(tmp_path):
    with open_store(tmp_path) as s:
        assert s.applied_migrations == SCHEMA_VERSION and s.schema_version == SCHEMA_VERSION
    path = db_path(tmp_path)
    objects = _schema_objects(path)
    assert {name for kind, name, _ in objects if kind == "table"} >= {"build", "job", "attempt",
                                                                       "routing_decision", "transition"}
    with open_store(tmp_path) as s:
        assert s.applied_migrations == 0 and s.schema_version == SCHEMA_VERSION
    assert _schema_objects(path) == objects


def test_state_survives_restart(tmp_path):
    with open_store(tmp_path, new_id=Ids()) as s:
        job = drive_job(s, "validating")
        s.add_attempt(job, "local", "retry", validation_errors=["L1 unresolved_ref R-9"])
        s.add_routing_decision(job, "routing@0", "local", {"risk_class": "low"}, ["low risk"])
        s.transition_job(job, "retry")
        before = (s.export(), s.history(job))
    with open_store(tmp_path) as s:
        assert (s.export(), s.history(job)) == before
        assert s.transition_job(job, "ready")["state"] == "ready"
        assert s.quality_attempts(job) == 1


def test_newer_database_is_refused_and_file_released(tmp_path):
    open_store(tmp_path).close()
    path = db_path(tmp_path)
    conn = sqlite3.connect(path)
    conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION + 1}")
    conn.close()
    with pytest.raises(StoreError, match=f"wersję schematu {SCHEMA_VERSION + 1}"):
        open_store(tmp_path)
    path.unlink()  # on Windows this fails if the store left the connection open


def test_not_a_database_is_refused_and_file_released(tmp_path):
    path = db_path(tmp_path)
    path.parent.mkdir()
    path.write_bytes(b"not a sqlite file at all, just bytes" * 10)
    with pytest.raises(StoreError, match="nie jest poprawną bazą stanu GLU"):
        open_store(tmp_path)
    path.unlink()


def test_failed_migration_rolls_back(tmp_path, monkeypatch):
    broken = (("CREATE TABLE build (id TEXT PRIMARY KEY)", "CREATE TABLE broken (syntax error here"),)
    monkeypatch.setattr(store_mod, "MIGRATIONS", broken)
    monkeypatch.setattr(store_mod, "SCHEMA_VERSION", 1)
    with pytest.raises(StoreError, match="migracja bazy stanu GLU do wersji 1 nie powiodła się"):
        open_store(tmp_path)
    assert _schema_objects(db_path(tmp_path)) == []
    conn = sqlite3.connect(db_path(tmp_path))
    try:
        assert conn.execute("PRAGMA user_version").fetchone()[0] == 0
    finally:
        conn.close()


def test_open_existing_only_does_not_create(tmp_path):
    with pytest.raises(StoreError, match="brak bazy stanu GLU"):
        Store.at_root(tmp_path, create=False)
    assert not (tmp_path / ".glu").exists()


# --- export --------------------------------------------------------------------------------------------------

def test_export_reproduces_contract_fixture(tmp_path):
    """The store, driven through the GLU §3 life cycle, exports exactly the records of the glu/exec@0 fixture."""
    fixture = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
    by_kind = {r["kind"]: r for r in fixture["records"]}
    fb, fj, rd = by_kind["build"], by_kind["job"], by_kind["routing_decision"]
    attempts = {r["id"]: {k: v for k, v in r.items() if k not in ("kind", "id", "job")}
                for r in fixture["records"] if r["kind"] == "attempt"}
    ids = Ids({"build": [fb["id"]], "job": [fj["id"]], "att": sorted(attempts), "rd": [rd["id"]]})
    clock = Clock(fb["started_at"])

    def attempt(job, att_id):
        fields = dict(attempts[att_id])
        s.add_attempt(job, fields.pop("tier"), fields.pop("outcome"), **fields)

    with open_store(tmp_path, clock=clock, new_id=ids) as s:
        build = s.create_build(fb["project"], fb["target"]["stage"], scope=fb["target"]["scope"],
                               policy=fb["policy"], project_rev=fb["project_rev"],
                               inference_snapshot=fb["inference_snapshot"])
        s.transition_build(build, "running")
        job = s.create_job(build, fj["task"], fj["inputs"], fj["cache_key"], tier="local",
                           risk_class=fj["risk_class"])
        for dst in ("ready", "running"):
            s.transition_job(job, dst)
        attempt(job, "att_000000")                       # node unreachable: no quality retry consumed
        s.transition_job(job, "waiting_inference")
        s.transition_job(job, "running")
        attempt(job, "att_000001")                       # local run, forced rule → escalate
        for dst in ("proposed", "validating", "escalated"):
            s.transition_job(job, dst)
        s.add_routing_decision(job, rd["policy"], rd["chosen"], rd["signals"], rd["reasons"],
                               premium_reason=rd["premium_reason"])
        s.transition_job(job, "ready", tier="premium")
        s.transition_job(job, "running")
        attempt(job, "att_000002")
        for dst in ("proposed", "validating"):
            s.transition_job(job, dst)
        s.transition_job(job, "accepted", accepted_records=fj["accepted_records"])
        s.transition_job(job, "done")
        clock.now = datetime.fromisoformat(fb["finished_at"].replace("Z", "+00:00"))
        s.transition_build(build, "done", metrics=fb["metrics"])
        doc = s.export()
        assert s.quality_attempts(job) == 2

    assert contracts.errors(doc) == []
    assert {r["id"]: r for r in doc["records"]} == {r["id"]: r for r in fixture["records"]}
    assert [r["kind"] for r in doc["records"]] == ["build", "job", "attempt", "attempt", "attempt",
                                                   "routing_decision"]


def test_export_filters_by_build_and_orders_fields(tmp_path):
    with open_store(tmp_path) as s:
        first = drive_job(s, "running")
        drive_job(s, "ready")
        build = s.job(first)["build"]
        doc = s.export(build)
        assert [r["kind"] for r in doc["records"]] == ["build", "job"]
        assert list(doc["records"][1])[:4] == ["kind", "id", "build", "task"]
        assert len(s.export()["records"]) == 4

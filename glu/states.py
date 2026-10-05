"""State machines of Job and Build (GLU §3, ADR-0023).

Transitions are data: a table of `Rule`s. A rule may name a guard (a condition checked on the record, its build
and the transition parameters), an effect (a change of the record made by the transition) and the parameters
it accepts. `step()` is the only interpreter of the tables; the store never decides legality on its own.
Pure functions over record dicts: no database, no clock (the caller passes `now`).
"""
from __future__ import annotations

from typing import Callable, NamedTuple

# Enum order from glu/exec@0 (`#/$defs/job/properties/state`, `#/$defs/build/properties/state`).
JOB_STATES = ("pending", "ready", "running", "waiting_inference", "proposed", "validating", "accepted", "rejected",
              "retry", "escalated", "waiting_review", "waiting_human", "done", "failed", "cancelled", "stale")
BUILD_STATES = ("planning", "running", "waiting_inference", "waiting_review", "waiting_human", "done", "failed",
                "cancelled")
# Escalation order of executors (glu/exec@0 `#/$defs/tier`).
TIERS = ("deterministic", "local", "premium", "human")

JOB_INITIAL = "pending"
BUILD_INITIAL = "planning"
JOB_TERMINAL = frozenset({"rejected", "failed", "cancelled"})
BUILD_TERMINAL = frozenset({"done", "failed", "cancelled"})


class Rule(NamedTuple):
    src: str
    dst: str
    guard: str | None = None
    effect: str | None = None
    params: frozenset = frozenset()


class IllegalTransition(ValueError):
    """A transition outside the table, or one whose guard or parameters do not hold."""


_JOB_CANCELLABLE = ("pending", "ready", "running", "waiting_inference", "proposed", "validating", "retry",
                    "escalated", "waiting_review", "waiting_human")

JOB_RULES: tuple[Rule, ...] = (
    Rule("pending", "ready"),
    Rule("ready", "running", effect="cache_miss"),
    # cache hit: accepted without any executor call (GLU §3)
    Rule("ready", "accepted", effect="cache_hit", params=frozenset({"accepted_records"})),
    # availability error of the provider: no quality attempt consumed (ADR-0017)
    Rule("running", "waiting_inference"),
    Rule("running", "proposed"),
    Rule("running", "failed"),
    Rule("waiting_inference", "running"),
    # premium fallback only when the build policy allows it explicitly (ADR-0017)
    Rule("waiting_inference", "escalated", guard="premium_fallback_allowed"),
    Rule("waiting_inference", "failed"),
    Rule("proposed", "validating"),
    Rule("validating", "accepted", params=frozenset({"accepted_records"})),
    Rule("validating", "retry"),
    Rule("validating", "escalated"),
    Rule("validating", "waiting_review"),
    Rule("validating", "waiting_human"),
    Rule("validating", "rejected"),
    Rule("validating", "failed"),
    Rule("retry", "ready"),
    Rule("escalated", "ready", guard="tier_raised", params=frozenset({"tier"})),
    Rule("waiting_review", "validating"),
    Rule("waiting_human", "validating"),
    Rule("accepted", "done"),
    Rule("accepted", "stale"),
    Rule("done", "stale"),
    Rule("stale", "pending"),
    *(Rule(s, "cancelled") for s in _JOB_CANCELLABLE),
)

BUILD_RULES: tuple[Rule, ...] = (
    Rule("planning", "running"),
    *(Rule(s, "running") for s in ("waiting_inference", "waiting_review", "waiting_human")),
    *(Rule("running", s) for s in ("waiting_inference", "waiting_review", "waiting_human")),
    Rule("running", "done", effect="finish", params=frozenset({"metrics"})),
    *(Rule(s, dst, effect="finish", params=frozenset({"metrics"}))
      for s in ("planning", "running", "waiting_inference", "waiting_review", "waiting_human")
      for dst in ("failed", "cancelled")),
)


def _tier_raised(record: dict, build: dict | None, params: dict) -> str | None:
    tier = params.get("tier")
    if tier not in TIERS:
        return f"wymagany parametr tier ({', '.join(TIERS)}), otrzymano {tier!r}"
    current = record.get("tier")
    if current in TIERS and TIERS.index(tier) <= TIERS.index(current):
        return f"eskalacja musi podnieść tier: {current} → {tier}"
    return None


def _premium_fallback_allowed(record: dict, build: dict | None, params: dict) -> str | None:
    fallback = ((build or {}).get("policy") or {}).get("fallback") or {}
    if not fallback.get("allow_premium_fallback", False):
        return ("polityka buildu nie pozwala na premium przy niedostępnym węźle "
                "(policy.fallback.allow_premium_fallback: false, ADR-0017)")
    return None


GUARDS: dict[str, Callable[[dict, dict | None, dict], str | None]] = {
    "tier_raised": _tier_raised,
    "premium_fallback_allowed": _premium_fallback_allowed,
}


def _set(field: str, value: Callable[[dict, str], object]) -> Callable[[dict, dict, str], None]:
    def effect(record: dict, params: dict, now: str) -> None:
        record[field] = value(params, now)
    return effect


EFFECTS: dict[str, Callable[[dict, dict, str], None]] = {
    "cache_hit": _set("cache_hit", lambda params, now: True),
    "cache_miss": _set("cache_hit", lambda params, now: False),
    "finish": _set("finished_at", lambda params, now: now),
}

# Parameters copied onto the record when the rule accepts them.
PARAM_FIELDS = {"tier": "tier", "accepted_records": "accepted_records", "metrics": "metrics"}

MACHINES = {
    "job": (JOB_STATES, JOB_RULES, "joba"),
    "build": (BUILD_STATES, BUILD_RULES, "buildu"),
}


def rule_index(rules: tuple[Rule, ...]) -> dict[tuple[str, str], Rule]:
    return {(r.src, r.dst): r for r in rules}


_INDEX = {kind: rule_index(rules) for kind, (_, rules, _) in MACHINES.items()}


def allowed(kind: str, src: str) -> list[str]:
    """States reachable from `src` in one step."""
    return [dst for (s, dst) in _INDEX[kind] if s == src]


def step(kind: str, record: dict, dst: str, params: dict | None = None, *, build: dict | None = None,
         now: str) -> dict:
    """Return a copy of `record` moved to `dst`, or raise IllegalTransition (message in Polish)."""
    states, _, noun = MACHINES[kind]
    params = {k: v for k, v in (params or {}).items() if v is not None}
    src = record["state"]
    what = f"{noun} {record['id']}"
    if dst not in states:
        raise IllegalTransition(f"nieznany stan {noun}: {dst!r} (znane: {', '.join(states)})")
    rule = _INDEX[kind].get((src, dst))
    if rule is None:
        options = ", ".join(allowed(kind, src)) or "brak, stan końcowy"
        raise IllegalTransition(f"niedozwolone przejście {what}: {src} → {dst} (dozwolone: {options})")
    extra = sorted(set(params) - rule.params)
    if extra:
        raise IllegalTransition(f"przejście {what} {src} → {dst} nie przyjmuje parametrów: {', '.join(extra)}")
    if rule.guard:
        problem = GUARDS[rule.guard](record, build, params)
        if problem:
            raise IllegalTransition(f"przejście {what} {src} → {dst} odrzucone: {problem}")
    out = dict(record)
    out["state"] = dst
    for name, value in params.items():
        out[PARAM_FIELDS[name]] = value
    if rule.effect:
        EFFECTS[rule.effect](out, params, now)
    return out

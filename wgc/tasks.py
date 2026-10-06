"""Task specifications: the contract WGC → GLU (docs/ARCHITECTURE.md §2, ADR-0025).

A `TaskSpec` says what a task reads, what a correct output looks like and how to compute it deterministically
(Tier 0). GLU plans jobs from the registry (`REGISTRY`, `for_stage`), runs them and hands every output to
`wgc.kb.accept`, the only path into `kb/`. `wgc` never imports `glu` (ADR-0002): GLU imports this module.

A task output is a list of **proposals** (docs/DATA-CONTRACTS.md §10):
`{record: <record without prov, status, risk>, anchors: [{seg, quote?, span?}], derived_from: [ids]}`.
Provenance, status, `inputs_hash` and `manifest` are added by `wgc.kb.accept` (ADR-0014). What a job reads (inputs,
authority data of source documents, `kb/` context) is defined once, by `wgc.manifest.build` from the fields below
(ADR-0033): the planner keys the job with it and `accept()` records it.

Scopes of a build (`--scope`): `all`, `chapter:<N>` (segments under the heading labelled `N` or `N.0`, by
`parent`), `segment:<SEG-id>`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from wgc.kb import Workspace

Inputs = tuple[str, ...]  # input ids of one job (SEG-… in Stage 1 Tier 0 tasks)


class TaskError(ValueError):
    """Wrong task, stage or scope (message in Polish)."""


@dataclass(frozen=True)
class TaskSpec:
    """One task of the pipeline. Fields marked M10 are optional until the structured-output loop exists."""
    id: str                       # e.g. "wgc.tables.parse"
    version: str                  # task version; with `id` it is the tool name `id@version` in `prov.by`
    stage: str                    # build stage, e.g. "stage1"
    output_kind: str              # record kind of the proposals, e.g. "table"
    output_schema: str            # contract and definition of the proposal record, e.g. "wgc/logic@0#table"
    # Which jobs a build over the given segments needs: one tuple of input ids per job.
    input_selector: Callable[["Workspace", list[str]], list[Inputs]]
    # Domain checks of the proposals beyond the schema and the KB validator: Polish messages, empty = valid.
    validate: Callable[["Workspace", Inputs, list[dict]], list[str]]
    # Tier 0 implementation: inputs → proposals. None for model-only tasks.
    deterministic_impl: Callable[["Workspace", Inputs], list[dict]] | None = None
    # What of one input affects the result (its entry in the job manifest); default: its `logic` projection.
    semantic_projection: Callable[["Workspace", str], dict] | None = None
    # Source documents whose authority data (role, seg_prefix, precedence) the task reads besides those of its input
    # segments, e.g. every `rules` document when it picks the main rules (ADR-0033).
    authority_selector: Callable[["Workspace", Inputs], list[str]] | None = None
    # Records of `kb/` the task reads as context (ids). A task with it reads `kb/`: its manifest is checked against
    # `kb/` at acceptance (ADR-0033). `context_builder` (M10) may read only these records.
    context_selector: Callable[["Workspace", Inputs], list[str]] | None = None
    # Risk features of a proposal (`wgc/risk@0`, M6); none until then.
    risk_features: Callable[[dict], list[dict]] = lambda proposal: []
    # M10: context for the model, prompt id@version and the flat decoding schema for the node.
    context_builder: Callable[["Workspace", Inputs], list[dict]] | None = None
    prompt: str | None = None
    decoding_schema: dict | None = None

    @property
    def name(self) -> str:
        """Tool or task name with version, as recorded in `prov.by.tool` and in the cache key."""
        return f"{self.id}@{self.version}"


def _registry() -> dict[str, TaskSpec]:
    from wgc import tables, terms
    specs = [tables.PARSE, terms.HARVEST]
    return {s.id: s for s in specs}


REGISTRY: dict[str, TaskSpec] = {}


def registry() -> dict[str, TaskSpec]:
    if not REGISTRY:
        REGISTRY.update(_registry())
    return REGISTRY


def get(task_id: str) -> TaskSpec:
    try:
        return registry()[task_id]
    except KeyError:
        raise TaskError(f"Nieznane zadanie `{task_id}`.") from None


def stage_name(stage: str) -> str:
    """`1`, `stage1` → `stage1`."""
    return stage if stage.startswith("stage") else f"stage{stage}"


def for_stage(stage: str) -> list[TaskSpec]:
    """Tasks of a stage in registry order; an unknown stage is an error."""
    name = stage_name(stage)
    specs = [s for s in registry().values() if s.stage == name]
    if not specs:
        known = ", ".join(sorted({s.stage for s in registry().values()}))
        raise TaskError(f"Brak zadań dla etapu `{stage}` (etapy z zadaniami: {known}).")
    return specs


# --- scope --------------------------------------------------------------------------------------------------------

def select(ws: "Workspace", scope: str | None) -> list[str]:
    """Segment ids of present documents in `scope`, in inventory order."""
    segments = [s for s in ws.inventory.segments if (ws.document(s["doc"]) or {}).get("present")]
    scope = scope or "all"
    if scope == "all":
        return [s["id"] for s in segments]
    kind, sep, value = scope.partition(":")
    if not sep or not value or kind not in ("chapter", "segment"):
        raise TaskError(f"Niepoprawny zakres `{scope}`: oczekiwano `all`, `chapter:<N>` albo `segment:<SEG-id>`.")
    if kind == "segment":
        if not any(s["id"] == value for s in segments):
            raise TaskError(f"Zakres `{scope}`: segmentu `{value}` nie ma w inwentarzu (wśród obecnych dokumentów).")
        return [value]
    heads = {s["id"] for s in segments if s.get("segment_type") == "heading" and s.get("label") in (value, f"{value}.0")}
    if not heads:
        raise TaskError(f"Zakres `{scope}`: brak nagłówka rozdziału `{value}` (etykieta `{value}` albo `{value}.0`).")
    parents = {s["id"]: s.get("parent") for s in segments}

    def under(sid: str) -> bool:
        seen = set()
        while sid is not None and sid not in seen:
            if sid in heads:
                return True
            seen.add(sid)
            sid = parents.get(sid)
        return False

    return [s["id"] for s in segments if under(s["id"])]

"""Receipt diagnostics: the `kb_receipt` of one job against the current `kb/` (`glu receipt`, ADR-0033).

Read only, by decision of the owner (2026-10-06): the job store is opened with `mode=ro` and never migrated, `kb/`
is compared by `wgc.kb.compare_receipt` (no recovery, no lock file created), nothing is reconciled and no receipt is
removed. The receipt is the `kb_receipt` of the job's accepted Attempt; a job still `validating` with a receipt in
`.glu/kb-receipts/` (an undecided acceptance, ADR-0031) has that one compared instead.

A difference from a historical receipt is not damage by itself: a later correct `accept()` (another job, a human
decision) changes the record too. For each differing record the report gives its current `prov.job` and whether
that job is later than the one asked about.
"""
from __future__ import annotations

from pathlib import Path

from glu.store import Store, StoreError
from wgc import kb

# status → exit code of `glu receipt` (2 = operational error, raised as an exception)
EXIT = {"match": 0, "differs": 1, "no_job": 1, "no_receipt": 1, "pending_batch": 1}


def report(root: str | Path, job_id: str) -> dict:
    """`{job, status, …}`; see `EXIT` for the statuses. `StoreError`/`wgc.kb.KBError` on operational errors."""
    root = Path(root)
    with Store.at_root(root, read_only=True) as store:
        try:
            job = store.job(job_id)
        except StoreError:
            return {"job": job_id, "status": "no_job"}
        out = {"job": job_id, "task": job["task"], "state": job["state"]}
        receipt = next((a["kb_receipt"] for a in reversed(store.attempts(job_id)) if a.get("kb_receipt")), None)
        out["receipt"] = "attempt"
        if receipt is None and job["state"] == "validating":
            receipt, out["receipt"] = kb.read_receipt(root, job_id), "pending"
        if receipt is None:
            return {**out, "status": "no_receipt", "receipt": None}
        cmp = kb.compare_receipt(root, receipt)
        out.update(status=cmp.status, generation_equal=cmp.generation_equal, records=cmp.records)
        started = store.creation_seq(job_id)
        for info in cmp.records.values():
            other = info["job"]
            if info["state"] == "same" or other is None or other == job_id:
                continue
            try:
                store.job(other)
            except StoreError:
                info["later"] = None  # a job of a store that no longer exists (e.g. .glu/ recreated)
                continue
            other_started = store.creation_seq(other)
            info["later"] = None if started is None or other_started is None else other_started > started
    return out


STATE_PL = {"same": "zgodny", "changed": "inna treść w kb/", "missing": "brak w kb/"}


def lines(rep: dict) -> list[str]:
    """Polish text of a report."""
    job, status = rep["job"], rep["status"]
    if status == "no_job":
        return [f"Brak joba {job} w bazie stanu GLU."]
    head = f"Job {job} ({rep['task']}, stan: {rep['state']})"
    if status == "no_receipt":
        return [f"{head}: brak receiptu (job nie ma zaakceptowanego wyniku ani receiptu nierozstrzygniętej akceptacji)."]
    out = [head + (": receipt nierozstrzygniętej akceptacji z .glu/kb-receipts/ (przed reconcile)"
                   if rep["receipt"] == "pending" else ": receipt z Attemptu accepted")]
    if status == "pending_batch":
        return out + ["kb/ ma przerwaną partię zapisu: porównanie po `wgc kb recover` (to polecenie niczego nie "
                      "naprawia)."]
    for rid, info in rep["records"].items():
        label = ("wycofany, brak w kb/ (zgodny)" if info["state"] == "missing" else
                 "wycofany, znów obecny w kb/") if info.get("retired") else STATE_PL[info["state"]]
        line = f"  {rid}: {label}"
        if info["state"] != "same" and info.get("job") not in (None, job):
            when = {True: "późniejszy job", False: "wcześniejszy job", None: "job spoza tej bazy"}[info.get("later")]
            line += f" (bieżący rekord pochodzi z {info['job']}, {when})"
        elif info["state"] == "changed":
            line += " (bieżący rekord ma prov.job tego joba: zmiana poza accept())"
        out.append(line)
    out.append("Generacja kb/: " + ("równa receiptowi (kb/ bajt w bajt jak po akceptacji)." if rep["generation_equal"]
                                    else "inna niż w receipcie (kb/ zmieniło się od akceptacji)."))
    if status == "match":
        out.append("Wynik: zgodny. kb/ zawiera wynik joba.")
    else:
        out.append("Wynik: różnice. Różnica względem historycznego receiptu nie oznacza sama w sobie uszkodzenia: "
                   "kb/ mogło później zostać poprawnie zmienione (inny job, decyzja człowieka). Polecenie niczego nie "
                   "naprawia; rozbieżność bez późniejszej zmiany naprawia ponowny build.")
    return out

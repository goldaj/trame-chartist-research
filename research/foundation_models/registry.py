"""A6: frozen metadata for candidate time-series foundation checkpoints.

This module intentionally imports no model package, fetches no weights,
and cannot establish whether pretrained models saw evaluation series.
Never mistake code licensing for pretrained-weight licensing.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FoundationCandidate:
    id: str
    checkpoint: str
    code_license: str
    weight_license: str
    commercial_weight_eligible: bool
    contamination_status: str = "unknown"
    pretrained: bool = True


MODELS = {
    "timesfm3": FoundationCandidate(
        id="timesfm3", checkpoint="google/timesfm-3.0-pytorch",
        code_license="Apache-2.0",
        weight_license="timesfm-non-commercial-license-v1.0",
        commercial_weight_eligible=False),
    "chronos2": FoundationCandidate(
        id="chronos2", checkpoint="amazon/chronos-2",
        code_license="Apache-2.0", weight_license="Apache-2.0",
        commercial_weight_eligible=True),
    "moirai2": FoundationCandidate(
        id="moirai2", checkpoint="Salesforce/moirai-2.0-R-small",
        code_license="see SalesforceAIResearch/uni2ts at chosen version",
        weight_license="CC-BY-NC-4.0",
        commercial_weight_eligible=False),
}


def decision(model_id, *, commercial=False, confirmatory=False,
             revision=None):
    """Classify access, never assert missing contamination has been resolved."""
    if model_id not in MODELS:
        raise ValueError("unknown model id")
    if type(commercial) is not bool or type(confirmatory) is not bool:
        raise ValueError("booleans required")
    if revision is not None and (not isinstance(revision, str) or not revision.strip()):
        raise ValueError("revision must be a nonempty explicit commit SHA or None")
    spec = MODELS[model_id]
    blockers = []
    if commercial and not spec.commercial_weight_eligible:
        blockers.append("checkpoint_weight_license_noncommercial")
    if confirmatory and spec.contamination_status != "verified_clear":
        blockers.append("pretraining_contamination_unknown")
    if (commercial or confirmatory) and revision is None:
        blockers.append("checkpoint_revision_not_pinned")
    return {
        "id": spec.id, "checkpoint": spec.checkpoint,
        "weight_license": spec.weight_license,
        "commercial_weight_eligible": spec.commercial_weight_eligible,
        "pretraining_contamination_status": spec.contamination_status,
        "intended_use": "commercial" if commercial else "research",
        "confirmatory": confirmatory,
        "admissible_under_known_constraints": len(blockers) == 0,
        "blockers": blockers,
        "loaded_weights": False,
        "ran_forecasting": False,
    }

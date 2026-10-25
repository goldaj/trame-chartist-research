"""P1 research checkpoint manifest: validation without deserializing model code.

This proves only structural integrity and optional file-byte identity.
It does NOT prove that model training happened or that a financial test
was independent. A manifest cannot self-certify its own scientific truth.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

REQUIRED = frozenset((
    "source_release", "source_resolution", "split_version",
    "origin_policy", "architecture", "representation", "objective",
    "seed", "hardware", "environment", "train_budget", "search_budget",
    "code_commit", "train_only_transforms", "artifact_sha256",
    "weight_license", "independent_test_opened",
))
PINNED_BTC_TAG = "btcusd-bitstamp-2010-2026-reference-v1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
FORBIDDEN = ("secret", "private_key", "api_key", "access_token", "wallet", "password")
SAFE_CHECKPOINT_SUFFIXES = (".safetensors",)


def validate_manifest(manifest, *, checkpoint_path=None):
    if not isinstance(manifest, dict) or set(manifest) != REQUIRED:
        raise ValueError("exact research manifest fields required")
    if any(any(k in name.lower() for k in FORBIDDEN) for name in manifest):
        raise ValueError("credentials/identities forbidden")
    for name in ("source_release", "split_version", "origin_policy", "architecture",
                 "representation", "objective", "hardware", "environment", "weight_license"):
        value = manifest[name]
        if not isinstance(value, str) or not value.strip() or len(value) > 180:
            raise ValueError(f"{name} must be non-empty bounded string")
    if manifest["source_release"] != PINNED_BTC_TAG:
        raise ValueError("unexpected version of BTC release")
    if manifest["source_resolution"] not in ("D1", "H1", "M1"):
        raise ValueError("unsupported resolution")
    if type(manifest["seed"]) is not int or manifest["seed"] < 0:
        raise ValueError("nonnegative integer seed required")
    for field in ("train_budget", "search_budget"):
        value = manifest[field]
        if type(value) is not int or value < 0:
            raise ValueError(f"{field} must be a nonnegative integer")
    if manifest["train_budget"] == 0:
        raise ValueError("actual training requires nonzero declared budget")
    if manifest["train_only_transforms"] is not True:
        raise ValueError("transformations must have been fit on training only")
    if manifest["independent_test_opened"] is not False:
        raise ValueError("the independent test must remain sealed")
    if not HEX40.fullmatch(manifest["code_commit"]):
        raise ValueError("full 40-hex Git commit required")
    if not HEX64.fullmatch(manifest["artifact_sha256"]):
        raise ValueError("lowercase sha256 checkpoint fingerprint required")
    canonical = json.dumps(manifest, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":"), allow_nan=False).encode("utf-8")
    checkpoint_matches = False
    if checkpoint_path is not None:
        path = Path(checkpoint_path)
        if (not path.is_file() or path.is_symlink()
                or path.suffix.lower() not in SAFE_CHECKPOINT_SUFFIXES):
            raise ValueError("regular .safetensors checkpoint only, no pickle")
        digest = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != manifest["artifact_sha256"]:
            raise ValueError("checkpoint bytes disagree with declared sha256")
        checkpoint_matches = True
    return {
        "contract": "TRAME_P1_RESEARCH_CHECKPOINT_MANIFEST_V1",
        "manifest_sha256": hashlib.sha256(canonical).hexdigest(),
        "checkpoint_bytes_match_declared_sha256": checkpoint_matches,
        "training_run_independently_verified": False,
        "model_skill_independently_verified": False,
        "model_selected_for_product": False,
        "ready_for_production": False,
        "independent_test_opened_by_validator": False,
    }

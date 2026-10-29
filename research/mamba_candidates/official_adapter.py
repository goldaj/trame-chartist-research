"""Optional official GPU Mamba-2/3 bridges, never silently fake a CUDA backend.

No import of mamba_ssm until a user deliberately instantiates a GPU arm.
CPU-only unit tests can validate the explicit refusal path. The actual
forward/backward/causality path MUST be executed on a compatible GPU
before reporting that a Mamba candidate is validated.
"""
from __future__ import annotations

import importlib
import platform

import torch

from research.architecture_comparison.models import CausalGaussianModel


CANDIDATES = ("mamba2_official", "mamba3_official")
DEFAULT_WIDTH = 64
DEFAULT_CONTEXT = 64


def gpu_environment():
    """Read-only capabilities, with no third-party package import or download."""
    ready = bool(torch.cuda.is_available())
    return {
        "cuda_available": ready,
        "cuda_bf16_supported": bool(ready and torch.cuda.is_bf16_supported()),
        "cuda_device_name": torch.cuda.get_device_name(0) if ready else None,
        "torch_version": torch.__version__,
        "torch_cuda_runtime": torch.version.cuda,
        "python_version": platform.python_version(),
        "mamba_imported_or_installed": False,
        "actually_executed_mamba": False,
    }


def require_gpu():
    info = gpu_environment()
    if not info["cuda_available"]:
        raise RuntimeError("Official Mamba GPU execution requires CUDA; CPU substitute forbidden")
    if not info["cuda_bf16_supported"]:
        raise RuntimeError("Official Mamba candidate requires working CUDA bf16 support")
    return info


class OfficialMambaCandidate(CausalGaussianModel):
    """Common P1-B0 rounded-Gaussian output, optional official Mamba backbone."""

    def __init__(self, *, variant, width=DEFAULT_WIDTH,
                 length=DEFAULT_CONTEXT, device="cuda:0"):
        if variant not in CANDIDATES:
            raise ValueError("variant must be mamba2_official or mamba3_official")
        if type(width) is not int or width < 64 or width % 64:
            raise ValueError("width must be >=64 and a multiple of 64")
        if type(length) is not int or not 16 <= length <= 128:
            raise ValueError("length must be within 16..128")
        if device != "cuda:0":
            raise ValueError("only explicit cuda:0 device is supported by this pilot")
        require_gpu()
        try:
            package = importlib.import_module("mamba_ssm")
            cls = getattr(package, "Mamba2" if variant == "mamba2_official" else "Mamba3")
        except (ImportError, AttributeError) as exc:
            raise RuntimeError("Official mamba_ssm with Mamba2/Mamba3 must be installed opt-in") from exc
        super().__init__(width=width, length=length)
        if variant == "mamba2_official":
            core = cls(d_model=width, d_state=64, d_conv=4, expand=2)
        else:
            # Candidate SISO settings. Not asserted to match the vendor's
            # 768-dim MIMO example without real GPU verification.
            core = cls(d_model=width, d_state=128, headdim=64,
                       is_mimo=False, chunk_size=64, dtype=torch.bfloat16)
        self.variant = variant
        self.core = core.to(device=device, dtype=torch.bfloat16)
        self.to(device=device)

    def _validate(self, prior_codes):
        super()._validate(prior_codes)
        if prior_codes.device.type != "cuda" or prior_codes.device.index not in (0, None):
            raise ValueError("GPU model inputs must be float64 on cuda:0")

    def encode(self, x):
        encoded = self.core(x.to(dtype=torch.bfloat16))
        if encoded.shape != x.shape:
            raise RuntimeError("official Mamba backbone returned a different shape")
        return encoded.to(dtype=torch.float64)


def new_candidate(variant, *, width=DEFAULT_WIDTH, length=DEFAULT_CONTEXT):
    return OfficialMambaCandidate(variant=variant, width=width, length=length)

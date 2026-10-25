"""CPU-only import/guard tests; these are NOT Mamba GPU validation."""
import sys
import unittest
from unittest.mock import patch

from research.mamba_candidates.official_adapter import (
    CANDIDATES, OfficialMambaCandidate, gpu_environment, require_gpu,
)
from research.mamba_candidates.gpu_smoke import gpu_smoke


class OfficialMambaGuardsTests(unittest.TestCase):
    def test_read_only_cpu_environment(self):
        with patch("torch.cuda.is_available", return_value=False):
            info = gpu_environment()
        self.assertFalse(info["cuda_available"])
        self.assertFalse(info["cuda_bf16_supported"])
        self.assertFalse(info["actually_executed_mamba"])

    def test_cpu_refuses_without_importing_official_kernels(self):
        initial = set(sys.modules)
        with patch("torch.cuda.is_available", return_value=False):
            with self.assertRaisesRegex(RuntimeError, "CUDA"):
                require_gpu()
            for variant in CANDIDATES:
                with self.subTest(variant=variant):
                    with self.assertRaisesRegex(RuntimeError, "CUDA"):
                        OfficialMambaCandidate(variant=variant)
                    with self.assertRaisesRegex(RuntimeError, "CUDA"):
                        gpu_smoke(variant=variant)
        self.assertFalse(bool(set(sys.modules) - initial & {"mamba_ssm"}))

    def test_invalid_architecture_and_dimensions(self):
        with self.assertRaises(ValueError):
            OfficialMambaCandidate(variant="recurrent_gru_control")
        for kwargs in ({"variant": CANDIDATES[0], "width": 16},
                       {"variant": CANDIDATES[0], "length": 256},
                       {"variant": CANDIDATES[0], "device": "cpu"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                OfficialMambaCandidate(**kwargs)

    def test_reject_fake_success_conditions(self):
        with self.assertRaises(ValueError):
            gpu_smoke(variant="not_mamba")
        with self.assertRaises(ValueError):
            gpu_smoke(variant=CANDIDATES[0], batch=True)


if __name__ == "__main__":
    unittest.main()

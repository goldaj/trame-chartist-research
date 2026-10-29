"""Offline tests of pinned PRIVATE BTC release asset acquisition.

Simulated gh calls only; never connect GitHub or use a real token.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase, mock

from research.btc_h1_m1 import release_store as store


class ReleaseCacheTests(TestCase):
    def test_exact_registry_and_pinned_source(self):
        self.assertEqual(store.REPOSITORY, "goldaj/btc-historical-data")
        self.assertEqual(store.TAG, "btcusd-bitstamp-2010-2026-reference-v1")
        self.assertEqual(len(store.selected_names("D1")), 3)
        self.assertEqual(len(store.selected_names("H1")), 1)
        self.assertEqual(len(store.selected_names("M1")), 15)
        self.assertEqual(len(store.selected_names("ALL")), 19)
        self.assertEqual(len(store.ASSETS), 19)
        with self.assertRaises(ValueError):
            store.selected_names("hyperliquid")

    def test_missing_files_fail_closed_offline(self):
        with TemporaryDirectory() as d:
            with self.assertRaisesRegex(FileNotFoundError, "--download"):
                store.ensure_assets("H1", directory=Path(d))
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_authenticated_gh_only_downloads_missing_assets(self):
        with TemporaryDirectory() as d:
            folder = Path(d)
            filename = store.H1_FILES[0]
            with mock.patch.dict(store.ASSETS, {filename: 12}):
                def fake_download(args, **kwargs):
                    self.assertEqual(args[:4], ["gh", "release", "download", store.TAG])
                    self.assertEqual(args[4:6], ["--repo", store.REPOSITORY])
                    self.assertEqual(args[6:8], ["--pattern", filename])
                    self.assertEqual(args[8:10], ["--dir", str(folder)])
                    (folder / filename).write_bytes(b"B" * 12)
                    return SimpleNamespace(returncode=0)
                with mock.patch.object(store.subprocess, "run",
                                       side_effect=fake_download) as call:
                    result = store.ensure_assets("H1", directory=folder, download=True)
                    self.assertEqual(result, (folder / filename,))
                    self.assertEqual(call.call_count, 1)
                with mock.patch.object(store.subprocess, "run") as call:
                    self.assertEqual(store.ensure_assets("H1", directory=folder), result)
                    call.assert_not_called()

    def test_invalid_cache_not_overwritten(self):
        with TemporaryDirectory() as d:
            f=Path(d) / store.H1_FILES[0]
            f.write_bytes(b"incomplete")
            with mock.patch.object(store.subprocess, "run") as run:
                with self.assertRaisesRegex(ValueError, "unexpected byte count"):
                    store.ensure_assets("H1",directory=Path(d),download=True)
                run.assert_not_called()

    def test_gh_failure_sanitized(self):
        with TemporaryDirectory() as d:
            with mock.patch.object(store.subprocess,"run",
                    return_value=SimpleNamespace(returncode=1,
                      stderr="PRIVATE_AUTH_TOKEN_MUST_NOT_APPEAR")):
                with self.assertRaises(RuntimeError) as raised:
                    store.ensure_assets("H1",directory=Path(d),download=True)
                self.assertNotIn("PRIVATE_AUTH_TOKEN_MUST_NOT_APPEAR",str(raised.exception))

    def test_symlink_never_read(self):
        with TemporaryDirectory() as d:
            root=Path(d)
            source=root / "other"
            source.write_bytes(b"secret")
            path=root / store.H1_FILES[0]
            path.symlink_to(source)
            with self.assertRaisesRegex(ValueError,"symlinked"):
                store.ensure_assets("H1",directory=root,download=False)


if __name__ == "__main__":
    import unittest
    unittest.main()

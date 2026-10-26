"""Offline tests for a real public D1 reference and invented gzip download bytes.

No network request, no private release, no credentials, and no trading.
"""
from __future__ import annotations

import hashlib
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from research.data import public_data
from research.btc_h1_m1.daily import read_daily
from research.btc_h1_m1.stream import iter_cases


class _Response(BytesIO):
    status = 200


class PublicBTCDataTests(unittest.TestCase):
    def test_vendored_2012_daily_identity_and_complete_range(self):
        meta=public_data._verified(
            public_data.DAILY,size=public_data.DAILY_SIZE,
            blob=public_data.DAILY_BLOB)
        self.assertEqual(meta["bytes"],372096)
        self.assertEqual(meta["git_blob_sha1"],public_data.DAILY_BLOB)
        with TemporaryDirectory() as folder:
            destination=Path(folder)
            records=public_data.install("D1",directory=destination,
                                        download=False)
            self.assertEqual(len(records),1)
            days=list(read_daily(directory=destination))
            self.assertEqual(days[0].day.isoformat(),"2012-01-01")
            self.assertEqual(days[-1].day.isoformat(),"2026-06-30")
            self.assertTrue(all(x.grade=="bitstamp_spot_ohlcv" for x in days))
            self.assertEqual(days[-1].available_at_utc.date().isoformat(),
                             "2026-07-01")
            cases=list(iter_cases("D1",destination))
            self.assertGreater(len(cases),100)
            self.assertTrue(all(c.target_open.year<2026 for _,c in cases))
            self.assertTrue(all(c.grade=="bitstamp_D1_observed_nonzero_volume"
                                for _,c in cases))
            self.assertTrue(any(kind=="train" for kind,_ in cases))
            self.assertTrue(any(kind=="development" for kind,_ in cases))

    def test_pinned_public_source_manifest_has_expected_archives(self):
        data=public_data.load_manifest()
        self.assertEqual(len(public_data._selection("M1",data)),15)
        self.assertEqual(len(public_data._selection("H1",data)),1)
        self.assertEqual(len(public_data._selection("D1",data)),1)
        self.assertEqual(len(public_data._selection("ALL",data)),17)
        with self.assertRaises(ValueError):
            public_data._selection("BAD",data)

    def test_download_pins_hash_and_rejects_corruption(self):
        blob=b"example compressed archive bytes; fake for test only"
        prefix=f"blob {len(blob)}\0".encode()
        sha=hashlib.sha1(prefix+blob).hexdigest()
        item={
            "relative_path":"bitstamp/1h/BTCUSD_bitstamp_hourly_2012-2026.csv.gz",
            "size_bytes":len(blob),
            "git_blob_sha1":sha,
        }
        with TemporaryDirectory() as folder:
            path=Path(folder)/"BTCUSD_bitstamp_hourly_2012-2026.csv.gz"
            with patch.object(public_data,"urlopen",return_value=_Response(blob)):
                record=public_data._download_one(item,path)
            self.assertEqual(record["git_blob_sha1"],sha)
            self.assertEqual(path.read_bytes(),blob)
            with patch.object(public_data,"urlopen",
                              side_effect=AssertionError("unexpected network")):
                self.assertEqual(public_data._download_one(item,path)["sha256"],
                                 hashlib.sha256(blob).hexdigest())
            path.write_bytes(b"corrupted bytes")
            with self.assertRaises(public_data.IntegrityError):
                public_data._download_one(item,path)

    def test_rejects_manifest_traversal_and_symlink(self):
        data=public_data.load_manifest()
        changed={"repo":data["repo"],"commit":data["commit"],
                 "files":[dict(x) for x in data["files"]]}
        changed["files"][0]["relative_path"]="../unsafe.csv.gz"
        with TemporaryDirectory() as folder:
            changed_path=Path(folder)/"bad_manifest.json"
            changed_path.write_text(__import__("json").dumps(changed),encoding="utf-8")
            with patch.object(public_data,"MANIFEST",changed_path):
                with self.assertRaises(public_data.IntegrityError):
                    public_data.load_manifest()


if __name__=="__main__":
    unittest.main()

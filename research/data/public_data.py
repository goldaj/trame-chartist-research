"""Install verified PUBLIC-source Bitstamp datasets into TRAME's existing cache.

No GitHub private token, wallet, broker, or Actions workflow is required.
The D1 2012+ CSV is vendored (text). H1/M1 compressed archives come from
the pinned public upstream Git blob, not from the private release.

Existing A7/S1/S2 readers continue to use TRAME_BTC_CACHE_DIR, without
requiring data to be committed to Git history. SHA-1 is for Git blob
IDENTITY only; SHA-256 is recorded as a second digest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
from urllib.request import Request, urlopen

from research.btc_h1_m1.release_store import DEFAULT_CACHE

REFERENCE_DIR = Path(__file__).resolve().parent / "reference"
MANIFEST = REFERENCE_DIR / "bitstamp_source_manifest.json"
DAILY = REFERENCE_DIR / "btcusd-bitstamp-d1-2012-2026H1.csv"
DAILY_NAME = DAILY.name
DAILY_SIZE = 372096
DAILY_BLOB = "a8f2da91cb00fce75117ba5bf000384f240abd56"
PINNED_COMMIT = "b57f460fab1afb82705eb813cee2ef4afb1f6848"
UPSTREAM = "https://raw.githubusercontent.com/alessiostomeo/btc-cycle-data/"
RESOLUTIONS = ("D1", "H1", "M1", "ALL")


class IntegrityError(ValueError):
    pass


def digest(path: Path) -> tuple[str, str, int]:
    if path.is_symlink() or not path.is_file():
        raise IntegrityError("not a regular file")
    length = path.stat().st_size
    git = hashlib.sha1(f"blob {length}\\0".encode("ascii"))
    sha256 = hashlib.sha256()
    with path.open("rb") as src:
        for block in iter(lambda: src.read(1024 * 1024), b""):
            git.update(block)
            sha256.update(block)
    return git.hexdigest(), sha256.hexdigest(), length


def _verified(path, *, size, blob):
    sha, sha256, length = digest(path)
    if length != size or sha != blob:
        raise IntegrityError(f"size or Git blob mismatch: {path.name}")
    return {"name": path.name, "bytes": length, "git_blob_sha1": sha,
            "sha256": sha256}


def load_manifest():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = data["files"]
    if data.get("repo") != "alessiostomeo/btc-cycle-data" or data.get("commit") != PINNED_COMMIT:
        raise IntegrityError("unapproved source revision")
    if len(items) != 16 or len({x["id"] for x in items}) != 16:
        raise IntegrityError("expected exactly 16 original gzip files")
    for item in items:
        name = item.get("relative_path", "")
        path = Path(name)
        if (path.is_absolute() or ".." in path.parts or len(path.parts)!=3
                or path.parts[:2] not in (("bitstamp","1min"),("bitstamp","1h"))
                or not path.name.endswith(".csv.gz")
                or type(item.get("size_bytes")) is not int
                or not 1000 <= item["size_bytes"] <= 20_000_000
                or len(item.get("git_blob_sha1",""))!=40):
            raise IntegrityError("unexpected file in source manifest")
    return data


def _selection(resolution, manifest):
    if resolution not in RESOLUTIONS:
        raise ValueError("resolution must be D1/H1/M1/ALL")
    out=[]
    if resolution in ("D1","ALL"):
        out.append(("D1", DAILY_NAME, None))
    if resolution in ("H1","ALL"):
        out.extend(("H1", Path(x["relative_path"]).name, x)
                   for x in manifest["files"] if x["interval_seconds"]==3600)
    if resolution in ("M1","ALL"):
        out.extend(("M1", Path(x["relative_path"]).name, x)
                   for x in manifest["files"] if x["interval_seconds"]==60)
    expected={"D1":1,"H1":1,"M1":15,"ALL":17}[resolution]
    if len(out)!=expected:
        raise IntegrityError(f"expected {expected} files, found {len(out)}")
    return out


def _download_one(item, destination:Path):
    """Atomic verified transfer. Never change an existing mismatched source."""
    if destination.exists() or destination.is_symlink():
        return _verified(destination,size=item["size_bytes"],
                         blob=item["git_blob_sha1"])
    url = UPSTREAM + PINNED_COMMIT + "/" + item["relative_path"]
    partial = destination.with_name(destination.name + ".partial")
    if partial.exists() or partial.is_symlink():
        raise IntegrityError("untrusted leftover partial download")
    error = None
    for retry in range(3):
        try:
            req=Request(url,headers={"User-Agent":"TRAME-pinned-market-research/1.0"})
            with urlopen(req,timeout=90) as reply, partial.open("xb") as target:
                if getattr(reply,"status",200)!=200:
                    raise IntegrityError("upstream returned non-200 status")
                n=0
                while True:
                    data=reply.read(1024*1024)
                    if not data:
                        break
                    n += len(data)
                    if n>item["size_bytes"]:
                        raise IntegrityError("upstream larger than pinned size")
                    target.write(data)
                if n!=item["size_bytes"]:
                    raise IntegrityError("upstream shorter than pinned size")
            record=_verified(partial,size=item["size_bytes"],
                             blob=item["git_blob_sha1"])
            os.replace(partial,destination)
            return {**record,"name":destination.name}
        except (OSError, ValueError, IntegrityError) as exc:
            error=exc
            partial.unlink(missing_ok=True)
            if retry<2:
                time.sleep(1)
    raise IntegrityError(f"source download failed for {destination.name}: {error}")


def install(resolution, *, directory:Path=DEFAULT_CACHE, download=True):
    manifest=load_manifest()
    root=Path(directory).expanduser()
    if root.is_symlink():
        raise IntegrityError("cache directory may not be symlink")
    selection=_selection(resolution,manifest)
    root.mkdir(parents=True,exist_ok=True)
    done=[]
    for _,filename,item in selection:
        dest=root/filename
        if item is None:
            verified=_verified(DAILY,size=DAILY_SIZE,blob=DAILY_BLOB)
            if dest.exists() or dest.is_symlink():
                record=_verified(dest,size=DAILY_SIZE,blob=DAILY_BLOB)
            else:
                shutil.copyfile(DAILY,dest)
                record=_verified(dest,size=DAILY_SIZE,blob=DAILY_BLOB)
            done.append(record)
        elif download:
            done.append(_download_one(item,dest))
        elif dest.exists():
            done.append(_verified(dest,size=item["size_bytes"],
                                  blob=item["git_blob_sha1"]))
        else:
            raise FileNotFoundError(f"missing {filename}; rerun without --check-only")
    return done


def main(argv=None):
    p=argparse.ArgumentParser(description="Install BTC public-origin original D1/H1/M1 archives with Git SHA verification")
    p.add_argument("--resolution",choices=RESOLUTIONS,required=True)
    p.add_argument("--directory",type=Path,default=DEFAULT_CACHE)
    p.add_argument("--check-only",action="store_true",help="never access network (D1 can still be copied locally)")
    args=p.parse_args(argv)
    try:
        report=install(args.resolution,directory=args.directory,
                       download=not args.check_only)
    except (OSError, IntegrityError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"DATA_IMPORT_FAILED: {exc}",file=sys.stderr)
        return 2
    print(json.dumps({
        "source":"public GitHub at pinned commit",
        "downloaded_archives":len(report),
        "total_bytes":sum(r["bytes"] for r in report),
        "cache":str(args.directory),
        "files":report,
        "note":"Data downloaded/verified, NOT a new BTC prediction or opening of the 2026 test set."
    },indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())

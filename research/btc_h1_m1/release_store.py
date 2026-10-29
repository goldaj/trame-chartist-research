"""Pinned private GitHub Release as the canonical BTC/USD historical dataset.

No archives belong in the TRAME Git repository. The GitHub CLI downloads
unchanged assets to a local cache only when explicitly requested. It uses
the caller's existing GitHub authentication and never reads or stores tokens.

This module does not investigate upstream price provenance. It checks only
file identity by exact release filename and expected byte count.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess


REPOSITORY = "goldaj/btc-historical-data"
TAG = "btcusd-bitstamp-2010-2026-reference-v1"
RELEASE_URL = f"https://github.com/{REPOSITORY}/releases/tag/{TAG}"
DEFAULT_CACHE = Path(
    os.environ.get("TRAME_BTC_CACHE_DIR",
                   str(Path.home() / ".cache" / "trame" / "bitcoin" / TAG))
).expanduser()
ASSETS = {
    "btcusd-indicative-close-d1-2010-2011.csv": 6364,
    "btcusd-bitstamp-d1-2011H2.csv": 5916,
    "btcusd-bitstamp-d1-2012-2026H1.csv": 372096,
    "BTCUSD_bitstamp_hourly_2012-2026.csv.gz": 2727050,
    "BTCUSD_bitstamp_1min_2012.csv.gz": 1542568,
    "BTCUSD_bitstamp_1min_2013.csv.gz": 4534716,
    "BTCUSD_bitstamp_1min_2014.csv.gz": 5876556,
    "BTCUSD_bitstamp_1min_2015.csv.gz": 5604297,
    "BTCUSD_bitstamp_1min_2016.csv.gz": 5151558,
    "BTCUSD_bitstamp_1min_2017.csv.gz": 8310425,
    "BTCUSD_bitstamp_1min_2018.csv.gz": 9354174,
    "BTCUSD_bitstamp_1min_2019.csv.gz": 9312143,
    "BTCUSD_bitstamp_1min_2020.csv.gz": 9941171,
    "BTCUSD_bitstamp_1min_2021.csv.gz": 11064625,
    "BTCUSD_bitstamp_1min_2022.csv.gz": 8830442,
    "BTCUSD_bitstamp_1min_2023.csv.gz": 7200642,
    "BTCUSD_bitstamp_1min_2024.csv.gz": 8301488,
    "BTCUSD_bitstamp_1min_2025.csv.gz": 8532805,
    "BTCUSD_bitstamp_1min_2026.csv.gz": 6447679,
}
D1_FILES = (
    "btcusd-indicative-close-d1-2010-2011.csv",
    "btcusd-bitstamp-d1-2011H2.csv",
    "btcusd-bitstamp-d1-2012-2026H1.csv",
)
H1_FILES = ("BTCUSD_bitstamp_hourly_2012-2026.csv.gz",)
M1_FILES = tuple(f"BTCUSD_bitstamp_1min_{year}.csv.gz" for year in range(2012, 2027))


def selected_names(resolution: str) -> tuple[str, ...]:
    if resolution == "D1":
        return D1_FILES
    if resolution == "H1":
        return H1_FILES
    if resolution == "M1":
        return M1_FILES
    if resolution == "ALL":
        return D1_FILES + H1_FILES + M1_FILES
    raise ValueError("resolution must be D1, H1, M1 or ALL")


def ensure_assets(resolution: str, *, directory: Path = DEFAULT_CACHE,
                  download: bool = False, executable: str = "gh") -> tuple[Path, ...]:
    """Return local assets; optionally retrieve missing ones from PRIVATE release.

    Never overwrite existing files or fallback to another source/release.
    Failure messages never contain gh stdout/stderr or credentials.
    """
    names = selected_names(resolution)
    root = Path(directory).expanduser()
    missing = []
    for filename in names:
        path = root / filename
        if path.is_symlink():
            raise ValueError(f"refusing symlinked archive: {filename}")
        if path.exists():
            if not path.is_file() or path.stat().st_size != ASSETS[filename]:
                raise ValueError(f"cached archive has unexpected byte count: {filename}")
        else:
            missing.append(filename)
    if missing and not download:
        raise FileNotFoundError(
            f"{len(missing)} missing BTC {resolution} release assets in {root}. "
            "Run: python -m research.btc_h1_m1.release_store --resolution "
            f"{resolution} --download"
        )
    if missing:
        root.mkdir(parents=True, exist_ok=True)
        for filename in missing:
            command = [
                executable, "release", "download", TAG, "--repo", REPOSITORY,
                "--pattern", filename, "--dir", str(root)
            ]
            try:
                completed = subprocess.run(command, capture_output=True, text=True,
                                           timeout=600, check=False)
            except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
                raise RuntimeError(
                    f"Unable to access private GitHub Release using {executable}; "
                    "install GitHub CLI and authenticate with gh auth login"
                ) from exc
            if completed.returncode:
                raise RuntimeError(
                    f"Private GitHub Release download failed for {filename}; "
                    "verify gh auth status and repository access"
                )
            path = root / filename
            if (not path.is_file() or path.is_symlink()
                    or path.stat().st_size != ASSETS[filename]):
                raise ValueError(f"release download incomplete: {filename}")
    return tuple(root / name for name in names)


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description="Read or cache pinned PRIVATE Bitcoin Release")
    p.add_argument("--resolution", choices=("D1", "H1", "M1", "ALL"), required=True)
    p.add_argument("--directory", type=Path, default=DEFAULT_CACHE)
    p.add_argument("--download", action="store_true",
                   help="Download only missing, exact release asset names using gh")
    args = p.parse_args(argv)
    files = ensure_assets(args.resolution, directory=args.directory,
                          download=args.download)
    print(f"Private release: {RELEASE_URL}")
    print(f"Cached {len(files)} unchanged files in {args.directory}")


if __name__ == "__main__":
    main()

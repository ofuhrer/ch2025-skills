#!/usr/bin/env python3
"""Discover public CH2025 sources or retrieve one station asset. Python 3.10+."""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import zipfile

SKILL = Path(__file__).resolve().parents[1]
STAC = "https://data.geo.admin.ch/api/stac/v1"
COLLECTION = "ch.meteoschweiz.ogd-climate-scenarios-ch2025"
DOI = "https://doi.org/10.18751/climate/scenarios/ch2025/data/1.0/"


def request(url):
    if urlparse(url).scheme != "https":
        raise ValueError("Expected an HTTPS public source URL")
    return urlopen(Request(url, headers={"User-Agent": "CH2025-skills/0.1"}), timeout=45)


def fetch_json(url):
    with request(url) as response:
        raw = response.read(5_000_001)
        if len(raw) > 5_000_000:
            raise ValueError("Metadata exceeds 5 MB; refine the request")
        return json.loads(raw)


def station_asset(station, parameter, gwl, file_format):
    station, parameter, gwl = station.lower(), parameter.lower(), gwl.lower()
    if not re.fullmatch(r"[a-z0-9]{3,16}", station):
        raise ValueError("Use a station identifier from the official station metadata")
    item_url = f"{STAC}/collections/{COLLECTION}/items/{station}"
    item = fetch_json(item_url)
    key = f"ogd-climate-scenarios-ch2025_{station}_{parameter}_{gwl}.{file_format}"
    asset = item.get("assets", {}).get(key)
    if not asset:
        choices = sorted(item.get("assets", {}))
        raise ValueError(f"Asset not available: {key}. Inspect the station item: {item_url}. "
                         f"Available asset count: {len(choices)}")
    href = asset.get("href", "")
    if urlparse(href).scheme != "https":
        raise ValueError("Station asset has no HTTPS download URL")
    return dict(station=station, parameter=parameter, gwl=gwl, format=file_format,
                asset=key, url=href, item_url=item_url, metadata=asset,
                citation="MeteoSwiss & ETH Zurich (2025): Climate CH2025 – Daily Datasets.",
                doi=DOI, licence="CC BY 4.0", status="discovered")


def inspect_csv(path):
    metadata = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for line in stream:
            if line.startswith("DATE;"):
                models = next(csv.reader([line], delimiter=";"))[1:]
                rows = 0
                first = last = None
                for row in csv.reader(stream, delimiter=";"):
                    if len(row) != len(models) + 1:
                        raise ValueError("Ragged daily CSV row")
                    first = first or row[0]
                    last = row[0]
                    rows += 1
                return dict(metadata=metadata, models=models, model_count=len(models),
                            rows=rows, first_date=first, last_date=last)
            if ";" in line:
                key, value = line.rstrip("\r\n").split(";", 1)
                metadata[key] = value
    raise ValueError("Response is not a CH2025 daily CSV: DATE header missing")


def download(asset, directory, max_bytes):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / asset["asset"]
    sidecar = target.with_name(target.name + ".provenance.json")
    partial = target.with_name(target.name + ".part")
    if any(p.exists() for p in (target, sidecar, partial)):
        raise ValueError(f"Refusing to overwrite an existing output for {target.name}")
    made_partial = False
    try:
        with request(asset["url"]) as response:
            if int(response.headers.get("Content-Length", 0)) > max_bytes:
                raise ValueError("Download exceeds --max-mb; choose a smaller product or raise the limit")
            digest, size = hashlib.sha256(), 0
            with partial.open("xb") as stream:
                made_partial = True
                while chunk := response.read(262144):
                    size += len(chunk)
                    if size > max_bytes:
                        raise ValueError("Download exceeds --max-mb")
                    digest.update(chunk)
                    stream.write(chunk)
        if asset["format"] == "csv":
            inspection = inspect_csv(partial)
        else:
            with zipfile.ZipFile(partial) as archive:
                if archive.testzip() is not None:
                    raise ValueError("ZIP integrity check failed")
                inspection = {"members": archive.namelist(), "member_count": len(archive.namelist())}
        record = dict(asset, status="downloaded", path=str(target.resolve()), bytes=size,
                      sha256=digest.hexdigest(), inspection=inspection,
                      retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat())
        # Reserve the final path without replacing a file created after the initial check.
        with target.open("xb") as output, partial.open("rb") as source:
            while chunk := source.read(262144):
                output.write(chunk)
        with sidecar.open("x", encoding="utf-8") as stream:
            json.dump(record, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        record["provenance_path"] = str(sidecar.resolve())
        return record
    finally:
        if made_partial:
            partial.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    sources = commands.add_parser("sources", help="List bundled public sources; no network request")
    sources.add_argument("--topic", default="")
    station = commands.add_parser("station", help="Discover one station asset; optionally download it")
    station.add_argument("--station", required=True)
    station.add_argument("--parameter", required=True, choices=["tas", "tasmin", "tasmax", "pr", "rsds", "hurs", "sfcwind"])
    station.add_argument("--gwl", required=True, type=str.lower, choices=["ref91-20", "gwl1.5", "gwl2.0", "gwl2.5", "gwl3.0"])
    station.add_argument("--format", choices=["csv", "zip"], default="csv")
    station.add_argument("--download", metavar="DIRECTORY")
    station.add_argument("--max-mb", type=int, default=25)
    args = parser.parse_args()
    try:
        if args.command == "sources":
            sources = json.loads((SKILL / "references/sources.json").read_text())
            result = [s for s in sources if args.topic.lower() in json.dumps(s, ensure_ascii=False).lower()]
        else:
            if args.max_mb <= 0:
                raise ValueError("--max-mb must be positive")
            result = station_asset(args.station, args.parameter, args.gwl, args.format)
            if args.download:
                result = download(result, args.download, args.max_mb * 1_000_000)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, HTTPError, URLError, zipfile.BadZipFile) as exc:
        message = f"HTTP {exc.code}" if isinstance(exc, HTTPError) else str(exc)
        print(json.dumps({"status": "failed", "error": message,
                          "official_access_guide": "https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios"}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

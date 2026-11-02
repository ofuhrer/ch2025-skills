#!/usr/bin/env python3
"""Discover CH2025 sources, atlas/grid/station products, or retrieve a station asset. Python 3.10+."""
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
from urllib.parse import urlparse, urlencode
from urllib.request import Request, urlopen
import zipfile

SKILL = Path(__file__).resolve().parents[1]
STAC = "https://data.geo.admin.ch/api/stac/v1"
COLLECTION = "ch.meteoschweiz.ogd-climate-scenarios-ch2025"
DOI = "https://doi.org/10.18751/climate/scenarios/ch2025/data/1.0/"
ATLAS = "https://api.productbrowser.app.meteoswiss.ch/pbbackend/api/v1/displays/"


def products():
    return json.loads((SKILL / "references/products.json").read_text())


def atlas_product(product, language="en", selections=None, product_type=None):
    """Discover a live display, rejecting silently changed or dropped selections."""
    entry = next((p for p in products() if p["key"] == product), None)
    if entry is None:
        raise ValueError("Unknown atlas product; use the products command")
    requested = dict(selections or {})
    if any(not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", key) for key in requested):
        raise ValueError("Use live option IDs, e.g. scenarioIndicator, region or location")
    if "language" in requested and requested["language"] != language:
        raise ValueError("Specify language using --language")
    requested["language"] = language
    if product_type:
        requested["productType"] = product_type
    query = {"lang": language, "isPlayerActive": "false"}
    query.update({"cg1." + key: value for key, value in requested.items()})
    configuration_url = ATLAS + entry["display_id"] + "?" + urlencode(query)
    display = fetch_json(configuration_url)
    groups = display.get("componentGroups", [])
    if not groups:
        raise ValueError("Atlas returned no display state; use the official application")
    selected = groups[0].get("stateEntries", {})
    changed = {key: {"requested": value, "returned": selected.get(key)}
               for key, value in requested.items() if selected.get(key) != value}
    if changed:
        raise ValueError("Atlas changed or dropped requested selections: " + json.dumps(changed) +
                         ". Inspect live options; some data products combine multiple locations, seasons or pathways.")
    options, realizations, information = [], [], []
    for component in display.get("components", []):
        value = component.get("value", {})
        if component.get("type") == "form":
            options.extend(value.get("elements", []))
        elif component.get("type") == "media":
            realizations.extend(value.get("realizations", []))
        elif component.get("type") == "info" and value.get("url"):
            information.append(value["url"])
    return dict(status="discovered", product=product, title=entry["title"],
                official_url=entry["url"], configuration_url=configuration_url,
                requested=requested, selected=selected, options=options,
                information_urls=information, realizations=realizations,
                citation="MeteoSwiss and ETH Zurich, Climate CH2025",
                licence="CC BY 4.0", notes="Implementation API; verify content and read product information. No data file downloaded.")


def station_catalogue(query):
    """Resolve station names/codes using the collection's actual metadata asset."""
    collection_url = f"{STAC}/collections/{COLLECTION}"
    collection = fetch_json(collection_url)
    matches = [a for key, a in collection.get("assets", {}).items() if key.endswith("_meta_stations.csv")]
    if len(matches) != 1:
        raise ValueError("Could not identify station metadata; use the official catalogue")
    url = matches[0]["href"]
    with request(url) as response:
        raw = response.read(5_000_001)
    if len(raw) > 5_000_000:
        raise ValueError("Station metadata exceeds 5 MB")
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")), delimiter=";")
    if not reader.fieldnames or not {"station_abbr", "station_name"}.issubset(reader.fieldnames):
        raise ValueError("Unrecognized station metadata schema")
    rows = [row for row in reader if query.casefold() in
            " ".join([row["station_abbr"], row["station_name"], row.get("station_canton", "")]).casefold()]
    return dict(status="discovered", query=query, metadata_url=url, stations=rows,
                note="Check variable availability in each station item; a station is not a municipality average.")


def grid_assets(parameter, gwl, model=None):
    item_url = f"{STAC}/collections/{COLLECTION}-grid/items/ch"
    item = fetch_json(item_url)
    suffix = "_" + gwl.lower() + ".nc"
    prefix = "ogd-climate-scenarios-ch2025-grid_ch_" + parameter.lower() + "_"
    assets = [dict(asset=key, **value) for key, value in item.get("assets", {}).items()
              if key.startswith(prefix) and key.endswith(suffix) and
              (not model or model.lower() in key[len(prefix):-len(suffix)])]
    if not assets:
        raise ValueError("No matching grid assets; inspect the current grid catalogue")
    return dict(status="discovered", item_url=item_url, parameter=parameter, gwl=gwl,
                assets=assets, doi=DOI, licence="CC BY 4.0",
                note="Metadata only. Raw daily grid files can exceed 1 GB; no file downloaded.")


def request(url):
    if urlparse(url).scheme != "https":
        raise ValueError("Expected an HTTPS public source URL")
    return urlopen(Request(url, headers={"User-Agent": "CH2025-skills/0.2"}), timeout=45)


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
    commands.add_parser("products", help="List all eight atlas families; no network request")
    atlas = commands.add_parser("atlas", help="Discover live atlas options and figures/data; no file download")
    atlas.add_argument("--product", required=True, choices=[p["key"] for p in products()])
    atlas.add_argument("--language", choices=["de", "fr", "it", "en"], default="en")
    atlas.add_argument("--select", action="append", default=[], metavar="OPTION=VALUE")
    atlas.add_argument("--product-type", choices=["plot", "data"])
    stations = commands.add_parser("stations", help="Find names/codes in official station metadata")
    stations.add_argument("--query", required=True)
    grid = commands.add_parser("grid", help="Discover daily-grid assets without downloading large files")
    grid.add_argument("--parameter", required=True, choices=["tas", "tasmin", "tasmax", "pr"])
    grid.add_argument("--gwl", required=True, type=str.lower, choices=["ref91-20", "gwl1.5", "gwl2.0", "gwl2.5", "gwl3.0"])
    grid.add_argument("--model", help="Optional model-chain substring to filter actual asset keys")
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
        elif args.command == "products":
            result = products()
        elif args.command == "atlas":
            selections = {}
            for option in args.select:
                key, separator, value = option.partition("=")
                if not separator or not value or key in selections:
                    raise ValueError("Use unique --select OPTION=VALUE entries")
                selections[key] = value
            result = atlas_product(args.product, args.language, selections, args.product_type)
        elif args.command == "stations":
            result = station_catalogue(args.query)
        elif args.command == "grid":
            result = grid_assets(args.parameter, args.gwl, args.model)
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

#!/usr/bin/env python3
"""Probe live CH2025 discovery; optionally download one small station CSV in a temporary directory."""
import argparse
import datetime as dt
import importlib.util
import json
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ch2025", ROOT / "skills/ch2025/scripts/ch2025.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def check_catalogue():
    url = ("https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/"
           "reports-data-and-graphs-of-climate-change-scenarios/swiss-climate-scenarios-web-atlas.html")
    with helper.request(url) as response:
        raw = response.read(5_000_001)
    assert len(raw) <= 5_000_000, "Atlas catalogue exceeds metadata limit"
    found = set(re.findall(r"/applications/ext/(climate-ch2025-[a-z-]+)\.html", raw.decode()))
    registered = {p["display_id"] for p in helper.products()}
    assert found == registered, f"Atlas catalogue changed: unregistered={sorted(found - registered)}, absent={sorted(registered - found)}"
    return {"url": url, "display_ids": sorted(found)}


def check_atlas(product, **kwargs):
    result = helper.atlas_product(product, **kwargs)
    assert result["information_urls"], "Missing product information"
    return {key: result[key] for key in ("configuration_url", "selected", "information_urls", "realizations")}


def check_stations():
    result = helper.station_catalogue("Bern")
    assert any(row["station_abbr"].lower() == "ber" for row in result["stations"])
    return result


def check_station(download):
    asset = helper.station_asset("ber", "tas", "gwl3.0", "csv")
    if not download:
        return asset
    with tempfile.TemporaryDirectory() as tmp:
        result = helper.download(asset, tmp, 25_000_000)
        result.pop("path")
        result.pop("provenance_path")
        result["note"] = "Verified original and provenance; temporary files removed after check."
        return result


def check_dropped_selection():
    try:
        helper.atlas_product("stations", selections={"location": "BER"}, product_type="data")
    except ValueError as exc:
        if "changed or dropped" not in str(exc):
            raise
        return {"rejected": str(exc)}
    raise AssertionError("Data mode now accepts location; inspect and update the contract check")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Also verify one Bern CSV (up to 25 MB)")
    parser.add_argument("--output", type=Path, help="Save full JSON evidence")
    args = parser.parse_args()
    checks = [("atlas-catalogue", check_catalogue)]
    checks += [("atlas-" + p["key"], lambda key=p["key"]: check_atlas(key)) for p in helper.products()]
    checks += [
        ("station-names", check_stations),
        ("grid", lambda: helper.grid_assets("tas", "gwl3.0", "clmcom-cclm4-cccma")),
        ("station", lambda: check_station(args.download)),
        ("pathway-selection", lambda: check_atlas("pathways", selections={"scenarioIndicator": "pr", "emissionScenario": "ssp245", "timeOfYear": "JJA"})),
        ("french-station", lambda: check_atlas("stations", language="fr", selections={"location": "BER"})),
        ("dropped-selection", check_dropped_selection),
    ]
    results = []
    for name, check in checks:
        record = {"check": name, "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
        try:
            record.update(status="passed", evidence=check())
        except Exception as exc:
            record.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        results.append(record)
        print(f"{name}: {record['status']}" + (f" — {record['error']}" if "error" in record else ""), flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    return int(any(r["status"] != "passed" for r in results))


if __name__ == "__main__":
    raise SystemExit(main())

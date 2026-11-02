"""Offline behavioural checks for station selection and file handling."""
import importlib.util
import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/ch2025/scripts/ch2025.py"
spec = importlib.util.spec_from_file_location("ch2025", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

def daily_csv():
    lines = ["TITLE;example", "CALENDAR;365_day", "UNIT;degrees_C",
             "STATION_ABBR;BER", "GWL;GWL3.0", "DATE;MODEL-A;MODEL-B"]
    day = dt.date(1, 1, 1)
    while day.year <= 30:
        if (day.month, day.day) != (2, 29):
            lines.append(f"{day.isoformat()};1.2;NA")
        day += dt.timedelta(days=1)
    return ("\n".join(lines) + "\n").encode()


CSV = daily_csv()
KEY = "ogd-climate-scenarios-ch2025_ber_tas_gwl3.0.csv"
ASSET = dict(asset=KEY, url="https://example.org/data.csv", format="csv", doi=helper.DOI,
             citation="MeteoSwiss & ETH Zurich (2025)")


class Response(io.BytesIO):
    def __init__(self, data, declared_length=None):
        super().__init__(data)
        self.headers = {"Content-Length": str(len(data) if declared_length is None else declared_length)}


class StationHelperTests(unittest.TestCase):
    def test_discovers_returned_asset_and_normalizes_station(self):
        with patch.object(helper, "fetch_json", return_value={"assets": {KEY: {"href": "https://example.org/actual.csv"}}}) as fetch:
            result = helper.station_asset("BER", "tas", "GWL3.0", "csv")
        self.assertEqual(result["url"], "https://example.org/actual.csv")
        self.assertTrue(fetch.call_args.args[0].endswith("/items/ber"))
        self.assertEqual(result["status"], "discovered")

    def test_missing_asset_does_not_invent_download(self):
        with patch.object(helper, "fetch_json", return_value={"assets": {}}):
            with self.assertRaisesRegex(ValueError, "Asset not available"):
                helper.station_asset("ber", "hurs", "gwl3.0", "csv")

    def test_download_retains_source_and_inspects_synthetic_dates(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(CSV)):
            record = helper.download(ASSET, tmp, 1_000_000)
            self.assertEqual(Path(record["path"]).read_bytes(), CSV)
            sidecar = json.loads(Path(record["provenance_path"]).read_text())
            self.assertEqual(sidecar["doi"], helper.DOI)
            self.assertEqual(sidecar["inspection"]["metadata"]["CALENDAR"], "365_day")
            self.assertEqual(sidecar["inspection"]["first_date"], "0001-01-01")
            self.assertEqual(sidecar["inspection"]["model_count"], 2)
            self.assertEqual(sidecar["inspection"]["rows"], 10950)
            self.assertEqual(sidecar["inspection"]["missing_cells"], 10950)
            self.assertEqual(sidecar["inspection"]["missing_by_model"], {"MODEL-A": 0, "MODEL-B": 10950})
            self.assertEqual(len(sidecar["sha256"]), 64)

    def test_existing_data_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / KEY
            path.write_bytes(b"existing")
            with patch.object(helper, "request") as request:
                with self.assertRaisesRegex(ValueError, "overwrite"):
                    helper.download(ASSET, tmp, 10000)
                request.assert_not_called()
            self.assertEqual(path.read_bytes(), b"existing")

    def test_declared_size_limit_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(CSV, 99999)):
            with self.assertRaisesRegex(ValueError, "exceeds"):
                helper.download(ASSET, tmp, 100)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_streamed_size_limit_cleans_partial_file(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(CSV, 0)):
            with self.assertRaisesRegex(ValueError, "exceeds"):
                helper.download(ASSET, tmp, 20)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_html_response_is_not_claimed_as_csv(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(b"<html>error</html>")):
            with self.assertRaisesRegex(ValueError, "DATE header missing"):
                helper.download(ASSET, tmp, 10000)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_ragged_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(b"CALENDAR;365_day\nDATE;M1;M2\n0001-01-01;1\n")):
            with self.assertRaisesRegex(ValueError, "Ragged"):
                helper.download(ASSET, tmp, 10000)

    def test_invalid_daily_products_leave_no_outputs(self):
        for raw, error in [
            (CSV[:CSV.index(b"0001-01-02")], "Incomplete daily CSV"),
            (CSV[:CSV.index(b"0001-01-01")], "Incomplete daily CSV"),
            (CSV.replace(b"0001-01-02", b"0001-01-03"), "Unexpected daily date"),
            (CSV.replace(b"1.2;NA", b"nan;NA", 1), "Non-finite"),
            (CSV.replace(b"MODEL-B", b"MODEL-A"), "duplicate model"),
            (CSV.replace(b"365_day", b"gregorian"), "365_day"),
        ]:
            with self.subTest(error=error), tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(raw)):
                with self.assertRaisesRegex(ValueError, error):
                    helper.download(ASSET, tmp, 1_000_000)
                self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_wrong_station_or_warming_level_is_rejected(self):
        for selection in ({"station": "lug"}, {"gwl": "gwl2.0"}):
            with self.subTest(selection=selection), tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(CSV)):
                with self.assertRaisesRegex(ValueError, "does not match"):
                    helper.download(dict(ASSET, **selection), tmp, 1_000_000)
                self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_content_length_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(CSV, len(CSV) + 1)):
            with self.assertRaisesRegex(ValueError, "Content-Length mismatch"):
                helper.download(ASSET, tmp, 1_000_000)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_provenance_write_failure_rolls_back_only_new_files(self):
        for concurrent in (False, True):
            with self.subTest(concurrent=concurrent), tempfile.TemporaryDirectory() as tmp:
                sidecar = Path(tmp) / (KEY + ".provenance.json")
                def fail_dump(*args, **kwargs):
                    raise OSError("disk full")
                def response(url):
                    if concurrent:
                        sidecar.write_text("other writer")
                    return Response(CSV)
                with patch.object(helper, "request", side_effect=response), patch.object(helper.json, "dump", side_effect=fail_dump):
                    with self.assertRaises(OSError):
                        helper.download(ASSET, tmp, 1_000_000)
                self.assertFalse((Path(tmp) / KEY).exists())
                if concurrent:
                    self.assertEqual(sidecar.read_text(), "other writer")
                else:
                    self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_zip_requires_netcdf_payloads(self):
        for members, valid in [([], False), ([("readme.txt", b"text")], False),
                               ([("model.nc", b"<html>error</html>")], False),
                               ([("model.nc", b"CDF\x01fixture")], True)]:
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as archive:
                for name, data in members:
                    archive.writestr(name, data)
            with self.subTest(members=members), tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(buffer.getvalue())):
                asset = dict(ASSET, asset="models.zip", format="zip")
                if valid:
                    record = helper.download(asset, tmp, 10000)
                    self.assertEqual(record["inspection"]["member_count"], 1)
                else:
                    with self.assertRaises(ValueError):
                        helper.download(asset, tmp, 10000)
                    self.assertEqual(list(Path(tmp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()

"""Offline behavioural checks for station selection and file handling."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/ch2025/scripts/ch2025.py"
spec = importlib.util.spec_from_file_location("ch2025", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

CSV = b"TITLE;example\nCALENDAR;365_day\nUNIT;degrees_C\n\nDATE;MODEL-A;MODEL-B\n0001-01-01;1.2;NA\n0001-01-02;2.3;4.5\n"
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
            record = helper.download(ASSET, tmp, 10000)
            self.assertEqual(Path(record["path"]).read_bytes(), CSV)
            sidecar = json.loads(Path(record["provenance_path"]).read_text())
            self.assertEqual(sidecar["doi"], helper.DOI)
            self.assertEqual(sidecar["inspection"]["metadata"]["CALENDAR"], "365_day")
            self.assertEqual(sidecar["inspection"]["first_date"], "0001-01-01")
            self.assertEqual(sidecar["inspection"]["model_count"], 2)
            self.assertEqual(sidecar["inspection"]["rows"], 2)
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
        with tempfile.TemporaryDirectory() as tmp, patch.object(helper, "request", return_value=Response(b"DATE;M1;M2\n0001-01-01;1\n")):
            with self.assertRaisesRegex(ValueError, "Ragged"):
                helper.download(ASSET, tmp, 10000)


if __name__ == "__main__":
    unittest.main()

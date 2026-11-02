"""Check that product discovery preserves selections and distinct data types."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from test_station_helper import helper, Response


def display(state):
    return {"componentGroups": [{"stateEntries": state}], "components": [
        {"type": "form", "value": {"elements": [{"attributeId": "region", "values": [{"value": "CH", "enabled": True}]}]}},
        {"type": "media", "value": {"realizations": [{"url": "https://example.org/realization", "mediaType": "text/csv", "sharedUrl": "https://example.org/selected"}]}},
        {"type": "info", "value": {"url": "https://example.org/product-help.md"}}]}


class DiscoveryTests(unittest.TestCase):
    def test_registry_covers_eight_distinct_official_atlas_families(self):
        registry = helper.products()
        self.assertEqual({p["key"] for p in registry}, {"maps", "altitude", "stations", "seasonal", "warming", "pathways", "annual-cycle", "ensemble"})
        self.assertEqual(len({p["display_id"] for p in registry}), 8)
        self.assertTrue(all(p["url"].startswith("https://www.meteoswiss.admin.ch/") for p in registry))

    def test_atlas_preserves_requested_and_returned_selection_and_help(self):
        with patch.object(helper, "fetch_json", return_value=display({"language": "en", "region": "CH", "productType": "data"})):
            result = helper.atlas_product("pathways", selections={"region": "CH"}, product_type="data")
        self.assertEqual(result["selected"]["region"], "CH")
        self.assertEqual(result["information_urls"], ["https://example.org/product-help.md"])
        self.assertEqual(result["realizations"][0]["sharedUrl"], "https://example.org/selected")
        self.assertEqual(result["status"], "discovered")

    def test_rejects_silently_substituted_global_warming_level(self):
        with patch.object(helper, "fetch_json", return_value=display({"language": "en", "globalWarmingLevel": "GWL1.5"})):
            with self.assertRaisesRegex(ValueError, "changed or dropped"):
                helper.atlas_product("maps", selections={"globalWarmingLevel": "GWL2.5"})

    def test_rejects_silently_dropped_station_in_aggregate_data_mode(self):
        with patch.object(helper, "fetch_json", return_value=display({"language": "en", "productType": "data"})):
            with self.assertRaisesRegex(ValueError, "location"):
                helper.atlas_product("stations", selections={"location": "BER"}, product_type="data")

    def test_rejects_plot_returned_instead_of_requested_data(self):
        with patch.object(helper, "fetch_json", return_value=display({"language": "en", "productType": "plot"})):
            with self.assertRaisesRegex(ValueError, "productType"):
                helper.atlas_product("ensemble", product_type="data")

    def test_station_name_lookup_uses_bom_and_official_columns(self):
        raw = '\ufeffstation_abbr;station_name;station_canton\nBER;Bern / Zollikofen;BE\nLUG;Lugano;TI\n'.encode()
        with patch.object(helper, "fetch_json", return_value={"assets": {"ogd_meta_stations.csv": {"href": "https://example.org/meta.csv"}}}), patch.object(helper, "request", return_value=Response(raw)):
            result = helper.station_catalogue("Bern")
        self.assertEqual([s["station_abbr"] for s in result["stations"]], ["BER"])
        self.assertEqual(result["metadata_url"], "https://example.org/meta.csv")

    def test_grid_discovery_filters_actual_model_asset_without_download(self):
        assets = {
            "ogd-climate-scenarios-ch2025-grid_ch_tas_model-a_gwl3.0.nc": {"href": "https://example.org/a.nc", "title": "a"},
            "ogd-climate-scenarios-ch2025-grid_ch_pr_model-a_gwl3.0.nc": {"href": "https://example.org/b.nc", "title": "b"},
            "ogd-climate-scenarios-ch2025-grid_ch_tas_model-b_gwl2.0.nc": {"href": "https://example.org/c.nc", "title": "c"}}
        with patch.object(helper, "fetch_json", return_value={"assets": assets}), patch.object(helper, "request") as request:
            result = helper.grid_assets("tas", "gwl3.0", "model-a")
            request.assert_not_called()
        self.assertEqual(len(result["assets"]), 1)
        self.assertEqual(result["assets"][0]["href"], "https://example.org/a.nc")


if __name__ == "__main__":
    unittest.main()

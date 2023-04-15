import unittest
from typing import Dict, Any


class FiveKTestCase(unittest.TestCase):
    cache_dir = ".cache"
    dataset_dir = ".cache/MITAboveFiveK"
    categories_labels = ["location", "time", "light", "subject"]

    def check_metadata(self, metadata: Dict[str, Any]):
        for value in metadata.values():
            assert 0 < len(value["files"]["dng"])
            for label in self.categories_labels:
                assert 0 < len(value["categories"][label])
            assert 0 < value["id"] <= 5000
            assert 0 < len(value["license"])

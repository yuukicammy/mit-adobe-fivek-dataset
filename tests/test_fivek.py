import os
import shutil
import unittest
from torch.utils.data.dataloader import DataLoader
from dataset.fivek import MITAboveFiveK
from tests.test_common import FiveKTestCase


class TestMITAboveFiveK(FiveKTestCase):
    def test_init(self):
        MITAboveFiveK(self.cache_dir, "debug")

    def test_init_with_download(self):
        MITAboveFiveK(self.cache_dir, "debug", download=True)

    def test_init_no_data(self):
        shutil.rmtree(self.dataset_dir)
        self.assertRaises(
            RuntimeError, MITAboveFiveK, self.cache_dir, "debug", download=False
        )

    def test___len__(self):
        assert MITAboveFiveK(self.cache_dir, "debug", download=True).__len__() == 9


class TestMITAboveFiveKWithDataLoader(FiveKTestCase):
    def test_load_with_dataloader(self):
        metadata_loader = DataLoader(
            MITAboveFiveK(self.cache_dir, "debug", download=True), batch_size=1
        )
        for metadata in metadata_loader:
            self.check_metadata(metadata)


if __name__ == "__main__":
    os.makedirs(FiveKTestCase.cache_dir, exist_ok=True)
    unittest.main()

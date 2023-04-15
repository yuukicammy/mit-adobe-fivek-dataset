import os
import shutil
import unittest
from torch.utils.data.dataloader import DataLoader
from fivek_dataset import MITAboveFiveK

cache_dir = ".cache"


class TestMITAboveFiveK(unittest.TestCase):
    def test_init(self):
        MITAboveFiveK(cache_dir, "debug")

    def test_init_with_download(self):
        MITAboveFiveK(cache_dir, "debug", download=True)

    def test_init_no_data(self):
        shutil.rmtree(os.path.join(cache_dir, "MITAboveFiveK"))
        self.assertRaises(
            RuntimeError, MITAboveFiveK, cache_dir, "debug", download=False
        )

    def test___len__(self):
        assert MITAboveFiveK(cache_dir, "debug", download=True).__len__() == 9


class TestMITAboveFiveKWithDataLoader(unittest.TestCase):
    def test_load_with_dataloader(self):
        data_loader = DataLoader(
            MITAboveFiveK(cache_dir, "debug", download=True), batch_size=1
        )
        data = next(iter(data_loader))
        assert 0 < len(data["files"]["dng"])


if __name__ == "__main__":
    os.makedirs(cache_dir, exist_ok=True)
    unittest.main()

"""
    Copyright (c) 2023 yuukicammy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
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
        MITAboveFiveK(self.cache_dir,
                      "debug",
                      download=True,
                      download_workers=self.download_workers)

    def test_init_no_data(self):
        shutil.rmtree(self.dataset_dir)
        self.assertRaises(RuntimeError,
                          MITAboveFiveK,
                          self.cache_dir,
                          "debug",
                          download=False)

    def test_init_with_data(self):
        MITAboveFiveK(self.cache_dir,
                      "debug",
                      download=True,
                      download_workers=self.download_workers)
        MITAboveFiveK(self.cache_dir, "debug", download=False)

    def test___len__(self):
        assert MITAboveFiveK(
            self.cache_dir,
            "debug",
            download=True,
            download_workers=self.download_workers).__len__() == 9


class TestMITAboveFiveKWithDataLoader(FiveKTestCase):

    def test_load_with_dataloader(self):
        metadata_loader = DataLoader(
            MITAboveFiveK(self.cache_dir, "debug", download=True),
            batch_size=None,
        )
        for metadata in metadata_loader:
            self.check_metadata({metadata["basename"]: metadata})


if __name__ == "__main__":
    os.makedirs(FiveKTestCase.cache_dir, exist_ok=True)
    unittest.main()

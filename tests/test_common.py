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
import unittest
from typing import Dict, Any


class FiveKTestCase(unittest.TestCase):
    cache_dir = ".cache"
    dataset_dir = ".cache/MITAboveFiveK"
    categories_labels = ["location", "time", "light", "subject"]
    num_workers = 4

    def check_metadata(self, metadata: Dict[str, Any]):
        for value in metadata.values():
            assert 0 < len(value["files"]["dng"])
            for label in self.categories_labels:
                assert 0 < len(value["categories"][label])
            assert 0 < value["id"] <= 5000
            assert 0 < len(value["license"])

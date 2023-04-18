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
from tests.test_common import FiveKTestCase
from dataset.fivek_builder import MITAboveFiveKBuilder


class TestMITAboveFiveKBuilderInit(FiveKTestCase):

    def test_init_all(self):
        for config in MITAboveFiveKBuilder.BUILDER_CONFIGS:
            MITAboveFiveKBuilder(self.dataset_dir, config_name=config.name)
            shutil.rmtree(self.cache_dir)

    def test_init_wrong_config(self):
        self.assertRaises(
            ValueError,
            MITAboveFiveKBuilder,
            self.dataset_dir,
            config_name="wrong_config",
        )


class TestMITAboveFiveKBuilderBuild(FiveKTestCase):

    def test_build_wrong_split(self):
        shutil.rmtree(self.cache_dir)
        for config in MITAboveFiveKBuilder.BUILDER_CONFIGS:
            builder = MITAboveFiveKBuilder(self.dataset_dir,
                                           config_name=config.name)
            self.assertRaises(ValueError, builder.build, "wrong")

    def test_per_camera_model_build_debug(self):
        shutil.rmtree(self.cache_dir)
        builder = MITAboveFiveKBuilder(self.dataset_dir,
                                       config_name="per_camera_model")
        res = builder.build(split="debug", num_workers=self.num_workers)
        assert len(res.keys()) == 9
        self.check_metadata(res)


class TestMITAboveFiveKBuilderPath(FiveKTestCase):

    def test_raw_file_path_archive(self):
        expected = os.path.join(
            self.cache_dir,
            "MITAboveFiveK",
            "raw",
            "fivek_dataset",
            "raw_photos",
            "HQa1to700",
            "photos",
            "a0298-IMG_5043.dng",
        )
        actual = MITAboveFiveKBuilder(
            os.path.join(self.cache_dir, "MITAboveFiveK"),
            config_name="archive").raw_file_path("a0298-IMG_5043")
        assert expected == actual

    def test_raw_file_path_per_camera_model(self):
        expected = os.path.join(
            self.dataset_dir,
            "raw",
            "Canon_EOS_450D",
            "a0298-IMG_5043.dng",
        )
        builder = MITAboveFiveKBuilder(self.dataset_dir,
                                       config_name="per_camera_model")
        builder.build(split="debug", num_workers=self.num_workers)
        actual = builder.raw_file_path("a0298-IMG_5043")
        assert expected == actual

    def test_expert_path(self):
        expected = os.path.join(self.dataset_dir, "processed", "tiff16_e",
                                "a0298-IMG_5043.tif")
        for config in MITAboveFiveKBuilder.BUILDER_CONFIGS:
            builder = MITAboveFiveKBuilder(
                self.dataset_dir,
                config_name=config.name,
                experts=["e"],
            )
            builder.build(split="debug", num_workers=self.num_workers)
            actual = builder.expert_file_path("a0298-IMG_5043", "e")
            assert expected == actual


class TestMITAboveFiveKBuilderMetadata(FiveKTestCase):

    def test_metadata_archive_debug(self):
        builder = MITAboveFiveKBuilder(self.dataset_dir, "archive")
        metadata = builder.build("debug")
        assert len(metadata.keys()) == 9
        self.check_metadata(metadata)

    # def test_metadata_archive_all(self):
    #     builder = MITAboveFiveKBuilder(os.path.join("..", "MITAboveFiveK"), "archive")
    #     metadata = builder.metadata()
    #     assert len(metadata.keys()) == 5000
    #     self.check_metadata(metadata)


if __name__ == "__main__":
    os.makedirs(FiveKTestCase.cache_dir, exist_ok=True)
    unittest.main()

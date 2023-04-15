import os
import shutil
import unittest
from fivek_dataset_builder import MITAboveFiveKBuilder

cache_dir = ".cache"


def check_metadata(metadata):
    categories_labels = ["location", "time", "light", "subject"]
    for value in metadata.values():
        assert 0 < len(value["files"]["dng"])
        for label in categories_labels:
            assert 0 < len(value["categories"][label])
        assert 0 < value["id"] <= 5000
        assert 0 < len(value["license"])


class TestMITAboveFiveKBuilderInit(unittest.TestCase):
    def test_init_all(self):
        for config in MITAboveFiveKBuilder.BUILDER_CONFIGS:
            MITAboveFiveKBuilder(
                os.path.join(cache_dir, "MITAboveFiveK"), config_name=config.name
            )
            shutil.rmtree(cache_dir)

    def test_init_wrong_config(self):
        self.assertRaises(
            ValueError,
            MITAboveFiveKBuilder,
            os.path.join(cache_dir, "MITAboveFiveK"),
            config_name="wrong_config",
        )


class TestMITAboveFiveKBuilderBuild(unittest.TestCase):
    def test_build_wrong_split(self):
        shutil.rmtree(cache_dir)
        for config in MITAboveFiveKBuilder.BUILDER_CONFIGS:
            builder = MITAboveFiveKBuilder(
                os.path.join(cache_dir, "MITAboveFiveK"), config_name=config.name
            )
            self.assertRaises(ValueError, builder.build, "wrong")

    def test_per_camera_model_build_debug(self):
        shutil.rmtree(cache_dir)
        builder = MITAboveFiveKBuilder(
            os.path.join(cache_dir, "MITAboveFiveK"), config_name="per_camera_model"
        )
        res = builder.build(split="debug")
        assert len(res.keys()) == 9
        check_metadata(res)


class TestMITAboveFiveKBuilderPath(unittest.TestCase):
    def test_raw_file_path_archive(self):
        expected = os.path.join(
            cache_dir,
            "MITAboveFiveK",
            "raw",
            "fivek_dataset",
            "raw_photos",
            "HQa1to700",
            "photos",
            "a0298-IMG_5043.dng",
        )
        actual = MITAboveFiveKBuilder(
            os.path.join(cache_dir, "MITAboveFiveK"), config_name="archive"
        ).raw_file_path("a0298-IMG_5043")
        assert expected == actual

    def test_raw_file_path_per_camera_model(self):
        expected = os.path.join(
            cache_dir,
            "MITAboveFiveK",
            "raw",
            "Canon_EOS_450D",
            "a0298-IMG_5043.dng",
        )
        builder = MITAboveFiveKBuilder(
            os.path.join(cache_dir, "MITAboveFiveK"), config_name="per_camera_model"
        )
        builder.build("debug")
        actual = builder.raw_file_path("a0298-IMG_5043")
        assert expected == actual

    def test_expert_path(self):
        expected = os.path.join(
            cache_dir, "MITAboveFiveK", "processed", "tiff16_e", "a0298-IMG_5043.tif"
        )
        for config in MITAboveFiveKBuilder.BUILDER_CONFIGS:
            builder = MITAboveFiveKBuilder(
                os.path.join(cache_dir, "MITAboveFiveK"),
                config_name=config.name,
                experts=["e"],
            )
            builder.build("debug")
            actual = builder.expert_file_path("a0298-IMG_5043", "e")
            assert expected == actual


class TestMITAboveFiveKBuilderMetadata(unittest.TestCase):
    def test_metadata_archive_debug(self):
        builder = MITAboveFiveKBuilder(
            os.path.join(cache_dir, "MITAboveFiveK"), "archive"
        )
        metadata = builder.build("debug")
        assert len(metadata.keys()) == 9
        check_metadata(metadata)

    def test_metadata_archive_all(self):
        builder = MITAboveFiveKBuilder(os.path.join("..", "MITAboveFiveK"), "archive")
        metadata = builder.metadata()
        assert len(metadata.keys()) == 5000
        check_metadata(metadata)


if __name__ == "__main__":
    os.makedirs(cache_dir, exist_ok=True)
    unittest.main()

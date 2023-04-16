"""
Script to generate a json files describing the MIT-Adobe FiveK Dataset \
    items from the data downloaded and extracted from the archive.

Usage:
    python generate_dataset_json.py [-h] dir_root camera_models train_ratio val_ratio

Arguments:
    dir_root Path of the root directory where the tar file was extracted. \
            The program generats `training.json`, `validation.json`, and `testing.json` files \
            and stores in this directory.
    camera_models  Path of the csv file listing a file id and its camera information.
    train_ratio    Percentage of data used for `training` out of total data.
    vaL_ratio    Percentage of data used for `validation` out of total data.

Example:
    python generate_dataset_json.py  ../data/MITAboveFiveK ../data/camera_models.csv 0.7 0.1

Note:
    Please see the official website for more information.
    MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>
"""

import os
import argparse
from typing import List, Dict, Any
import rawpy
from torch.utils.data.dataloader import DataLoader
from PIL import Image
from dataset.fivek import MITAboveFiveK


def main():
    parser = argparse.ArgumentParser(
        description="Develop and save raw images of the FiveK dataset using RawPy."
    )
    parser.add_argument(
        "root_dir",
        type=str,
        default=".cache",
        help="Path of the root directory where the directory 'MITAboveFiveK' exists.",
    )
    parser.add_argument(
        "--to_dir",
        type=str,
        default=None,
        required=False,
        help="Path to a directory to save developed images. If None, save to `root_dir`/MITAboveFiveK/processed/sRGB/.",
    )

    args = parser.parse_args()
    if not args.to_dir:
        args.to_dir = os.path.join(args.root_dir, "MITAboveFiveK", "processed", "sRGB")
    os.makedirs(args.to_dir, exist_ok=True)

    metadata_loader = DataLoader(
        MITAboveFiveK(root=args.root_dir, split="debug"),
        batch_size=None,
        num_workers=2,
    )
    for item in metadata_loader:
        # Some kind of process using FiveK
        raw = rawpy.imread(item["files"]["dng"])
        srgb = raw.postprocess()
        Image.fromarray(srgb).save(
            os.path.join(args.to_dir, f"{item['basename']}.jpeg")
        )


if __name__ == "__main__":
    main()

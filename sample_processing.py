"""Sample Processing with MITAboveFiveK

Script to convert RAW images of MIT-Above FiveK Dataset to 8-bit sRGB with RawPy.

Usage:
    python sample_processing.py [-h] dir_root

Arguments:
    [Positional]
    dir_root    Path of the root directory where the directory 'MITAboveFiveK' exists.
    
    [Options]
    --to_dir    Path to a directory to save developed images. If None, save to `root_dir`/MITAboveFiveK/processed/sRGB/.
    -h, --help  Show the help message and exit.

Example:
    python sample_processing.py  ./data/MITAboveFiveK 

Note:
    Please see the official website for more information.
    MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>
"""

import os
import argparse
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

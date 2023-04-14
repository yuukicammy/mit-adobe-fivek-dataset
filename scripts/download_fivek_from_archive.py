"""
Script to download the MIT-Adobe FiveK Dataset from tar archive.
The MIT-Adobe FiveK Dataset is a collection that includes the following items:
    1) 5,000 raw images in DNG format,
    2) 5,000 retouched images in TIFF format,
    3) semantic information about each image.
This script downloads the dataset and extracts it.

Usage:
    python download_fivek_from_archive.py [-h] root [{A,B,C,D,E} ...]

Arguments:
  root         Root directory where the dataset will be downloaded and extracted. The data will be saved under `<root>/MITAboveFiveK/raw`. 
  {A,B,C,D,E}  List of experts who adjusted tone of the photos to download. Experts are 'A', 'B', 'C', 'D', and/or 'E'.

Example:
    python download_fivek_from_archive.py ../data A

Note:
    Please see the official website for more information.
    MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>
"""

import argparse
import sys
sys.path.append('../')
from fivek_dataset_builder import MITAboveFiveKBuilder

def main():

    parser = argparse.ArgumentParser(
        description="Download the MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>."
    )
    parser.add_argument(
        "root",
        type=str,
        help="Root directory where the dataset will be downloaded and extracted. The data will be saved under `<root>/MITAboveFiveK/raw`.",
    )
    parser.add_argument(
        "experts",
        nargs="*",
        choices=["a", "b", "c", "d", "e", []],
        help="List of experts who adjusted tone of the photos to download. Experts are 'a', 'b', 'c', 'd', and/or 'e'.",
        default=None,
    )
    args = parser.parse_args()
    builder = MITAboveFiveKBuilder(
        dataset_dir=args.root, config_name="archive", experts=args.experts
    )
    builder.build()


if __name__ == "__main__":
    main()

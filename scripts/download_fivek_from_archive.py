"""
Script to download the MIT-Adobe FiveK Dataset from tar archive.
The MIT-Adobe FiveK Dataset is a collection that includes the following items:
    1) 5,000 raw images in DNG format,
    2) 5,000 retouched images in TIFF format,
    3) semantic information about each image.
This script downloads the dataset and extracts it.

Usage:
    python download_fivek_from_archive.py [-h] root [{a,b,c,d,e} ...]

Arguments:
  root         Root directory. The data will be saved under `<root>/MITAboveFiveK/raw`. 
  {a,b,c,d,e}  List of experts who adjusted tone of the photos to download. Experts are 'a', 'b', 'c', 'd', and/or 'e'.

Example:
    python download_fivek_from_archive.py ../data a

Note:
    Please see the official website for more information.
    MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>

License:
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
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dataset.fivek_builder import MITAboveFiveKBuilder


def main():
    parser = argparse.ArgumentParser(
        description=
        "Download the MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>."
    )
    parser.add_argument(
        "dir",
        type=str,
        help=
        "A directory where the dataset will be downloaded and extracted. The data will be saved under `<root>/MITAboveFiveK/raw`.",
    )
    parser.add_argument(
        "--experts",
        nargs="*",
        choices=["a", "b", "c", "d", "e"],
        help=
        "List of experts who adjusted tone of the photos to download. Experts are 'a', 'b', 'c', 'd', and/or 'e'.",
        default=None,
    )
    args = parser.parse_args()
    builder = MITAboveFiveKBuilder(dataset_dir=args.dir,
                                   config_name="archive",
                                   experts=args.experts)
    builder.build()


if __name__ == "__main__":
    main()

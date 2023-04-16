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
    python sample_processing.py  ./data

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
import argparse
import rawpy
from torch.utils.data.dataloader import DataLoader
from PIL import Image
from dataset.fivek import MITAboveFiveK


def main():
    parser = argparse.ArgumentParser(
        description=
        "Develop and save raw images of the FiveK dataset using RawPy.")
    parser.add_argument(
        "root_dir",
        type=str,
        default=".cache",
        help=
        "Path of the root directory where the directory 'MITAboveFiveK' exists.",
    )
    parser.add_argument(
        "--to_dir",
        type=str,
        default=None,
        required=False,
        help=
        "Path to a directory to save developed images. If None, save to `root_dir`/MITAboveFiveK/processed/sRGB/.",
    )

    args = parser.parse_args()
    if not args.to_dir:
        args.to_dir = os.path.join(args.root_dir, "MITAboveFiveK", "processed",
                                   "sRGB")
    os.makedirs(args.to_dir, exist_ok=True)

    data_loader = DataLoader(
        MITAboveFiveK(root=args.root_dir, split="debug"),
        batch_size=None,
        num_workers=2,  # multi-processing
    )
    for item in data_loader:
        # Some kind of process using FiveK
        raw = rawpy.imread(item["files"]["dng"])
        srgb = raw.postprocess()
        Image.fromarray(srgb).save(
            os.path.join(args.to_dir, f"{item['basename']}.jpeg"))


if __name__ == "__main__":
    main()

"""
Script to generate a json files describing the MIT-Adobe FiveK Dataset 
items from the data downloaded and extracted from the archive.

Usage:
    python generate_dataset_json.py [-h] dir_root camera_models train_ratio val_ratio

Arguments:
    dir_root        Path of the root directory where the tar file was extracted. 
                    The program generats `training.json`, `validation.json`, 
                    and `testing.json` files and stores in this directory.
    camera_models   Path of the csv file listing a file id and its camera information.
    train_ratio     Percentage of data used for `training` out of total data.
    vaL_ratio       Percentage of data used for `validation` out of total data.

Example:
    python generate_dataset_json.py  ../data/MITAboveFiveK ../data/camera_models.csv 0.7 0.1

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
from typing import List, Dict, Any
import json
import csv
import random
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dataset.fivek_builder import MITAboveFiveKBuilder

random.seed(42)


def load_list(filepath: str, encoding: str = "ascii") -> List[str]:
    """
    Args:
        filepath (str): Text file to be read.
        encoding (str, optional): Encording of the file. Defaults to 'ascii'.

    Returns:
        List[str]: Returns a list with a single line of a text file as an element.
    """
    list_ = []
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding=encoding) as file:
            list_ = list(map(lambda s: s.rstrip("\n"), file.readlines()))
    return list_


def load_camera_info(filepath: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """Load camera information of each image

    Args:
        filepath (str): Path to the CSV file containing the camera information corresponding to each image.
        encoding (str, optional): Encording of the file. Defaults to 'utf-8'.

    Returns:
        Dict[str, Any]: A dictionary that can refer to camera information from each image name.
    """
    camera_info = {}
    if os.path.isfile(filepath):
        with open(filepath, newline="", encoding=encoding) as csvfile:
            header = next(csv.reader(csvfile))
            reader = csv.reader(csvfile)
            for row in reader:
                camera_info[row[0]] = {}
                for i in range(1, len(row)):
                    camera_info[row[0]][header[i]] = row[i]
    return camera_info


def extract_id(fid: str) -> int:
    return int(fid.split("-")[0][1:])


def split_list(list: List[Any], ratios: List[float]) -> List[List[Any]]:
    random.shuffle(list)
    splitted = []
    n_data = len(list)
    sum_ratio = sum(ratios)
    n_curr = 0
    for ratio in ratios[:len(ratios) - 1]:
        ratio /= sum_ratio
        n = int(ratio * n_data)
        splitted.append(list[n_curr:n_curr + n])
        n_curr += n
    splitted.append(list[n_curr:])
    return splitted


def main():
    parser = argparse.ArgumentParser(
        description=
        "Generate a json file describing items of MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>."
    )
    parser.add_argument(
        "root_dir",
        type=str,
        default="../MITAboveFiveK",
        help="Path of the root directory where the tar file was extracted.",
    )
    parser.add_argument(
        "camera_models",
        type=str,
        default="./camera_models.csv",
        help=
        "Path of the csv file listing a file id and its camera information.",
    )
    parser.add_argument(
        "train_ratio",
        type=float,
        default=0.7,
        help="Percentage of data used for `training` out of total data.",
    )
    parser.add_argument(
        "val_ratio",
        type=float,
        default=0.1,
        help="Percentage of data used for `validation` out of total data.",
    )

    args = parser.parse_args()
    if args.train_ratio + args.val_ratio > 0.99:
        print(
            "Please set `train_ratio` and `val_ratio` to be less than 0.99. ")

    builder = MITAboveFiveKBuilder(dataset_dir=args.root_dir,
                                   config_name="archive")
    metadata = builder.build()

    files_license = {}
    for fid in load_list(
            os.path.join(builder.dataset_dir, "raw", "fivek_dataset",
                         "filesAdobeMIT.txt")):
        files_license[fid] = "AdobeMIT"
    for fid in load_list(
            os.path.join(builder.dataset_dir, "raw", "fivek_dataset",
                         "filesAdobe.txt")):
        files_license[fid] = "Adobe"

    camera_info = load_camera_info(args.camera_models)

    for name, value in metadata.items():
        value["id"] = extract_id(name)
        value["license"] = files_license[name]
        value["urls"] = {
            "dng":
            f"http://data.csail.mit.edu/graphics/fivek/img/dng/{name}.dng",
            "tiff16": {},
        }
        for expert in ["a", "b", "c", "d", "e"]:
            value["urls"]["tiff16"][
                expert] = f"http://data.csail.mit.edu/graphics/fivek/img/tiff16_{expert}/{name}.tif"
        value["camera"] = {
            "make": camera_info[name]["make"],
            "model": camera_info[name]["model"],
        }
        del value["files"]

    ratios = [
        args.train_ratio, args.val_ratio,
        (1 - args.train_ratio - args.val_ratio)
    ]
    splitted_basenames = split_list(list=list(metadata.keys()), ratios=ratios)
    for phase, basenames in zip(["training", "validation", "testing"],
                                splitted_basenames):
        filepath = os.path.join(builder.dataset_dir, f"{phase}.json")
        partial = {}
        for name in basenames:
            partial[name] = metadata[name]
        with open(filepath, "w", encoding="utf-8") as outfile:
            json.dump(partial, outfile)


if __name__ == "__main__":
    main()

"""
Script to generate a json file describing the MIT-Adobe FiveK Dataset \
    items from the data downloaded and extracted from the archive.

Usage:
    python generate_dataset_json.py [-h] filepath dir_root

Arguments:
  filepath  Path to save the generated json file.
  dir_root  Path of the root directory where the tar file was extracted.

Example:
    python generate_dataset_json.py ../data/fivek_all.json ../data

Note:
    Please see the official website for more information.
    MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>
"""

import os
import argparse
from typing import List, Dict, Any
import json
import csv
from mit_adobe_fivek import MITAboveFiveK


def load_list(filepath: str, encoding: str = 'ascii') -> List[str]:
    """
    Args:
        filepath (str): Text file to be read.
        encoding (str, optional): Encording of the file. Defaults to 'ascii'.

    Returns:
        List[str]: Returns a list with a single line of a text file as an element.
    """
    list_ = []
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding=encoding) as file:
            list_ = list(map(lambda s: s.rstrip("\n"), file.readlines()))
    return list_


def load_camera_info(filepath: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """Load camera information of each image

    Args:
        filepath (str): Path to the CSV file containing the camera information corresponding to each image.
        encoding (str, optional): Encording of the file. Defaults to 'utf-8'.

    Returns:
        Dict[str, Any]: A dictionary that can refer to camera information from each image name.
    """
    camera_info = {}
    if os.path.isfile(filepath):
        with open(filepath, newline='', encoding=encoding) as csvfile:
            header = next(csv.reader(csvfile))
            reader = csv.reader(csvfile)
            for row in reader:
                camera_info[row[0]] = {}
                for i in range(1, len(row)):
                    camera_info[row[0]][header[i]] = row[i]
    return camera_info


def extract_id(fid: str) -> int:
    return int(fid.split("-")[0][1:])


def main():

    parser = argparse.ArgumentParser(
        description=
        'Generate a json file describing items of MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>.'
    )
    parser.add_argument('filepath',
                        type=str,
                        default='all.json',
                        help='Path to save the generated json file.')
    parser.add_argument(
        'root_dir',
        type=str,
        default='../',
        help='Path of the root directory where the tar file was extracted.')
    parser.add_argument(
        'camera_models',
        type=str,
        default='./camera_models.csv',
        help=
        'Path of the csv file listing a file id and its camera information.')

    args = parser.parse_args()
    fivek = MITAboveFiveK(args.root_dir, False)

    files_license = {}
    for fid in load_list(
            os.path.join(fivek.raw_dir, 'fivek_dataset', 'filesAdobeMIT.txt')):
        files_license[fid] = 'AdobeMIT'
    for fid in load_list(
            os.path.join(fivek.raw_dir, 'fivek_dataset', 'filesAdobe.txt')):
        files_license[fid] = 'Adobe'

    category_label = fivek.category_types

    camera_info = load_camera_info(args.camera_models)

    alldata = {}
    for fid in fivek.file_ids:
        data = {}
        data['id'] = extract_id(fid)
        data['license'] = files_license[fid]
        data['urls'] = {
            'dng':
            f'http://data.csail.mit.edu/graphics/fivek/img/dng/{fid}.dng',
            'tiff16': {}
        }
        for expert in ['a', 'b', 'c', 'd', 'e']:
            data['urls']['tiff16'][
                expert] = f'http://data.csail.mit.edu/graphics/fivek/img/tiff16_{expert}/{fid}.tif'
        data['categories'] = {}
        categories = fivek.file_categories(fid)
        for i in range(4):
            data['categories'][category_label[i]] = categories[i]
        data['camera'] = {
            'make': camera_info[fid]['make'],
            'model': camera_info[fid]['model']
        }
        alldata[fid] = data
    with open(args.filepath, 'w', encoding='utf-8') as outfile:
        json.dump(alldata, outfile)


if __name__ == '__main__':
    main()

"""
Script to generate a json file describing the MIT-Adobe FiveK Dataset \
    items from the data downloaded and extracted from the archive.

Usage:
    python generate_base_json.py [-h] filepath dir_root

Arguments:
  filepath  Path to save the generated json file.
  dir_root  Path of the root directory where the tar file was extracted.

Example:
    python generate_base_json.py ./fivek_all.json ../MITAdobeFiveK/raw/

Note:
    Please see the official website for more information.
    MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>
"""

import os
import argparse
from typing import List, Dict, Tuple
from mit_adobe_fivek import MITAboveFiveK


def load_list(filepath: str, encoding: str = 'ascii') -> List[str]:
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding=encoding) as file:
            return list(map(lambda s: s.rstrip("\n"), file.readlines()))
    else:
        return []


def extract_id(fid: str) -> int:
    return int(fid.split("-")[0][1:])


def main():

    parser = argparse.ArgumentParser(
        description=
        'Generate a json file describing items of MIT-Adobe FiveK Dataset <https://data.csail.mit.edu/graphics/fivek/>.'
    )
    parser.add_argument('filepath',
                        type=str,
                        help='Path to save the generated json file.')
    parser.add_argument(
        'root_dir',
        type=str,
        help='Path of the root directory where the tar file was extracted.')

    args = parser.parse_args()
    fivek = MITAboveFiveK(args.root_dir, False)

    files_license = {'AdobeMIT': [], 'Adobe': []}
    files_license['AdobeMIT'] = load_list(
        os.path.join(fivek.raw_dir, 'fivek_dataset', 'filesAdobeMIT.txt'))
    files_license['Adobe'] = load_list(
        os.path.join(fivek.raw_dir, 'fivek_dataset', 'filesAdobe.txt'))

    for fid in fivek.file_ids[:3]:
        with open(args.filepath, 'a+', encoding='utf-8') as outfile:
            data = {}
            data['baseName'] = fid
            data['id'] = extract_id(fid)
            data['license'] = 'AdobeMIT' if fid in files_license[
                'AdobeMIT'] else 'Adobe'
            outfile.write(data)


if __name__ == '__main__':
    main()

"""`MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset.

The MIT-Adobe FiveK Dataset is a collection that includes the following items:
    1) 5,000 raw images in DNG format,
    2) 5,000 retouched images in TIFF format,
    3) semantic information about each image.

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
from typing import List, Dict, Any, Callable
from torch.utils.data import Dataset
from dataset.fivek_builder import MITAboveFiveKBuilder


class MITAboveFiveK(Dataset):
    """`MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset.

    Args:
            root (str): 
                The root directory where the 'MITAboveFiveK' directory exists or to be created.
            split (str): 
                One of {'train', 'val', 'test', 'debug'}. 'debug' uses only 9 data contained in 'train'.
            download (bool): 
                If True, downloads the dataset from the official urls. Files that already exist locally will skip the download. 
                Defaults to False.
            experts (List[str]): 
                List of {'a', 'b', 'c', 'd', 'e'}. 'a' means 'Expert A' in the website <https://data.csail.mit.edu/graphics/fivek/>. 
                Defaults to None.
            download_workers (int):  
                How many subprocesses to use for data downloading.
                None means that min(32, cpu_count() + 4). Defaults to 1.
            process_fn ([[Dict[str, Any]], Any]): 
                Function of the processing to be performed on each element of the dataset.
                This function applied in __getitem__().
                Defaults to None.

    Notes:
            Expects the following folder structure if download=False:
            .. code::
                <root>
                └── MITAboveFiveK
                    ├─ raw
                    |   ├── Canon_EOS-1D_Mark_II
                    |   |   ├── a1527-20041010_072954__E6B5620.dng
                    |   |   └── ...
                    |   ...
                    |   └── Sony_DSLR-A900
                    |       ├── 4337-kme_1082.dng
                    |       └── ...
                    ├── processed
                    |   ├── tiff16_a
                    |   |   ├── a0001-jmac_DSC1459.tif
                    |   |   └── ...
                    |   ├── tiff16_b
                    |   └── ...
                    ├── training.json
                    ├── validation.json
                    ├── testing.json
                    └── debugging.json
    Raises:
            ValueError: If the value of split is not one of {'train', 'val', 'test', 'debug'}.
            RuntimeError: If dataset not found, or download failed.
    """

    def __init__(self,
                 root: str,
                 split: str,
                 download: bool = False,
                 experts: List[str] = None,
                 download_workers: int = 1,
                 process_fn: Callable[[Dict[str, Any]], Any] = None) -> None:
        # root directory of datasets
        self.root = root

        # One of {'train', 'val', 'test'}
        split = split.lower()
        if split not in ["train", "val", "test", "debug"]:
            raise ValueError(
                f"Invalid split: {split}. `split` must be one of {'train', 'val', 'test', 'debug'}."
            )
        self.split = split
        self.process_fn = process_fn

        # list of 'a', 'b', 'c', 'd', and/or 'e'
        self.experts = []
        if experts:
            for e in experts:
                e = e.lower()
                if e in ["a", "b", "c", "d", "e"]:
                    self.experts.append(e)

        if download:
            self.metadata = MITAboveFiveKBuilder(
                dataset_dir=self.dataset_dir,
                config_name="per_camera_model",
                experts=self.experts,
            ).build(split=self.split, num_workers=download_workers)
        else:
            self.metadata = MITAboveFiveKBuilder(
                dataset_dir=self.dataset_dir,
                config_name="per_camera_model",
                experts=self.experts,
            ).metadata(split=self.split)
        self.keys_list = list(self.metadata.keys())

        if not self._check_exists():
            raise RuntimeError(
                "Dataset not found. You can use download=True to download it. "
                "This error also occurs when download=True but the download did not complete. "
                "Initializing the instance with download=True again, then downloading only files that have not been downloaded yet."
            )

    def __getitem__(self, index: int) -> Dict[str, Any]:
        item = self.metadata[self.keys_list[index]]
        item["basename"] = self.keys_list[index]
        if self.process_fn:
            return self.process_fn(item)
        del item["urls"]
        return item

    def __len__(self):
        return len(self.keys_list)

    def _check_exists(self) -> bool:
        if len(self.metadata) == 0:
            return False
        for basename in self.metadata.keys():
            if not os.path.isfile(self.metadata[basename]["files"]["dng"]):
                return False
            for e in self.experts:
                if not os.path.isfile(
                        self.metadata[basename]["files"]["tiff16"][e]):
                    return False
        return True

    @property
    def dataset_dir(self) -> str:
        return os.path.join(self.root, self.__class__.__name__)

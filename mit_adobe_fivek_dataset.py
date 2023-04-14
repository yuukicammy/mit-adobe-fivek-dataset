"""`MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset.

The MIT-Adobe FiveK Dataset is a collection that includes the following items:
    1) 5,000 raw images in DNG format,
    2) 5,000 retouched images in TIFF format,
    3) semantic information about each image.
"""
from typing import List, Dict, Tuple, Optional, Callable
import os
import json
from torchvision.datasets import VisionDataset

from fivek_dataset_builder import MITAboveFiveKBuilder

class MITAboveFiveK(VisionDataset):
    """`MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset.

    Args:
        root (string): Root directory in which MITAboveFiveK directory to be created.
        
            Expects the following folder structure if download=False:
            .. code::
                <root>
                └── MITAboveFiveK
                    └─ raw
                        ├── Canon_EOS-1D_Mark_II
                            ├── a1527-20041010_072954__E6B5620.dng
                            └── ...
                        ...
                        ├── Sony_DSLR-A900
                            ├── 4337-kme_1082.dng
                            └── ...
                    └── processed
                        ├── tiff16_a
                        |   ├── a0001-jmac_DSC1459.tif
                        |   └── ...
                        ├── tiff16_b
                        └── ...
                    └── train.json
                    └── test.json
        train (bool, optional): If True, creates dataset from training set, otherwise
            creates from test set.
        transform (callable, optional): A function/transform that takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
        experts (List[str], optional): List of experts to download. Experts are 'a', 'b', 'c', 'd', and/or 'e'.
            'a' means 'Expert A' in the website <https://data.csail.mit.edu/graphics/fivek/>.
            If None, no expert data will be downloaded.
    Raises:
        RuntimeError: Error rises if dataset does not exist or the download failed.
    """

    train_file = 'train.json'
    test_file = 'test.json'

    def __init__(self,
                 root: str,
                 train: bool = True,
                 transform: Optional[Callable] = None,
                 target_transform: Optional[Callable] = None,
                 download: bool = False,
                 experts: List[str] = None) -> None:

        super().__init__(root,
                         transform=transform,
                         target_transform=target_transform)

        # root directory of datasets
        self.root = root

        # training set or test set
        self.train = train

        # list of 'a', 'b', 'c', 'd', and/or 'e'
        self.experts = []
        for e in experts:
            e = e.lower()
            if e in ['a', 'b', 'c', 'd', 'e']:
                self.experts.append(e)

        self.data_file = os.path.join(
            self.dataset_dir, self.train_file if train else self.test_file)

        if download:
            self.metadata = MITAboveFiveKBuilder(root=self.root, config_name='per_camera_model', experts=self.experts, json_path=self.data_file).build()
        else:
            self.metadata = MITAboveFiveKBuilder(root=self.root, config_name='per_camera_model', experts=self.experts, json_path=self.data_file).metadata()
    
    def _check_exists(self) -> bool:
        for basename in self.metadata.keys():
            if not os.path.isfile(self.metadata[basename]['files']['dng']):
                return False
            for e in self.experts:
                if not os.path.isfile(self.metadata[basename]['files']['tiff16'][e]):
                    return False
        return True

    @property
    def dataset_dir(self) -> str:
        return os.path.join(self.root, self.__class__.__name__)




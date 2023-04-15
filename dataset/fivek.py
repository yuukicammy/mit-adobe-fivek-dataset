"""`MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset.

The MIT-Adobe FiveK Dataset is a collection that includes the following items:
    1) 5,000 raw images in DNG format,
    2) 5,000 retouched images in TIFF format,
    3) semantic information about each image.
"""
import os
from typing import List, Dict, Any
from torch.utils.data import Dataset
from dataset.fivek_builder import MITAboveFiveKBuilder


class MITAboveFiveK(Dataset):
    """`MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset.

    Args:
        root (string): Root directory in which MITAboveFiveK directory to be created.
        split (str):  One of {'train', 'val', 'test', 'debug'}.
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

    Notes:
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
                    ├── trainint.json
                    ├── validation.json
                    ├── testint.json
                    └── debugging.json
    Raises:
        RuntimeError: Error rises if dataset does not exist or the download failed.
    """

    def __init__(
        self, root: str, split: str, download: bool = False, experts: List[str] = None
    ) -> None:
        # root directory of datasets
        self.root = root

        # One of {'train', 'val', 'test'}
        split = split.lower()
        if split not in ["train", "val", "test", "debug"]:
            raise ValueError(
                f"Invalid split: {split}. `split` must be one of {'train', 'val', 'test', 'debug'}."
            )
        self.split = split

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
            ).build(split=self.split)
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
        return self.metadata[self.keys_list[index]]

    def __len__(self):
        return len(self.keys_list)

    def _check_exists(self) -> bool:
        if len(self.metadata) == 0:
            return False
        for basename in self.metadata.keys():
            if not os.path.isfile(self.metadata[basename]["files"]["dng"]):
                return False
            for e in self.experts:
                if not os.path.isfile(self.metadata[basename]["files"]["tiff16"][e]):
                    return False
        return True

    @property
    def dataset_dir(self) -> str:
        return os.path.join(self.root, self.__class__.__name__)

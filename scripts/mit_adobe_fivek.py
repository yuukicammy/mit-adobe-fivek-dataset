"""`MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset.

The MIT-Adobe FiveK Dataset is a collection that includes the following items:
    1) 5,000 raw images in DNG format,
    2) 5,000 retouched images in TIFF format,
    3) semantic information about each image.
"""
from typing import List, Dict, Tuple
import os
import tarfile
import urllib
import urllib3
import requests


class MITAboveFiveK:
    """`MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset.

    This class just downloads and saves the original MIT-Adobe FiveK, which is not in a Deep Learning-friendly format.
    The actual dataset loader for machine learning will be created by the user.

    Args:
        root (string): Root directory in which MITAboveFiveK directory to be created
            Expects the following folder structure if download=False:

            .. code::
                <root>
                └── MITAboveFiveK
                    └─ raw
                        ├── fivek_dataset # from the tar file
                        |   ├── filesAdobeMIT.txt
                        |   └── filesAdobe.txt
                        |   └── categories.txt
                        |   └── raw_photos
                        |       └── HQa1to700/photos/a0001-jmac_DSC1459.dng
                        |       └── ...
                        └── ProPhotoRGB
                            └── tiff16_a
                            |   └── a0001-jmac_DSC1459.tif
                            |   └── ...
                            └── tiff16_b
                            └── ...
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
        experts (List[str], optional): List of experts to download. Experts are 'A', 'B', 'C', 'D', and/or 'E'.
            The expert indicated as 'Expert A' is designated as 'A'.
            If None, no expert data will be downloaded.
    Raises:
        RuntimeError: Error rises if dataset does not exist or the download failed.
    """

    mirrors = [
        "https://data.csail.mit.edu/graphics/fivek/",
    ]
    archive = "fivek_dataset.tar"
    list_files = ["filesAdobe.txt", "filesAdobeMIT.txt"]
    category_file = "categories.txt"
    expert_dir_names = {
        "A": "tiff16_a",
        "B": "tiff16_b",
        "C": "tiff16_c",
        "D": "tiff16_d",
        "E": "tiff16_e",
    }
    _category_types = {0: "location", 1: "time", 2: "light", 3: "subject"}

    def __init__(
        self, root: str, download: bool = False, experts: List[str] = None
    ) -> None:
        # root directory of datasets
        self.root = root

        # list of 'A', 'B', 'C', 'D', and/or 'E'
        self._experts = experts if experts is not None else []

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError(
                "Dataset not found. You can use download=True to download it. \
                This error also occurs when download=True but the download did not complete."
            )

        # list of file id like 'a0001-jmac_DSC1459'
        self._file_ids = self._all_file_ids()

        # dictionary of categories.
        # ex) self.categories['a0001-jmac_DSC1459'] = [outdoor, day, sun_sky, nature]
        self._file_categories = self._load_categories()

    def getitem(self, index: int) -> Tuple[str, List[str], List[str]]:
        """Get raw image path, expert image list, and cacetories list corresponding to `index`.
        Args:
            index (int): Index

        Returns:
            Tuple[str, List[str], List[str]]: \
                Returns 1) RAW corresponding to the Index the path of the image, \
                        2) path list of expert images, and \
                        3) category list.
        """
        fid = self.file_ids[index]
        raw_file_path = self.raw_image_path(fid)
        expert_file_path = (
            []
            if len(self.experts) == 0
            else [self.expert_image_path(fid, expert) for expert in self.experts]
        )
        item_categories = self._file_categories[fid]
        return raw_file_path, expert_file_path, item_categories

    def load_data(self) -> Tuple[List[str], List[List[str]], List[str]]:
        """Returns all data in dataset.

        Returns:
            Tuple[List[str], List[List[str]], List[str]]: Tuple of \
                1) raw pathes, \
                2) expert image pathes, and \
                3) image categories.
        """
        raw_image_files = []
        expert_image_files = []
        image_categories = []
        for fid in self.file_ids:
            raw_image_files.append(self.raw_image_path(fid))
            image_categories.append(self._file_categories[fid])
            exp_files = []
            for exp in self.experts:
                exp_files.append(self.expert_image_path(fid, exp))
            expert_image_files.append(exp_files)
        return raw_image_files, expert_image_files, image_categories

    def len(self) -> int:
        """Number of the total raw files

        Returns:
            int: number of raw files
        """
        return len(self.file_ids)

    def download(self) -> None:
        """Download the MIT-Adobe FiveK Dataset if it doesn't exist."""

        if self._check_exists():
            return

        os.makedirs(self.raw_dir, exist_ok=True)
        self.download_rawdata()
        self.download_experts()

    def download_rawdata(self) -> None:
        """Download unprocessed raw resources including DNG files and metadata files."""

        if self._check_rawdata_exists():
            return

        archive_path = os.path.join(self.raw_dir, self.archive)
        if os.path.isfile(archive_path):
            print(f"Archive exists. Extracting {archive_path}")
            try:
                self.extract_archive(
                    from_path=archive_path, to_path=self.raw_dir)
            except (urllib.error.URLError, OSError) as error:
                print(f"Failed to extract {archive_path}:\n{error}")
                print("Next, try to download.")
            finally:
                print()
        for mirror in self.mirrors:
            url = f"{mirror}{self.archive}"
            print(f"Downloading {url} ...")
            try:
                archive_path = os.path.join(self.raw_dir, self.archive)
                self.download_file(url, archive_path)
                self.extract_archive(archive_path, self.raw_dir)
            except (urllib.error.URLError, OSError) as error:
                print(f"Failed to download (trying next):\n{error}")
                continue
            finally:
                print()
            break
        else:
            raise RuntimeError(f"Error downloading {self.archive}")

    def download_experts(self) -> None:
        """Download processed TIFF files creatred by experts."""
        if self._check_experts_exist():
            return

        file_ids = self._all_file_ids()
        if len(file_ids) == 0:
            print(
                f"Prease download raw data before, or \
                    put {self.file_ids[0]} and {self.file_ids[1]} in {self.raw_dir}/fivek_dataset."
            )
        print("Downloading experts images...")
        for expert in self.experts:
            target_dir = os.path.join(
                self.experts_dir, self.expert_dir_names[expert])
            os.makedirs(target_dir, exist_ok=True)
            for fid in file_ids:
                filepath = os.path.join(target_dir, f"{fid}.tif")
                if not os.path.isfile(filepath):
                    for mirror in self.mirrors:
                        url = f"{mirror}img/{self.expert_dir_names[expert]}/{fid}.tif"
                        try:
                            self.download_file(url=url, filepath=filepath)

                        except (urllib.error.URLError, OSError) as error:
                            print(f"{url}")
                            print(
                                f"Failed to download (trying next):\n{error}")
                            continue
                        break
                    else:
                        raise RuntimeError(f"Error downloading {fid}")

    def raw_image_path(self, fid: str) -> str:
        """Returns a raw image path (DNG format).

        Args:
            fid (str): file id of raw image. ex) 'a0001-jmac_DSC1459'

        Returns:
            str: raw image path
        """
        rawimage_path_format = "fivek_dataset/raw_photos/{}/photos/{}.dng"
        id_ = int(fid.split("-")[0][1:])
        if 5000 < id_:
            return ""  # Error
        target_dir = "HQa4201to5000"
        for s in range(1, 3502, 700):
            e = s + 700
            if s <= id_ and id_ < e:
                # Note: Only the directory `HQa1400to2100` has a different naming convention.
                target_dir = f"HQa{s}to{e-1}" if s != 1401 else "HQa1400to2100"
                break
        return os.path.join(self.raw_dir, rawimage_path_format.format(target_dir, fid))

    def expert_image_path(self, fid: str, expert: str = "A") -> str:
        """Returns the path to an expert retouched image (TIFF format).

        Args:
            fid (str): file id of an image. ex) 'a0001-jmac_DSC1459'
            expert (str, optional): Retouched expert identifier. \
                Expert is "A", "B", "C", "D", or "E". Defaults to "A".

        Returns:
            str: path of expert retouched image
        """
        return os.path.join(
            self.experts_dir, self.expert_dir_names[expert], f"{fid}.tif"
        )

    def _unique_categories(self) -> Dict[str, List[str]]:
        unique_categories = {}
        for i, type_ in self.category_types.items():
            uniques = list(set([cat[i]
                           for cat in self._file_categories.values()]))
            uniques.sort()
            unique_categories[type_] = uniques
        return unique_categories

    def _all_file_ids(self) -> List[str]:
        file_ids = []
        for lfile in self.list_files:
            file_path = os.path.join(self.raw_dir, "fivek_dataset", lfile)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="ascii") as file:
                    file_ids += list(map(lambda s: s.rstrip("\n"),
                                         file.readlines()))
        file_ids.sort()
        return file_ids

    def _check_exists(self) -> bool:
        return self._check_rawdata_exists() and self._check_experts_exist()

    def _check_experts_exist(self) -> bool:
        file_ids = self._all_file_ids()
        if len(file_ids) == 0:
            return False
        for expert in self.experts:
            if not all(
                os.path.isfile(self.expert_image_path(fid=fid, expert=expert))
                for fid in file_ids
            ):
                return False
        return True

    def _check_rawdata_exists(self) -> bool:
        file_ids = self._all_file_ids()
        if len(file_ids) == 0:
            return False
        return all(os.path.isfile(self.raw_image_path(fid)) for fid in file_ids)

    def _load_categories(self) -> Dict[str, List[str]]:
        categories = {}
        with open(
            os.path.join(self.raw_dir, "fivek_dataset", self.category_file),
            "r",
            encoding="ascii",
        ) as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip("\n")
                items = line.split(",")
                assert len(items) == 5
                categories[items[0]] = items[1:]
                # change 'None' to 'unknown'
                for j, c in enumerate(categories[items[0]]):
                    if c == "None":
                        categories[items[0]][j] = "unknown"

        assert sorted(list(categories.keys())) == self.file_ids
        return categories

    @property
    def file_ids(self) -> List[str]:
        """List of file ids defined in "filesAdobe.txt" and "filesAdobeMIT.txt". \
            The list of files is defined in `self.list_files`.
        """
        return self._file_ids

    @property
    def experts(self) -> List[str]:
        """The expert identifier specified at initialization.
        """
        return self._experts

    @property
    def category_types(self) -> Dict[int, str]:
        """
        Returns:
            Dict[int, str]: dictionary of category types.
                {0: "Location", 1: "Time", 2: "Light", 3: "Subject"}
        """
        return self._category_types

    @property
    def all_categories(self) -> Dict[str, List[str]]:
        """
        Returns:
            Dict[str, List[str]]: A dictionary that associates category types with categories.
                {'Location': ['indoor', 'outdoor', 'unknown'], \
                'Time': ['day', 'dusk', 'night', 'unknown'], \
                'Light': ['artificial', 'mixed', 'sun_sky', 'unknown'], \
                'Subject': ['abstract', 'animals', 'man_made', 'nature', 'people', 'unknown']}
        """
        return self._unique_categories()

    def file_categories(self, fid: str) -> List[str]:
        """Return categories corresponding to fid.
           ex) file_categories['a0001-jmac_DSC1459'] = [outdoor, day, sun_sky, nature]
        Args:
            fid: file id corresponding to an image. ex) 'a0001-jmac_DSC1459'
        Returns:
            list of categories
        """
        return self._file_categories[fid]

    @property
    def raw_dir(self) -> str:
        """Directory where the original, immutable dataset is stored."""
        return os.path.join(self.root, self.__class__.__name__, "raw")

    @property
    def experts_dir(self) -> str:
        """Directory where TIFF files in the ProPhotoRGB color space are stored."""
        return os.path.join(self.root, self.__class__.__name__, "raw", "ProPhotoRGB")

    @staticmethod
    def download_file(url: str, filepath: str, retry: int = 5) -> bool:
        """Download a file from the url and save it.

        Args:
            url(str): URL to retrieve the file with the GET method.
            filepath(str): Path to save the downloaded file.
            retry(int): Number of times to retry GET requests.

        Returns:
            bool: return True if the file is successfully saved, otherwise False.
        """
        s = requests.Session()
        retries = urllib3.Retry(
            total=retry, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
        )
        s.mount("http://", requests.adapters.HTTPAdapter(max_retries=retries))
        s.mount("https://", requests.adapters.HTTPAdapter(max_retries=retries))

        r = s.get(
            url,
            stream=True,
            timeout=(3.0, 7.5),
        )  # (connect-timeout, read-timeout)
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return os.path.isfile(filepath)

    @staticmethod
    def extract_archive(from_path: str, to_path: str) -> None:
        """extract a tar archive.

        Args:
            from_path (str): tar file path.
            to_path (str): root directory path where files are extracted.
        """
        with tarfile.open(from_path, "r") as tar:
            tar.extractall(to_path)

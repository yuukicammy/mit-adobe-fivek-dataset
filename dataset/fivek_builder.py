"""
Dataset Builder for the MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>`_Dataset
"""
import os
from typing import List, Dict, Any
import json
import tarfile
import urllib3
import requests
from tqdm import tqdm


class MITAboveFiveKBuilderConfig:
    """
    A configuration for MITAboveFiveKBuilder.

    Args:
        name (str): The name of the configuration.
        version (str): The version of the configuration.
        description (str): The description of the configuration.
    """

    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description


class MITAboveFiveKBuilder:
    """
    Builds a dataset for the MIT-Adobe FiveK <https://data.csail.mit.edu/graphics/fivek/>` dataset.

    Args:
        dataset_dir (str): The top directory of the dataset.
        config_name (str): The name of the configuration to use. Defaults to 'per_camera_model'.
        experts (List[str]): A list of expert names. Experts are 'a', 'b', 'c', 'd', and/or 'e'. Defaults to None.
        redownload (bool): Whether to force data to be re-downloaded, even if it already exists. Defaults to False.
        json_path (str): The path to the JSON file containing metadata about the dataset. Defaults to None.

    Attributes:
        dataset_dir (str): The top directory of the dataset.
        experts (List[str]): A list of expert names.
        config (MITAboveFiveKBuilderConfig): The configuration to use.
        metadata (dict): A dictionary containing metadata about the dataset.
        redownload (bool): Whether to force data to be re-downloaded, even if it already exists.

    Usage:
        1) initializing an instance.
            ex) builder = MITAboveFiveKBuilder('../data/')
        2) building the dataset.
            ex) metadata = builder.build()

    Notes:
        If `config_name` is 'per_camera_model', The directory structure is as follows.
            .. code::
                <dataset_dir>
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

        If `config_name` is 'archive', The directory structure is as follows.
            .. code::
                <dataset_dir>
                    ├─ raw
                    |   ├── fivek_dataset.tar
                    |   └── fivek_dataset
                    |       ├── filesAdobeMIT.txt
                    |       ├── filesAdobe.txt
                    |       ├── categories.txt
                    |       └── raw_photos
                    |          ├── HQa1to700/photos/a0001-jmac_DSC1459.dng
                    |          └── ...
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
    """

    # Named configurations that modify the data generated by download_and_prepare.
    BUILDER_CONFIGS = [
        MITAboveFiveKBuilderConfig(
            name="per_camera_model",
            version="0.1.0",
            description="This configuration saves DNG files in a separate directory for each camera model.",
        ),
        MITAboveFiveKBuilderConfig(
            name="archive",
            version="0.1.0",
            description="This configuration downloads extracts a tar archive and then downloads expert images from ",
        ),
    ]
    DEFAULT_CONFIG_NAME = "per_camera_model"

    JSON_URLS = {
        "train": "https://huggingface.co/datasets/yuukicammy/MIT-Adobe-FiveK/raw/main/training.json",
        "val": "https://huggingface.co/datasets/yuukicammy/MIT-Adobe-FiveK/raw/main/validation.json",
        "test": "https://huggingface.co/datasets/yuukicammy/MIT-Adobe-FiveK/raw/main/testing.json",
        "debug": "https://huggingface.co/datasets/yuukicammy/MIT-Adobe-FiveK/raw/main/debugging.json",
    }

    SPLITS = ["train", "val", "test", "debug"]

    def __init__(
        self,
        dataset_dir: str,
        config_name: str = "per_camera_model",
        experts: List[str] = None,
        redownload=False,
    ):
        self.dataset_dir = dataset_dir
        self.redownload = redownload
        self.experts = experts if experts else []
        self.config = self._create_builder_config(config_name)
        self._metadata = {}
        self.json_files = {
            "train": os.path.join(self.dataset_dir, "training.json"),
            "val": os.path.join(self.dataset_dir, "validation.json"),
            "test": os.path.join(self.dataset_dir, "testing.json"),
            "debug": os.path.join(self.dataset_dir, "debugging.json"),
        }
        os.makedirs(self.dataset_dir, exist_ok=True)
        self.download_json()

    def _create_builder_config(self, config_name: str) -> MITAboveFiveKBuilderConfig:
        """
        Returns the named configuration.

        Args:
            config_name (str): The name of the configuration.

        Returns:
            MITAboveFiveKBuilderConfig: The configuration object.

        Raises:
            ValueError: Error rises if config_name does not exist.
        """
        for config in self.BUILDER_CONFIGS:
            if config.name == config_name:
                return config
        raise ValueError(f"Invalid config name {config_name}")

    def _check_exists(self):
        """
        Check whether dataset files exist.

        Returns:
            bool: True if the dataset files exist, False otherwise.
        """
        for file_path in self.json_files.values():
            if not os.path.isfile(file_path):
                return False
        if len(self._metadata.keys()) == 0:
            return False
        for basename in self._metadata.keys():
            if not os.path.isfile(self.raw_file_path(basename)):
                return False
            for e in self.experts:
                if not os.path.isfile(self.expert_file_path(basename, e)):
                    return False
        return True

    def _generate_metadata_from_extracted_archive(self):
        """
        Generates metadata for the extracted archive.

        Returns:
            dict: The metadata dictionary.
        """
        basenames = []
        for lfile in ["filesAdobe.txt", "filesAdobeMIT.txt"]:
            file_path = os.path.join(self.dataset_dir, "raw", "fivek_dataset", lfile)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="ascii") as file:
                    basenames += list(map(lambda s: s.rstrip("\n"), file.readlines()))
        basenames.sort()
        categories = self._load_category_file()
        licenses = self._load_license_file()
        metadata = {}
        for basename in basenames:
            metadata[basename] = {
                "id": int(basename.split("-")[0][1:]),
                "urls": {
                    "dng": f"http://data.csail.mit.edu/graphics/fivek/img/dng/{basename}.dng",
                    "tiff16": {},
                },
                "files": {"dng": self.raw_file_path(basename), "tiff16": {}},
                "categories": {
                    "location": categories[basename][0],
                    "time": categories[basename][1],
                    "light": categories[basename][2],
                    "subject": categories[basename][3],
                },
                "license": licenses[basename],
            }
            for e in ["a", "b", "c", "d", "e"]:
                metadata[basename]["urls"]["tiff16"][
                    e
                ] = f"https://data.csail.mit.edu/graphics/fivek/img/tiff16_{e}/{basename}.tif"
            for e in self.experts:
                metadata[basename]["files"]["tiff16"][e] = self.expert_file_path(
                    basename, e
                )
        return metadata

    def _load_license_file(self) -> Dict[str, List[str]]:
        files_license = {}
        for fid in load_list(
            os.path.join(self.dataset_dir, "raw", "fivek_dataset", "filesAdobeMIT.txt")
        ):
            files_license[fid] = "AdobeMIT"
        for fid in load_list(
            os.path.join(self.dataset_dir, "raw", "fivek_dataset", "filesAdobe.txt")
        ):
            files_license[fid] = "Adobe"
        return files_license

    def _load_category_file(self) -> Dict[str, List[str]]:
        categories = {}
        with open(
            os.path.join(self.dataset_dir, "raw", "fivek_dataset", "categories.txt"),
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
        return categories

    def _load_json(self, split: str = None) -> Dict[str, Any]:
        metadata = {}
        if split and not split.lower() in self.SPLITS:
            raise ValueError(
                f"`split` must be one of [{' '.join(self.SPLITS)}] (`{split}` was given)."
            )
        if split:
            if os.path.isfile(self.json_files[split]):
                with open(self.json_files[split], "r", encoding="utf-8") as jf:
                    metadata = json.load(jf)
        else:
            for sp in self.SPLITS:
                if os.path.isfile(self.json_files[sp]):
                    with open(self.json_files[sp], "r", encoding="utf-8") as jf:
                        metadata.update(json.load(jf))
        return metadata

    def build(self, split: str = None) -> Dict[str, Any]:
        """
        Builds the dataset.

        Args:
            split (str): One of {'train', 'val', 'test', 'debug'}. If None, build data of all splits.

        Returns:
            Dict[str]: metadata of builded dataset.
            The format of metadata is as follows.
                {
                    '{basename}' : {
                        'files': {
                            'dng': '{path-to-dng-dir}/{basename}.dng',
                            'tiff16': {
                                'a': '{path-to-tiff16_a-dir}/{basename}.tiff',
                                ...
                        },
                        'categories': {
                            'location': '{location-of-image}',
                            'time': '{time-of-image}',
                            'light': '{light-of-image}',
                            'subject': '{subject-of-image}'
                        }
                    },
                }

        Raises:
            ValueError: Error raises if `split` is not one of {'train', 'val', 'test', 'debug'}.
            RuntimeError: Error rises if building dataset fails.
        """
        if split and not split.lower() in self.SPLITS:
            raise ValueError(
                f"`split` must be one of [{' '.join(self.SPLITS)}] (`{split}` was given)."
            )
        self._metadata = self._load_json(split)
        if self.config.name == "archive" and split == "debug":
            return self.metadata(split)
        self.download_raw()
        self.download_experts()
        if not self._check_exists():
            raise RuntimeError("Error building dataset.")
        return self.metadata(split)

    def metadata(self, split: str = None) -> Dict[str, Any]:
        """
        Args:
            split (str): One of {'train', 'val', 'test'}. If None, returns metadata of all splits.

        Returns:
            Dict[str]: metadata of the dataset.
            The format of metadata is as follows.
                {
                    '{basename}' : {
                        'files': {
                            'dng': '{path-to-dng-dir}/{basename}.dng',
                            'tiff16': {
                                'a': '{path-to-tiff16_a-dir}/{basename}.tiff',
                                ...
                        },
                        'categories': {
                            'location': '{location-of-image}',
                            'time': '{time-of-image}',
                            'light': '{light-of-image}',
                            'subject': '{subject-of-image}'
                        }
                    },
                }
        """
        metadata = {}
        if self.config.name == "archive" and split is None:
            metadata = self._generate_metadata_from_extracted_archive()
        else:
            metadata = self._load_json(split)
            tmp = self._metadata
            self._metadata = metadata
            for basename in metadata.keys():
                metadata[basename]["files"] = {
                    "dng": self.raw_file_path(basename),
                    "tiff16": {},
                }
                for e in self.experts:
                    metadata[basename]["files"]["tiff16"][e] = self.expert_file_path(
                        basename, e
                    )
            self._metadata = tmp
        return metadata

    def download_json(self) -> None:
        for key, path in self.json_files.items():
            if self.redownload or not os.path.isfile(path):
                download(self.JSON_URLS[key], path)

    def download_raw(self) -> None:
        """
        Downloads the raw dataset.

        Raises:
            RuntimeError: Error rises if downloading the raw dataset fails.
        """
        if self.config.name == "archive":
            raw_dir = os.path.join(self.dataset_dir, "raw")
            os.makedirs(raw_dir, exist_ok=True)
            archive_path = os.path.join(raw_dir, "fivek_dataset.tar")
            if self.redownload or not os.path.isfile(archive_path):
                print("Downloading the archie...")
                url = "https://data.csail.mit.edu/graphics/fivek/fivek_dataset.tar"
                if not download(url, archive_path):
                    raise RuntimeError(f"Error downloading an archive from {url}.")
                print("Extracting the archive...")
                extract_archive(archive_path, raw_dir)

        else:
            raw_dir = os.path.join(self.dataset_dir, "raw")
            os.makedirs(raw_dir, exist_ok=True)
            for basename in tqdm(self._metadata.keys(), desc="Downloading (dng) "):
                os.makedirs(self.raw_file_dir(basename), exist_ok=True)
                filepath = self.raw_file_path(basename)
                item_info = self._metadata[basename]
                if self.redownload or not os.path.isfile(filepath):
                    download(url=item_info["urls"]["dng"], filepath=filepath)

    def download_experts(self):
        """
        Download expert images for each image in the dataset.
        The expert images are saved in the processed directory in TIFF format.

        Raises:
            RuntimeError: Error rises if downloading expert images fails.
        """
        expert_dir = os.path.join(self.dataset_dir, "processed")
        os.makedirs(expert_dir, exist_ok=True)
        for e in self.experts:
            os.makedirs(os.path.join(expert_dir, f"tiff16_{e}"), exist_ok=True)
        for basename, value in tqdm(self._metadata.items(), desc="Downloading (tiff) "):
            os.makedirs(self.raw_file_dir(basename), exist_ok=True)
            for e in self.experts:
                filepath = self.expert_file_path(basename, e)
                if self.redownload or not os.path.isfile(filepath):
                    if not download(url=value["urls"]["tiff16"][e], filepath=filepath):
                        raise RuntimeError(
                            f"Error downloading a file from {value['urls']['tiff16'][e]}."
                        )

    def raw_file_path(self, basename: str) -> str:
        """
        Returns the path to the raw file.

        Args:
            basename (str): The basename of the image.

        Returns:
            str: The path to the raw file.
        """
        return os.path.join(self.raw_file_dir(basename), f"{basename}.dng")

    def raw_file_dir(self, basename: str) -> str:
        """
        Return the directory path for the raw image for the given image basename.
        """
        if self.config.name == "archive":
            path_format = "fivek_dataset/raw_photos/{}/photos"
            id_ = int(basename.split("-")[0][1:])
            assert 1 <= id_ <= 5000
            target_dir = "HQa4201to5000"
            for s in range(1, 3502, 700):
                e = s + 700
                if s <= id_ and id_ < e:
                    # Note: Only the directory `HQa1400to2100` has a different naming convention.
                    target_dir = f"HQa{s}to{e-1}" if s != 1401 else "HQa1400to2100"
                    break
            return os.path.join(self.dataset_dir, "raw", path_format.format(target_dir))
        else:
            make = self._metadata[basename]["camera"]["make"]
            model = self._metadata[basename]["camera"]["model"]
            camera_model = (make + "_" + model).replace(" ", "_")
            return os.path.join(self.dataset_dir, "raw", camera_model)

    def expert_file_path(self, basename: str, expert: str) -> str:
        """
        Returns the path to the expert image.

        Args:
            basename (str): The basename of the image.
            expert (str): The name of the expert (one of {'a', 'b', 'c', 'd', 'e'}).

        Returns:
            str: The path to the expert image.
        """
        return os.path.join(
            self.dataset_dir, "processed", f"tiff16_{expert}", f"{basename}.tif"
        )


def download(url: str, filepath: str, retry: int = 5) -> bool:
    """Download a file from the url and save it.

    Args:
        url(str): URL to retrieve the file with the GET method.
        filepath(str): Path to save the downloaded file.
        retry(int): Number of times to retry GET requests.

    Returns:
        bool: return True if the file is successfully saved, otherwise False.

    Raises:
        HTTPError, if one occurred.
    """
    s = requests.Session()
    retries = urllib3.Retry(
        total=retry, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
    )
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=retries))
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=retries))

    with s.get(
        url,
        stream=True,
        timeout=(3.0, 7.5),  # (connect-timeout, read-timeout)
    ) as response:
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
    s.close()
    return os.path.isfile(filepath)


def extract_archive(from_path: str, to_path: str) -> None:
    """extract a tar archive.

    Args:
        from_path (str): tar file path.
        to_path (str): root directory path where files are extracted.
    """
    with tarfile.open(from_path, "r") as tar:
        tar.extractall(to_path)


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

import os
from typing import List, Dict, Any
import json
import tarfile
import urllib3
import requests
from progress.bar import Bar

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
                    └── processed
                        ├── tiff16_a
                        |   ├── a0001-jmac_DSC1459.tif
                        |   └── ...
                        ├── tiff16_b
                        └── ...

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
                    └── processed
                            └── tiff16_a
                            |   └── a0001-jmac_DSC1459.tif
                            |   └── ...
                            └── tiff16_b
                            └── ...
    """
    # Named configurations that modify the data generated by download_and_prepare.
    BUILDER_CONFIGS = [
        MITAboveFiveKBuilderConfig(
            name='per_camera_model',
            version='0.1.0',
            description=
            'This configuration saves DNG files in a separate directory for each camera model.'
        ),
        MITAboveFiveKBuilderConfig(
            name='archive',
            version='0.1.0',
            description=
            'This configuration downloads extracts a tar archive and then downloads expert images from '
        )
    ]
    DEFAULT_CONFIG_NAME = 'per_camera_model'

    def __init__(self,
                 dataset_dir: str,
                 config_name: str = 'per_camera_model',
                 experts: List[str] = None,
                 redownload=False,
                 json_path: str = None):
        self.dataset_dir = dataset_dir
        self.redownload = redownload
        self.experts = experts if experts else []
        self.config = self._create_builder_config(config_name)
        if self.config.name == 'per_camera_model':
            with open(json_path, mode='r', encoding='utf-8') as file:
                self._metadata = json.load(file)
        else:
            self._metadata = {}

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
        raise ValueError(f'Invalid config name: {config_name}') 

    def _check_exists(self):
        if len(self._metadata) == 0:
            return False
        for basename in self._metadata.keys():
            if not os.path.isfile(self.raw_file_path(basename)):
                return False
            for e in self.experts:
                if not os.path.isfile(self.expert_file_path(basename, e)):
                    return False
        return True
    
    def _generate_metadata_from_extracted_archive(self):
        basenames = []
        for lfile in ['filesAdobe.txt', 'filesAdobeMIT.txt']:
            file_path = os.path.join(self.dataset_dir, 'raw', 'fivek_dataset', lfile)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='ascii') as file:
                    basenames += list(map(lambda s: s.rstrip("\n"),
                                         file.readlines()))
        basenames.sort()
        categories = self._load_category_file()
        metadata = {}
        for basename in basenames:
            metadata[basename] = {
                'urls' : {'tiff16' : {}},
                'files' : { 'dng' : self.raw_file_path(basename), 'tiff16': {}},
                'categories' : {
                    'location' : categories[basename][0],
                    'time': categories[basename][1],
                    'light': categories[basename][2],
                    'subject': categories[basename][3]
                }
            }
            for e in self.experts:
                metadata[basename]['urls']['tiff16'][e] = f'https://data.csail.mit.edu/graphics/fivek/img/tiff16_{e}/{basename}.tif'
                metadata[basename]['files']['tiff16'][e] = self.expert_file_path(basename, e)
        return metadata

    def _load_category_file(self) -> Dict[str, List[str]]:
        categories = {}
        with open(
            os.path.join(self.dataset_dir, 'raw', 'fivek_dataset', 'categories.txt'),
            'r',
            encoding='ascii',
        ) as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\n')
                items = line.split(',')
                assert len(items) == 5
                categories[items[0]] = items[1:]
                # change 'None' to 'unknown'
                for j, c in enumerate(categories[items[0]]):
                    if c == 'None':
                        categories[items[0]][j] = 'unknown'
        return categories

    def build(self) -> Dict[str, Any]:
        """
        Builds the dataset.

        Returns:
            Dict[str]: metadata of builded dataset.
            The format of metadata is as follows.
                {
                    'basename' : {
                        'files': {
                            'dng': 'path-to-dng-dir/{basename}.dng',
                            'tiff16': {
                                'a': 'path-to-tiff16_a-dir/{basename}.tiff',
                                ...
                        },
                        'categories': {
                            'location': 'location-of-image',
                            'time': 'time-of-image',
                            'light': 'light-of-image',
                            'subject': 'subject-of-image'
                        }
                    }
                }
        
        Raises:
            RuntimeError: Error rises if building dataset fails.
        """
        self.download_raw()
        self.download_experts()

        if not self._check_exists():
            raise RuntimeError(
                        'Error building dataset.')
        return self.metadata()

    def metadata(self) -> Dict[str, Any]:
        metadata = {}
        if self.config.name == 'archive':
            metadata = self._generate_metadata_from_extracted_archive()
        else:
            metadata = self._metadata
            for basename in self._metadata.keys():
                metadata[basename]['files'] = {
                    'dng' : self.raw_file_path(basename),
                    'tiff16': {}
                }
                for e in self.experts:
                    metadata[basename]['files']['tiff16'][e] = self.expert_file_path(basename, e)
        return metadata


    def download_raw(self) -> None:
        """
        Downloads the raw data.

        Raises:
            RuntimeError: Error rises if  the download fails.
        """
        if self.config.name == 'archive':
            raw_dir = os.path.join(self.dataset_dir, 'raw')
            os.makedirs(raw_dir, exist_ok=True)
            archive_path = os.path.join(raw_dir, 'fivek_dataset.tar')
            if self.redownload or not os.path.isfile(archive_path):
                print('Downloading the archie...')
                url = 'https://data.csail.mit.edu/graphics/fivek/fivek_dataset.tar'
                if not download(url, archive_path):
                    raise RuntimeError(
                        f'Error downloading an archive from {url}.')
                print('Extracting the archive...')
                extract_archive(archive_path, raw_dir)

        else:
            raw_dir = os.path.join(self.dataset_dir, 'raw')
            os.makedirs(raw_dir, exist_ok=True)
            with Bar('Downloading (dng)',
                     fill='#',
                     suffix='%(percent).1f%% - %(eta)ds') as bar:
                for basename in self._metadata.keys():
                    os.makedirs(self.raw_file_dir(basename), exist_ok=True)
                    filepath = self.raw_file_path(basename)
                    item_info = self._metadata[basename]
                    if self.redownload or not os.path.isfile(filepath):
                        if not download(url=item_info['urls']['dng'],
                                             filepath=filepath):
                            raise RuntimeError(
                                f"Error downloading a file from {item_info['urls']['dng']}."
                            )
                    bar.next()

    def download_experts(self):
        """
        Download expert images for each image in the dataset.
        The expert images are saved in the processed directory in TIFF format.

        Raises:
            RuntimeError: Error rises if  the download fails.
        """
        if self.config.name == 'archive' and len(self._metadata) == 0:
            self._metadata = self.metadata()
        expert_dir = os.path.join(self.dataset_dir, 'processed')
        os.makedirs(expert_dir, exist_ok=True)
        for e in self.experts:
            os.makedirs(os.path.join(expert_dir, f'tiff16_{e}'), exist_ok=True)
        with Bar('Downloading (tiff)',
                 fill='#',
                 suffix='%(percent).1f%% - %(eta)ds') as bar:
            for basename, value in self._metadata.items():
                os.makedirs(self.raw_file_dir(basename), exist_ok=True)
                for e in self.experts:
                    filepath = self.expert_file_path(basename, e)
                    if self.redownload or not os.path.isfile(filepath):
                        if not download(
                                url=value['urls']['tiff16'][e],
                                filepath=filepath):
                            raise RuntimeError(
                                f"Error downloading a file from {value['urls']['tiff16'][e]}."
                            )
                    bar.next()

    def raw_file_path(self, basename: str) -> str:
        """
        Return the file path of the raw image for the given image basename.
        """
        return os.path.join(self.raw_file_dir(basename), f'{basename}.dng')

    def raw_file_dir(self, basename: str) -> str:
        """
        Return the directory path for the raw image for the given image basename.
        """
        if self.config.name == 'archive':
            path_format = 'fivek_dataset/raw_photos/{}/photos'
            id_ = int(basename.split("-")[0][1:])
            assert (1 <= id_ <= 5000)
            target_dir = 'HQa4201to5000'
            for s in range(1, 3502, 700):
                e = s + 700
                if s <= id_ and id_ < e:
                    # Note: Only the directory `HQa1400to2100` has a different naming convention.
                    target_dir = f"HQa{s}to{e-1}" if s != 1401 else "HQa1400to2100"
                    break
            return os.path.join(self.dataset_dir, 'raw',
                                path_format.format(target_dir))
        else:
            make = self._metadata[basename]['camera']['make']
            model = self._metadata[basename]['camera']['model']
            camera_model = (make + '_' + model).replace(' ', '_')
            return os.path.join(self.dataset_dir, 'raw', camera_model)

    def expert_file_path(self, basename: str, expert: str) -> str:
        """
        Return the directory path for the expert image of the given expert type and image basename.
        """
        return os.path.join(self.dataset_dir, 'processed', f'tiff16_{expert}',
                            f'{basename}.tif')


def download(url: str, filepath: str, retry: int = 5) -> bool:
    """Download a file from the url and save it.

    Args:
        url(str): URL to retrieve the file with the GET method.
        filepath(str): Path to save the downloaded file.
        retry(int): Number of times to retry GET requests.

    Returns:
        bool: return True if the file is successfully saved, otherwise False.
    """
    s = requests.Session()
    retries = urllib3.Retry(total=retry,
                            backoff_factor=1,
                            status_forcelist=[500, 502, 503, 504])
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

def extract_archive(from_path: str, to_path: str) -> None:
        """extract a tar archive.

        Args:
            from_path (str): tar file path.
            to_path (str): root directory path where files are extracted.
        """
        with tarfile.open(from_path, 'r') as tar:
            tar.extractall(to_path)


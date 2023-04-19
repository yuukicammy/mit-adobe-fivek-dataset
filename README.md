# Table of Contents
1. [MIT-Adobe FiveK Dataset](#mit-adobe-fivek-dataset)
   - [Official Website](#official-website)  
   -  [License](#license)  
   -  [Data Samples](#data-samples)  
   - [References](#references)
1. [Tools for MIT-Adobe FiveK Dataset](#tools-for-mit-adobe-fivek-dataset)
   - [Requirements](#requirements)
   - [Usage](#usage)
   - [Example](#example)
   - [Easiy Multi-Process Pre-Processing](#easiy-multi-process-pre-processing)
   - [API](#api)
   - [Format to be acquired by DataLoader](#format-to-be-acquired-by-dataloader)
   - [Directory Structure](#directory-structure)
   - [Resources](#references)



# MIT-Adobe FiveK Dataset

The MIT-Adobe FiveK Dataset [[1]]( #references ) is a publicly available dataset providing the following items.

1. 5,000 RAW images in DNG format
2. retouched images of each RAW image by five experts in TIFF format (25,000 images, 16 bits per channel, ProPhoto RGB color space, and lossless compression)
3. semantic information about each image

The dataset was created by MIT and Adobe Inc., and is intended to provide a diverse and challenging set of images for testing image processing algorithms. The images were selected to represent a wide range of scenes, including landscapes, portraits, still lifes, and architecture. The images also vary in terms of lighting conditions, color balance, and exposure.

## Official Website

[MIT-Adobe FiveK Dataset](https://data.csail.mit.edu/graphics/fivek/)

## License

- [LicenseAdobe.txt](https://data.csail.mit.edu/graphics/fivek/legal/LicenseAdobe.txt) covers files listed in [filesAdobe.txt](https://data.csail.mit.edu/graphics/fivek/legal/filesAdobe.txt)
- [LicenseAdobeMIT.txt](https://data.csail.mit.edu/graphics/fivek/legal/LicenseAdobeMIT.txt) covers files listed in [filesAdobeMIT.txt](https://data.csail.mit.edu/graphics/fivek/legal/filesAdobeMIT.txt)

## Data Samples

|Raw (DNG)|Expert A|Expert B|Expert C|Expert D|Expert E|Categories|Camera Model|
|---|---|---|---|---|---|---|---|
|[a0001-jmac_</br >DSC1459.dng](https://data.csail.mit.edu/graphics/fivek/img/dng/a0001-jmac_DSC1459.dng)|![tiff16_a/a0001-jmac_DSC1459](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a0001-jmac_DSC1459_A.jpg)|![tiff16_b/a0001-jmac_DSC1459](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a0001-jmac_DSC1459_B.jpg)|![tiff16_c/a0001-jmac_DSC1459](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a0001-jmac_DSC1459_C.jpg)|![tiff16_d/a0001-jmac_DSC1459](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a0001-jmac_DSC1459_D.jpg)|![tiff16_e/a0001-jmac_DSC1459](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a0001-jmac_DSC1459_E.jpg)|{"location":"outdoor","time": "day","light": "sun_sky","subject": "nature"}|Nikon D70|
|[a1384-dvf_095.dng](https://data.csail.mit.edu/graphics/fivek/img/dng/a1384-dvf_095.dng)|![tiff16_a/a1384-dvf_095](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a1384-dvf_095_A.jpg)|![tiff16_b/a1384-dvf_095](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a1384-dvf_095_B.jpg)|![tiff16_c/a1384-dvf_095](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a1384-dvf_095_C.jpg)|![tiff16_d/a1384-dvf_095](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a1384-dvf_095_D.jpg)|![tiff16_e/a1384-dvf_095](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a1384-dvf_095_E.jpg)|{ "location": "outdoor", "time": "day", "light": "sun_sky", "subject": "nature" }|Leica M8|
|[a4607-050801_</br >080948__</br >I2E5512.dng](https://data.csail.mit.edu/graphics/fivek/img/dng/a4607-050801_080948__I2E5512.dng)|![tiff16_a/a4607-050801_080948__I2E5512](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a4607-050801_080948__I2E5512_A.jpg)|![tiff16_b/a4607-050801_080948__I2E5512](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a4607-050801_080948__I2E5512_B.jpg)|![tiff16_c/a4607-050801_080948__I2E5512](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a4607-050801_080948__I2E5512_C.jpg)|![tiff16_d/a4607-050801_080948__I2E5512](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a4607-050801_080948__I2E5512_D.jpg)|![tiff16_e/a4607-050801_080948__I2E5512](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/data/thumbnails/a4607-050801_080948__I2E5512_E.jpg)|{ "location": "indoor", "time": "day", "light": "artificial", "subject": "people" }|Canon EOS-1D Mark II|

## References

```
@inproceedings{fivek,
	author = "Vladimir Bychkovsky and Sylvain Paris and Eric Chan and Fr{\'e}do Durand",
	title = "Learning Photographic Global Tonal Adjustment with a Database of Input / Output Image Pairs",
	booktitle = "The Twenty-Fourth IEEE Conference on Computer Vision and Pattern Recognition",
	year = "2011"
}
```

# Tools for MIT-Adobe FiveK Dataset

This repository provides tools to download and use MIT-Adobe FiveK Dataset in a machine learning friendly manner.

The official archive has a complicated directory structure and that expert images need to be downloaded individually. To simplify this process, I created a tool that allows all data to be downloaded with just a single line of python code. 

In practice, the dataset is often used after RAW images have undergone various processing steps, such as adding noise, overexposure, and underexposure to emulate camera errors. 
This tool also allows for these kinds of processing to be easily performed using PyTorch's DataLoader.
You can iteratively retrieve data via Pytorch's DetaLoader for your own use.

## Requirements
- Python 3.7 or greater
- Pytorch 2.X 
- tqdm
- urllib3

## Usage

1. locate [`dataset/fivek.py`](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/dataset/fivek.py) and [`dataset/fivek_builder.py`](https://github.com/yuukicammy/mit-adobe-fivek-dataset/raw/master/dataset/fivek_builder.py) in your program.

2. import `MITAboveFiveK` in your python code.

3. download the dataset by initializing a `MITAboveFiveK` instance with `download=True`.
```
fivek = MITAboveFiveK(root="/datasets", split="debug", download=True, experts=["a"])
```
4. data can be iteratively obtained via PyTorch's DataLoader.

You can use as follows.

<span style="color:red">
NOTE: For DataLoader, MUST set `batch_size` to `None` to disable automatic batching.
</span>

```python
from torch.utils.data.dataloader import DataLoader
from dataset.fivek import MITAboveFiveK

data_loader = DataLoader(
    MITAboveFiveK(root="path-to-dataset-root", split="train", download=True, experts=["a"]),
    batch_size=None)

for item in data_loader:
    # Processing as you want.
    # Add noise, overexpose, underexpose, etc.
    print(item["files"]["dng"])
```

## Example

Please see [sample code](./sample_processing.py) .

## Easiy Multi-Process Pre-Processing

If you set a function for preprocessing as `process_fn`, you can use PyTorch DataLoader to perform preprocessing in a multi-process manner!
See [sample code](./sample_processing.py) .

```python
    class Preprocess:
        def hello_world(self, item):
            print(f"hello world! the current ID is {item['id']}")

    data_loader = DataLoader(
        MITAboveFiveK(
            root=args.root_dir,
            split="debug",
            process_fn=Preprocess().hello_world),
        batch_size=None,  # must be `None`
        num_workers=args.workers  # multi-process for pre-processing
    )
    for item in data_loader:
        # pre-processing has already been performed.
        print(item)
```

## API

CLASS MITAboveFiveK(torch.utils.data.dataset.Dataset)  
- - -
   MITAboveFiveK(root: str, split: str, download: bool = False, experts: List[str] = None) -> None

- root (str):  
    The root directory where the MITAboveFiveK directory exists or to be created.
- split (str):   
    One of {'train', 'val', 'test', 'debug'}. 'debug' uses only 9 data contained in 'train'.
- download (bool):  
    If True, downloads the dataset from the official urls. Files that already exist locally will skip the download. Defaults to False.
- experts (List[str]):  
    List of {'a', 'b', 'c', 'd', 'e'}. 'a' means 'Expert A' in the [website](https://data.csail.mit.edu/graphics/fivek/ ). If None or empty list, no expert data is used. Defaults to None.
- download_workers (int):  
    How many subprocesses to use for data downloading.
    None means that min(32, cpu_count() + 4). Defaults to 1.
- process_fn ([[Dict[str, Any]], Any]): 
    Function of the processing to be performed on each element of the dataset.
    This function applied in __getitem__(). Defaults to None.

## Format to be acquired by DataLoader
```
{
   "basename": "<(str) basename of the image>"
    "files": {
        "dng": "<(str) path of the local DNG file>", 
        "tiff16": {
            "a": "<(str) path of the local TIFF file retouched by Expert A>",
            "b": "<(str) path of the local TIFF file retouched by Expert B>",
            "c": "<(str) path of the local TIFF file retouched by Expert C>",
            "d": "<(str) path of the local TIFF file retouched by Expert D>",
            "e": "<(str) path of the local TIFF file retouched by Expert E>"
        }
    },
    "categories": {
        "location": "<(str) image categories extracted from the official resouece>",
        "time": "<(str) image categories extracted from the official resouece>",
        "light": "<(str) image categories extracted from the official resouece>",
        "subject": "<(str) image categories extracted from the official resouece>"
    },
    "id": <(int) id extracted from basename>,
    "license": "<(str) Adobe or AdobeMIT>",
    "camera": {
        "make": "<(str) maker name extracted from dng>",
        "model": "<(str) camera model name extracted from dng>"
    }
}

```

example
```python
from torch.utils.data.dataloader import DataLoader
from dataset.fivek import MITAboveFiveK

data_loader = DataLoader(
    MITAboveFiveK(root="/datasets", split="debug", download=True, experts=["a", "c"], download_workers=4),
    batch_size=None)
item = next(iter(data_loader))
print(item)
# 
# Output↓
# {'categories': {'location': 'outdoor', 'time': 'day', 'light': 'sun_sky', 'subject': 'nature'}, 
#  'id': 1384, 'license': 'Adobe', 
#  'camera': {'make': 'Leica', 'model': 'M8'}, 
#  'files': {'dng': '/datasets/MITAboveFiveK/raw/Leica_M8/a1384-dvf_095.dng', 
#            'tiff16': {'a': '/datasets/MITAboveFiveK/processed/tiff16_a/a1384-dvf_095.tif', 
#                       'c': '/datasets/MITAboveFiveK/processed/tiff16_c/a1384-dvf_095.tif'}}, 
#  'basename': 'a1384-dvf_095'}
```

## Directory Structure

When a dataset is downloaded using the `MITAboveFiveK` class, the files are saved in the following structure.
RAW images are stored in a directory for each camera model.

```
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
```

## Resources
I provides json files that contain metadata for each image.

|Split| Json File | Number of data | Note|
|---|---|---|---|
| train | [training.json](https://huggingface.co/datasets/yuukicammy/MIT-Adobe-FiveK/raw/main/training.json) | 3500 ||
| val | [validation.json](https://huggingface.co/datasets/yuukicammy/MIT-Adobe-FiveK/raw/main/validation.json) | 500 ||
| test | [testing.json](https://huggingface.co/datasets/yuukicammy/MIT-Adobe-FiveK/raw/main/testing.json) | 1000 ||
| debug | [debug.json](https://huggingface.co/datasets/yuukicammy/MIT-Adobe-FiveK/raw/main/debug.json) | 9 |Subset of train|






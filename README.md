# MIT-Adobe FiveK Dataset

The MIT-Adobe FiveK Dataset is a publicly available dataset providing the following items.

1. 5,000 raw images in DNG format
2. retouched images of each raw image by five experts in TIFF format (16 bits per channel, ProPhoto RGB color space, and lossless compression)
3. semantic information about each image

The dataset was created by MIT and Adobe Systems, Inc., and is intended to provide a diverse and challenging set of images for testing image processing algorithms. The images were selected to represent a wide range of scenes, including landscapes, portraits, still lifes, and architecture. The images also vary in terms of lighting conditions, color balance, and exposure.

The dataset is a valuable resource for the computer vision and image processing communities, providing a diverse and challenging set of images for benchmarking and evaluation.

## Official Website

[MIT-Adobe FiveK Dataset](https://data.csail.mit.edu/graphics/fivek/)

## License

- [LicenseAdobe.txt](https://data.csail.mit.edu/graphics/fivek/legal/LicenseAdobe.txt) covers files listed in [filesAdobe.txt](https://data.csail.mit.edu/graphics/fivek/legal/filesAdobe.txt)
- [LicenseAdobeMIT.txt](https://data.csail.mit.edu/graphics/fivek/legal/LicenseAdobeMIT.txt) covers files listed in [filesAdobeMIT.txt](https://data.csail.mit.edu/graphics/fivek/legal/filesAdobeMIT.txt)

## Data Samples

|Raw (DNG)|Expert A|Expert B|Expert C|Expert D|Expert E|Categories|Camera Model|
|---|---|---|---|---|---|---|---|
|[a0001-jmac_DSC1459.dng](https://data.csail.mit.edu/graphics/fivek/img/dng/a0001-jmac_DSC1459.dng)|![tiff16_a/a0001-jmac_DSC1459](./data/thumbnails/a0001-jmac_DSC1459_A.jpg)|![tiff16_b/a0001-jmac_DSC1459](./data/thumbnails/a0001-jmac_DSC1459_B.jpg)|![tiff16_c/a0001-jmac_DSC1459](./data/thumbnails/a0001-jmac_DSC1459_C.jpg)|![tiff16_d/a0001-jmac_DSC1459](./data/thumbnails/a0001-jmac_DSC1459_D.jpg)|![tiff16_e/a0001-jmac_DSC1459](./data/thumbnails/a0001-jmac_DSC1459_E.jpg)|{"location":"outdoor","time": "day","light": "sun_sky","subject": "nature"}|Nikon D70|
|[a1384-dvf_095.dng](https://data.csail.mit.edu/graphics/fivek/img/dng/a1384-dvf_095.dng)|![tiff16_a/a1384-dvf_095](./data/thumbnails/a1384-dvf_095_A.jpg)|![tiff16_b/a1384-dvf_095](./data/thumbnails/a1384-dvf_095_B.jpg)|![tiff16_c/a1384-dvf_095](./data/thumbnails/a1384-dvf_095_C.jpg)|![tiff16_d/a1384-dvf_095](./data/thumbnails/a1384-dvf_095_D.jpg)|![tiff16_e/a1384-dvf_095](./data/thumbnails/a1384-dvf_095_E.jpg)|{ "location": "outdoor", "time": "day", "light": "sun_sky", "subject": "nature" }|Leica M8|
|[a4607-050801_080948__I2E5512.dng](https://data.csail.mit.edu/graphics/fivek/img/dng/a4607-050801_080948__I2E5512.dng)|![tiff16_a/a4607-050801_080948__I2E5512](./data/thumbnails/a4607-050801_080948__I2E5512_A.jpg)|![tiff16_b/a4607-050801_080948__I2E5512](./data/thumbnails/a4607-050801_080948__I2E5512_B.jpg)|![tiff16_c/a4607-050801_080948__I2E5512](./data/thumbnails/a4607-050801_080948__I2E5512_C.jpg)|![tiff16_d/a4607-050801_080948__I2E5512](./data/thumbnails/a4607-050801_080948__I2E5512_D.jpg)|![tiff16_e/a4607-050801_080948__I2E5512](./data/thumbnails/a4607-050801_080948__I2E5512_E.jpg)|{ "location": "indoor", "time": "day", "light": "artificial", "subject": "people" }|Canon EOS-1D Mark II|

# Dataset Loader

## Requirements

## Usage


I provide 
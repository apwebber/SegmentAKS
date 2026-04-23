# SegmnentAKS

SegmentAKS is a package that explores the nodule surface area correlation that was published in [Sweetman et al. 2024](https://www.nature.com/articles/s41561-024-01480-8), and adds additional data. It shows a method of image segmentation and surface area calculation and calculates correlation coefficients of surface area and nodule weight against rises in oxygen concentration.

## Contents

### Python code

* `segmentaks.py` contains utility functions and a class for image segmentation.
* `segmentation.ipynb` is a jupyter notebook that runs the image segmentation for each top-shot image, collates the data, calculates correlation coefficients and creates the plots.
* `sweetman_2024.ipynb` explores the data as originally published in [Sweetman et al. 2024](https://www.nature.com/articles/s41561-024-01480-8), as well as data from three chambers that were omitted from that publication.

### data

* `/data` contains the raw and edited chamber images, oxygen concentrations and nodule weights, and necessary data published in [Sweetman et al. 2024](https://www.nature.com/articles/s41561-024-01480-8)

## Installation

Clone the repo to install SegmentAKS, then `uv` to sync the environment. [Git](https://git-scm.com/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) need to be installed.

```bash
git clone [insert repo url] SegmentAKS
cd SegmentAKS
uv sync
```

Additionally, SegmentAKS uses the [SciencePlots](https://github.com/garrettj403/SciencePlots) package to generate publication quality figures. This has some additional requirements including LaTeX. If LaTeX is not installed the code will execute, but SciencePlots won't be used.

## Usage

Run the jupyter notebooks.

## License

Creative Commons Attribution 4.0 International Public License

Copyright (c) 2026 The Metals Company

You are free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit.

For the full text, see https://creativecommons.org/licenses/by/4.0/legalcode

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

[MIT](https://choosealicense.com/licenses/mit/)

Copyright (c) 2026 The Metals Company
  
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

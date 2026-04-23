from collections import Counter
from pathlib import Path
from typing import Tuple

from PIL import Image
import matplotlib.image as img
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap
import pandas as pd
import pingouin as pg
from skimage import color
from sklearn.cluster import KMeans


def write_publication_table(df: pd.DataFrame, outpath: str):
    with pd.ExcelWriter(outpath, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=True)

        workbook  = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Define formats
        normal = workbook.add_format()
        superscript = workbook.add_format({'font_script': 1})
        subscript = workbook.add_format({'font_script': 2})

        # 'Chamber'
        worksheet.write(
            0, 0,
            "Chamber",
        )

        # 'Incubation Time (h)'
        worksheet.write(
            0, 1,
            "Incubation Time (h)",
        )

        # 'T0 O2 (μmol)'
        worksheet.write_rich_string(0, 2,
            normal, "T0 O", subscript, "2", normal, " (μmol)"
        )
        # 'Max O2 (μmol)'
        worksheet.write_rich_string(0, 3,
            normal, "Max O", subscript, "2", normal, " (μmol)"
        )
        # '𝛿O2 max (μmol)'
        worksheet.write_rich_string(0, 4,
            normal, "\u0394O", subscript, "2", normal, " max (μmol)"
        )
        # 'End O2 (μmol)'
        worksheet.write_rich_string(0, 5,
            normal, "End O", subscript, "2", normal, " (μmol)"
        )
        # '𝛿O2 end (μmol)'
        worksheet.write_rich_string(0, 6,
            normal, "\u0394O", subscript, "2", normal, " end (μmol)"
        )
        # 'Water Volume (L)'
        worksheet.write(0, 7, "Water Volume (L)")
        # 'Flux (mmol O2 m-2 -1)'
        worksheet.write_rich_string(0, 8,
            normal, "Flux (mmol O", subscript, "2",
            normal, " m", superscript, "-2",
            normal, ")"
        )
        # 'Total O2 production (μmol)'
        worksheet.write_rich_string(0, 9,
            normal, "Total O", subscript, "2", normal, " production (μmol)"
        )
        # 'Layer 0-2 cm nodule weight (g)'
        # 'Layer 2-5 cm nodule weight (g)'
        # 'Total nodule weight (g)'
        worksheet.write(0, 10, "Layer 0-2 cm nodule weight (g)")
        worksheet.write(0, 11, "Layer 2-5 cm nodule weight (g)")
        worksheet.write(0, 12, "Total nodule weight (g)")
        # 'Nodule coverage (cm2)'
        worksheet.write_rich_string(0, 13,
            normal, "Nodule area (cm", superscript, "2", normal, ")"
        )
        # 'Number of nodules'
        worksheet.write(0, 14, "Number of nodules")
        # 'Average nodule area (cm2)'
        worksheet.write_rich_string(0, 15,
            normal, "Average nodule area (cm", superscript, "2", normal, ")"
        )
        # 'Average nodule weight (g)'
        worksheet.write(0, 16, "Average nodule weight (g)")
        # 'Notes'
        worksheet.write(0, 17, "Notes")


def matplotlib_has_latex() -> bool:
    """Check that maptlotlib has access to LaTeX

    Returns:
        bool: True if LaTeX is available
    """
    import matplotlib
    matplotlib.rcParams['text.usetex'] = True

    import matplotlib.pyplot as plt

    try:
        fig, ax = plt.subplots()
        ax.set_title('Total O$_2$ production ($\\mu$mol)')
        fig.canvas.draw()
        plt.close(fig)
        return True
    except Exception:
        return False

def print_correlation(x, y, method: str = 'spearman'):
    """Uses the pingouin library to calculate the correlation of x,y points
    and prints it to console.

    Args:
        x (_type_): array of x data
        y (_type_): array of y data
        method (str, optional): Correlation method as used by pg.corr. Defaults to 'spearman'.
    """
    x, y = np.asarray(x), np.asarray(y)
    valid = ~np.isnan(x) & ~np.isnan(y)
    x = x[valid]
    y = y[valid]
    
    full = pg.corr(x, y, method=method)
    full_corr = full['r'].values[0]
    full_p = full['p_val'].values[0]
    ci_low, ci_high = full['CI95'].values[0]
    outliers = full['outliers'].values[0] if 'outliers' in full.columns else 'N/A'
    
    print(f"{method.capitalize()} r = {full_corr:.4f}  |  p = {full_p:.4f}  |  95% CI = [{ci_low:.4f}, {ci_high:.4f}] | outliers: {outliers}")
    
class KMeansSeg:
    """Assign pixels as either nodule or background using K-Means clustering.
    
    Then calculate area of nodules based on real-world dimensions of the image.
    """
    
    def __init__(self, n_clusters: int, fpath: str | Path, dimentsions_cm: list[float] = [22.0,22.0], n_nodules: int | None = None):
        self.n_clusters = n_clusters
        self.fpath = fpath
        self.dimensions_cm = dimentsions_cm
        self.n_nodules = n_nodules
        self.nod_clusters = []
        
        self.results: Counter | None = None
        self.reject: bool = False # whether to reject this image based on image quality or clustering
    
    def do_segmentation(self):
        self._read_image()
        (h,w,c) = self.img_arr.shape
        img2D = self.img_arr.reshape(h*w,c)
        
        kmeans_model = KMeans(n_clusters=self.n_clusters, random_state=1)
        cluster_labels = kmeans_model.fit_predict(color.rgb2hsv(img2D))
        self.img_quant = np.reshape(cluster_labels, (h,w))
        
        self._assign_nodules()
        self._calculate_results()
        
    def set_nod_clusters(self, nod_clusters: list[int]):
        self.nod_clusters = nod_clusters
        self._assign_nodules()
        self._calculate_results()
        
    def get_results(self) -> tuple[float | None, int | None, float | None]:
        if self.results is None:
            raise ValueError("Perform segmentation first.")
        
        if self.reject:
            return None, None, None
        
        image_area = self.dimensions_cm[0] * self.dimensions_cm[1]
        percent_nods = self.results[1] / (self.results[0] + self.results[1])
        area_of_nodules = image_area * percent_nods
        average_nod_area = area_of_nodules / self.n_nodules if self.n_nodules else None
        
        return area_of_nodules, self.n_nodules, average_nod_area
        
        
    def plot_comparison(self, overlay: bool = False) -> Tuple[Figure, np.ndarray[plt.Axes]]:
        if overlay:
            return self._plot_overlay_comparison()
        
        if self.img_quant is None:
            raise ValueError("Perform segmentation first.")
        
        fig, ax = plt.subplots(1,3, figsize=(12,16))
        ax[0].imshow(self.img_arr)
        ax[0].set_title('Original Image')
        ax[0].axis('off')
        
        cmap = cm.get_cmap('gist_rainbow', 256)
        newcolors = cmap(np.linspace(0, 1, self.n_clusters))
        newcmp = ListedColormap(newcolors)

        ax[1].imshow(self.img_quant, cmap=newcmp)
        ax[1].set_title('Quantized Image')
        
        for i, c in enumerate(newcolors):
            ax[1].plot([None], [None], c=c, label=str(i))
        
        ax[1].legend()
        ax[1].axis('off')
        
        ax[2].imshow(self.img_seg, interpolation='nearest')
        ax[2].set_title('Segmented Image')
        ax[2].axis('off')
        
        return fig, ax
    
    def _plot_overlay_comparison(self) -> Tuple[Figure, np.ndarray[plt.Axes]]:
        if self.img_quant is None:
            raise ValueError("Perform segmentation first.")
        
        fig, ax = plt.subplots(2,2, figsize=(12,12), squeeze=True, layout='constrained')
        ax = ax.flatten()
        ax[0].imshow(self.img_arr)
        ax[0].set_title('Original Image', fontsize=12)
        ax[0].axis('off')
        
        cmap = cm.get_cmap('gist_rainbow', 256)
        newcolors = cmap(np.linspace(0, 1, self.n_clusters))
        newcmp = ListedColormap(newcolors)

        ax[1].imshow(self.img_quant, cmap=newcmp)
        ax[1].set_title('Quantized Image', fontsize=12)
        
        for i, c in enumerate(newcolors):
            ax[1].plot([None], [None], c=c, label=str(i))
        
        ax[1].legend(fontsize='large')
        ax[1].axis('off')
        
        ax[2].imshow(self.img_arr)
        masked = np.ma.masked_where(self.img_seg == 0, self.img_seg)
        ax[2].imshow(masked, interpolation='nearest', cmap='Greys', alpha=0.8)
        ax[2].set_title('Segmented Image', fontsize=12)
        ax[2].axis('off')
        
        ax[3].imshow(self.img_arr)
        masked = np.ma.masked_where(self.img_seg == 1, self.img_seg)
        ax[3].imshow(masked, interpolation='nearest', cmap='Greys', alpha=0.8)
        ax[3].set_title('Segmented Image', fontsize=12)
        ax[3].axis('off')
        
        return fig, ax
    
    def _assign_nodules(self):
        if self.img_quant is None:
            raise ValueError("Perform segmentation first.")
        
        self.img_seg = np.zeros(self.img_quant.shape)
        self.img_seg[np.isin(self.img_quant, self.nod_clusters)] = 1
    
    def _calculate_results(self):
        if self.img_seg is None:
            raise ValueError("Perform segmentation first.")
        
        self.results = Counter(self.img_seg.flatten())
        
    def _read_image(self, resize: bool = False):
        arr = img.imread(self.fpath)
        
        if not resize:
            self.img_arr = arr
            return
        else:
            im = Image.fromarray(arr)
            max_width = 800
            if im.width > max_width:
                ratio = max_width / im.width
                new_height = int(im.height * ratio)
                im = im.resize((max_width, new_height), Image.LANCZOS)

            self.img_arr = np.array(im)
        
    

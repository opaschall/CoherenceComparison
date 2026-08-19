# Code to reproduce the results and figures in submitted manuscript Paschall et al., 202X 
**"To normalize (by backscatter intensity) or not to normalize: Observations of InSAR coherence dependencies on normalization over the Imperial Valley, California"** by O. Paschall, L. Marone, K. Devlin, and R. Lohman. Submitted to Elsevier's *Computers & Geosciences* on <mark>month day</mark>, 2026.

This study shows that a more computationally-efficient method of calculating InSAR coherence (we call this "unit vector coherence" does not pose any deficiencies when using coherence to inform estimates of displacement rates, and for masking unreliable pixels.
<br><br>

## Installing dependencies
Install the conda environments `pygmt` (only used in producing Figure 1) and `earthscope_insar` (used to produce all other figures) using the YML files in the folder `/0_Creating_conda_env/`. I have included a version of each YML file that may be more compatible with another user's computer if the first installation does not work. 
<br><br>
Instructions for installing a conda environment with a YML file [can be found here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). 
<br><br>
Conda environments can be used as Jupyter notebook processing kernels. [I use VSCode as my code editor](https://code.visualstudio.com/), and you can set it up so that your Jupyter notebooks can access your Python (conda) environments to use them as processing kernels. This has worked well for me.
<br><br>

## Downloading SLCs 
Single Look Complex (SLC) images are the input data for this study. These files are very large, so we do not provide the files themselves here in this repository, but rather the code we used to download them to our local machine. The Sentinel-1 satellite data used in this study is free and open through the European Space Agency (ESA) and the Alaska Satellite Facility (ASF) DAAC. 
<br><br>
- First, the user needs to explore what data they want to use (what region of interest/bounding box, what dates to include, which polarizations of data, etc.). We use the [web-based graphical interface ASF Vertex](https://search.asf.alaska.edu/#/?dataset=SENTINEL-1) for this purpose. 
<br><br>
- Then, follow the steps in the Jupyter notebook `/1_Downloading_data/run_all.ipynb` using the `earthscope_insar` conda environment/processing kernel. A description of the file structure that running this notebook produces is described in comments at the bottom of the notebook.
<br><br>
- The user should now have a coregistered stack of SLCs. 
<br><br>

## Producing Figures 1-3

### Figure 1
*Basemap (optical image, faults, and InSAR data footprint)* 
<br><br>
- Use the following notebook to produce Figure 1: `/3_Making_figures/Figure_1_basemap/Fig_1_basemap.ipynb`. All of the necessary files are in the folder with the notebook. Use the `pygmt` conda environment for running this notebook. 
<br><br>
- From here forward, the `earthscope_insar` conda environment is used exclusively. 
<br><br>

### Figure 2: 
*Synthetic time series inversion example* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_2_synthetic_inversion/Fig_2_synthetic_rate_inversion.ipynb`
<br><br>

### Figure 3
*Surface types map* 
<br><br>
This map identifies the following surface types: desert, urban/barren, and vegetated. This step requires two files: `roadarray.r4` and `no_desert.r4`. 
<br><br>
- The first file `roadarray.r4` is produced by running code published by coauthor Kelly Devlin. First, the USDA Cropland Data Layer (CDL) file is [converted into radar coordinates with this notebook](https://github.com/kdevlin525/InSAR-calculations/blob/main/notebooks/ungeo_cropscape.ipynb) (we call this "ungeocoding," and it puts the CDL on the same grid as our SAR/InSAR data). Then, certain land cover types are screened for accuracy, combined into a single mask, and [saved as the `roadarray.r4` file in this notebook](https://github.com/kdevlin525/C-band-phase-bias/blob/main/segment_fields.ipynb) (naming convention is because roads typify stable surface types we tend to see as "favorable" in InSAR analyses.
<br><br>
- The second file `no_desert.r4` is produced by point-clicking the boundary between desert and agricultural valley, with the following notebook` 3_Making_figures/Figure_3_surface_types_map/draw_polygon_to_mask_desert.ipynb` 
<br><br>
- Once the user has successfully created the `roadarray.r4` and `no_desert.r4` mask files, run this notebook: `/3_Making_figures/Figure_3_surface_types_map/Fig_3_land_cover_map.ipynb`
<br><br>

## Create coherence files with Methods 1 and 2 and calculate averages.
The code to perform these calculations and save the coherence files are in the folder: `/2_Calculating_coherence_2_ways/`. 
<br><br>
- First, run this notebook to produce coherence files with Method 1 (complex coherence magnitude): `/2_Calculating_coherence_2_ways/produce_method1_files.py`
<br><br>
- Second, run this notebook to produce coherence files with Method 2 (unit vector coherence magnitude): `/2_Calculating_coherence_2_ways/produce_method2_files.py`
<br><br>
- Then, to calculate the average coherence value at each pixel with both methods, run this notebook: `/2_Calculating_coherence_2_ways/calculate_avg_coh_both_methods.py`. This produces the `avg_coh_method1.r4` and `avg_coh_method2.r4` files needed in the following analyses/figures.
<br><br>

## Producing Figures 4-12 and S1

### Figure 4-6 and S1
*Average coherence differences between the two methods* <br>
- To produce Figures 4-6, run this notebook: `/3_Making_figures/Figure_4-6_S1_coherence_diffs/Fig_4-6_coherence_diffs.ipynb`
<br><br>
- To produce Figure S1, run this notebook: `/3_Making_figures/Figure_4-6_S1_coherence_diffs/Fig_S1_coherence_diffs_histograms.ipynb`
<br><br>

### Figures 7-12
*USDA Cropland Data Layer (CDL) map of our region of interest, and focus areas with four panels each* 
<br><br>
- To produce Figures 7-12, run this notebook: `/3_Making_figures/Figure_7-12_CDL_map_and_focus_areas/Fig_7_8-12_CDL_map_and_focus_areas.ipynb`
<br><br>

## Performing displacement rate inversions
We do this with three methods: (1) unweighted inversion, just solving for the slope of a least squares line-of-best-fit through the cumulative displacement time series, (2) a weighted inversion with complex coherence magnitude (Method 1 of coherence estimation) as weights in our weighted least squares inversion of displacement rate, and (3) a weighted inversion with unit vector coherence magnitude (Method 2 of coherence estimation) as weights in a weighted least squares inversion of displacement rate. 
<br><br>
- We must first unwrap all of our sequential interferograms so that phase values are not limited to the $[-\pi,\pi]$ range. To do so, run the notebook: `/2.1_Inverting_for_displacement_rates/unwrap_full_res_interferograms.ipynb`. We use the method outlined in [Paschall and Lohman (2025)](https://ieeexplore.ieee.org/abstract/document/11214424). 
<br><br>
- Then, to perform unweighted inversions of displacement rate, run this notebook: `/2.1_Inverting_for_displacement_rates/unwrap_full_res_interferograms.ipynb`
<br><br>
- To perform weighted inversions using both Methods 1 and 2 in the weighted least squares inversions, run this notebook: `2.1_Inverting_for_displacement_rates/coherence_weighted_rate_inversions.py`
<br><br>

## Producing Figures 13-18, S2-S4

### Figures 13-14
*Rates inverted unweighted and weighted using two coherence methods, and rate differences between all three combinations* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_13-14_rates_maps_and_rate_diffs/Figs_13-14_rates_and_rate_diffs.ipynb`
<br><br>

### Figures 15 and S2
*Displacement rate histograms* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_15_S2_rate_histograms/Figs_15_S2_rate_histograms.ipynb`
<br><br>

### Figures 16-17
*Plots of percent non-vegetated ground (NVG) pixels* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_16-17_percent_NVG_plots/Figs_16_17_percent_NVGs_plots.ipynb`
<br><br>

### Figure 18
*Zoom-in to Focus Area A with diagram from Spreckels sugar factory and Google Earth image of the retention ponds* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_18_focus_area_A_zoomin/Fig_18_focus_area_A_zoomin.ipynb` 
<br><br>

### Figures S3-S4
*Synthetic data tests*
<br><br>
- Run this notebook: `/3_Making_figures/Figure_S3-S4_synthetic_data_tests/Figs_S3_S4_synthetic_tests.ipynb`

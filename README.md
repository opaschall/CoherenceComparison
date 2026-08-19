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
<p align="center">
<img width="50%" alt="SH_basemap_higher_res_test" src="https://github.com/user-attachments/assets/c4c82bc5-b9d4-436d-be2f-ab8d661ad988" />
</p>

### Figure 2: 
*Synthetic time series inversion example* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_2_synthetic_inversion/Fig_2_synthetic_rate_inversion.ipynb`
<p align="center">
<img width="60%" alt="synth_inversion_example" src="https://github.com/user-attachments/assets/3b2bc3ff-f9c6-49eb-9a3e-fd536e4b7e5d" />
</p>

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
<p align="center">
<img width="50%" alt="desert_urban_veg_mask" src="https://github.com/user-attachments/assets/34a5f9a1-727f-47fe-9453-fff490e6d732" />
</p>

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
<p align="center">
<img width="80%" alt="avg_cohs" src="https://github.com/user-attachments/assets/a64982ec-d8af-4360-a5a4-10df55275c88" />
<img width="40%" alt="coh_heatmap" src="https://github.com/user-attachments/assets/a558f71b-abe2-47cc-91d5-5f2e59938aee" /> <br>
<img width="50%" alt="coh_diffs" src="https://github.com/user-attachments/assets/00fd3e77-b1d7-4033-86fa-a1c78d9ef845" />
</p>
<br><br>
- To produce Figure S1, run this notebook: `/3_Making_figures/Figure_4-6_S1_coherence_diffs/Fig_S1_coherence_diffs_histograms.ipynb`
<br>
<p align="center">
<img width="80%" alt="Supp_hists_masks" src="https://github.com/user-attachments/assets/315f846e-aa6b-40a7-ab01-df09832de9d8" />
</p>

### Figures 7-12
*USDA Cropland Data Layer (CDL) map of our region of interest, and focus areas with four panels each* 
<br><br>
- To produce Figures 7-12, run this notebook: `/3_Making_figures/Figure_7-12_CDL_map_and_focus_areas/Fig_7_8-12_CDL_map_and_focus_areas.ipynb`
<p align="center">
  <img width="50%" alt="crop_map" src="https://github.com/user-attachments/assets/abab97d6-7e53-40db-8ecd-3eaae42f9bb5" /> <br>
  <img width="30%" alt="focus_area_A_imperial_road" src="https://github.com/user-attachments/assets/9776ab12-345d-4d8e-affe-dcea41c8a8d7" />
  <img width="30%" alt="focus_area_B_pools" src="https://github.com/user-attachments/assets/9517e6a4-9809-4497-9d36-674bf36dcf61" />
  <img width="70%" alt="focus_area_C_transect_roads" src="https://github.com/user-attachments/assets/52560362-02d7-4ad1-9918-e2215ed32cac" />
  <img width="30%" alt="focus_area_D_imperial_airport" src="https://github.com/user-attachments/assets/fff218d5-c767-4fdb-b066-6a38573a8f03" />
  <img width="30%" alt="focus_area_E_ElCentro_airport" src="https://github.com/user-attachments/assets/83e5878d-e2cd-433c-936d-5a00f0f4be20" />
</p>

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
<p align="center">
  <img width="80%" alt="disp_rates" src="https://github.com/user-attachments/assets/7b220cb1-ddb4-4193-9b4c-378903cbbe84" />
  <img width="80%" alt="disp_rate_diffs" src="https://github.com/user-attachments/assets/718fa676-a15d-4a6c-87d2-09739f82d402" />
</p>

### Figures 15 and S2
*Displacement rate histograms* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_15_S2_rate_histograms/Figs_15_S2_rate_histograms.ipynb`
<p align="center">
  <img width="50%" alt="hists_rates_all_focus_areas_same_set_of_pixels" src="https://github.com/user-attachments/assets/c10af762-8ac7-4a2a-892f-a3d408c7ca71" /> <br>
  <img width="50%" alt="hists_focus_areas" src="https://github.com/user-attachments/assets/4193f9d9-e366-4a12-9b8a-658934e2e7f3" />
</p>  

### Figures 16-17
*Plots of percent non-vegetated ground (NVG) pixels* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_16-17_percent_NVG_plots/Figs_16_17_percent_NVGs_plots.ipynb`
<p align="center">
  <img width="60%" alt="NVGs_captured_all_areas" src="https://github.com/user-attachments/assets/96862c30-d8c0-47b3-99aa-5fc5d609cc44" /> <br>
  <img width="60%" alt="NVGs_captured_by_area" src="https://github.com/user-attachments/assets/303c520f-0029-4788-86da-588493d6617a" />
</p>  

### Figure 18
*Zoom-in to Focus Area A with diagram from Spreckels sugar factory and Google Earth image of the retention ponds* 
<br><br>
- Run this notebook: `/3_Making_figures/Figure_18_focus_area_A_zoomin/Fig_18_focus_area_A_zoomin.ipynb` which produces panels (a) and (b) of the figure. Panels (c) and (d) are from a technical report (put link here) and from Google Earth, respectively.
<p align="center">
  <img width="50%" alt="Annotated_retention_pond" src="https://github.com/user-attachments/assets/dd1ca72e-0b1a-4fea-b317-bc3de4c5ce0e" />
</p>  

### Figures S3-S4
*Synthetic data tests*
<br><br>
- Run this notebook: `/3_Making_figures/Figure_S3-S4_synthetic_data_tests/Figs_S3_S4_synthetic_tests.ipynb`
<p align="center">
  <img width="45%" alt="synthetic_test_window_sizes" src="https://github.com/user-attachments/assets/7444ed01-5657-4789-8f11-d5ddc5f25ef4" />
  <img width="80%" alt="synthetic_test_bright_dark" src="https://github.com/user-attachments/assets/e3867ac5-4eea-4a40-ab12-bd7a11377195" />
</p>  

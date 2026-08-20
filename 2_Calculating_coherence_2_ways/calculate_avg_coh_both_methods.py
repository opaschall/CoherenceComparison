#import necessary packages
import os,sys
import glob
import pandas as pd
from osgeo import gdal
import datetime 
from datetime import datetime
from datetime import timedelta
from dateutil import parser
import numpy as np
from scipy.ndimage import gaussian_filter 

# set the driver first, only do once.
driver=gdal.GetDriverByName('ISCE')

#define working directory 
# these may be different for another user, must update
workdir = '/data/ocp4/SuperstitionHills/Data_and_Figs/cropped_20000_2475_9000_1575/'  #subfolder in SuperstitionHills
SLCdir = 'VV/merged/SLC/'  #need to define dates
cohdir = 'VV/merged/coherence/'  

# size of SLCs/coherence images
x1 = 0; y1= 0    #coord values are 0 if interferogram has already been cropped
dx= 9000; dy=1575

print(dx,dy)

# load in dates, make sure they are in order
dates = [os.path.basename(x) for x in glob.glob(workdir+SLCdir+'*')] 
dates = sorted(dates)
nd = len(dates); print(nd)
numIgrams = nd - 1

# set the folders to where coherence files are saved 
window1dir = 'method1/'
window2dir = 'method2/'
save1dir = workdir + cohdir + window1dir
save2dir = workdir + cohdir + window2dir

# initialize arrays for average coherence values
avg_coh1 = np.ndarray((dy,dx),dtype='float') 
avg_coh2 = np.ndarray((dy,dx),dtype='float') 
# initialize array for coherence time series at an individual pixel
temp_coh1 = np.ndarray((numIgrams,),dtype='float')
temp_coh2 = np.ndarray((numIgrams,),dtype='float')

# loop over each pixel and each interferogram, pull out coherence magnitudes over entire time span, calculate the average
for y in range(dy):     
    for x in range(dx): 
        # loop through coh files and calculate std for that pixel
        for i in range(numIgrams):
            date1 = dates[i]; date2 = dates[i+1]

            # METHOD 1: complex coherence magnitude
            fileName = gdal.Open(save1dir+"coh_"+date1+"_"+date2+"_method1.r4", gdal.GA_ReadOnly)
            temp_coh1[i] = fileName.GetRasterBand(1).ReadAsArray(x,y,1,1)[0,0]

            # METHOD 2: unit vector coherence magnitude
            fileName = gdal.Open(save2dir+"coh_"+date1+"_"+date2+"_method2.r4", gdal.GA_ReadOnly)
            temp_coh2[i] = fileName.GetRasterBand(1).ReadAsArray(x,y,1,1)[0,0]

        # calculate the averages across all times
        avg_coh1[y,x] = np.nanmean(temp_coh1)
        avg_coh2[y,x] = np.nanmean(temp_coh2)

    # print an update every row
    print('Row '+str(y)+' weighted inversions done.')

print('Avg coh (both methods) calculated for all pixels.')

# save them
driver = gdal.GetDriverByName('ISCE')

# This is where I saved it, but this is updated to save locally so it can be more easily loaded in to produce figures.
# saveDir_avg = '/data/ocp4/SuperstitionHills/Data_and_Figs/coherence/comparing_coh_methods/AverageCohImages/'

# save method 1
fileName1 = 'avg_coh_method1.r4'
colds = driver.Create(fileName1,dx,dy,1,gdal.GDT_Float32)
colds.GetRasterBand(1).WriteArray(avg_coh1)
colds=None

# save method 2
fileName2 = 'avg_coh_method2.r4'
colds = driver.Create(fileName2,dx,dy,1,gdal.GDT_Float32)
colds.GetRasterBand(1).WriteArray(avg_coh2)
colds=None
print('Averages Saved!')

print('Producing files with coherence method 1: complex coherence magnitude')

# Run times: 
# 52638.7591 sec on Oct. 6, 2025
# 52569.2520 sec on Oct. 8, 2025
# 52087.1724 sec on Nov. 12, 2025
# 51903.9295 sec on Jul. 27, 2026

#import necessary packages 
import os
import glob
from osgeo import gdal
import numpy as np
import time   #to see if Method 1 is less efficient than Method 3

# Start the timer
start_time = time.time()

# define working directory 
# these may be different for another user, must update
workdir = '/data/ocp4/SuperstitionHills/Data_and_Figs/cropped_20000_2475_9000_1575/'  #subfolder in SuperstitionHills
SLCdir = 'VV/merged/SLC/'
cohdir = 'VV/merged/coherence/'  

# size of SLCs
x1 = 0; y1= 0    #values are 0 if interferogram has already been cropped
dx= 9000; dy=1575

# load in dates, make sure they are in order
dates = [os.path.basename(x) for x in glob.glob(workdir+SLCdir+'*')] 
dates = sorted(dates)
nd = len(dates)
numIgrams = nd - 1

#METHOD 1: Complex coherence magnitude
# start with array of nans so that we can see if the calculation failed for any pixels
coh1 = np.ndarray((dy,dx),dtype='float')*np.nan

# window to calculate coherence over
alooks=4; rlooks=20 # x is range, y is azimuth 

# set the driver first, only do once.
driver=gdal.GetDriverByName('ISCE')

# set the folder to save these coh files to 
windowdir = 'method1/'
save1dir = workdir + cohdir + windowdir  #correct save1dir
# this one was just for testing the run time:
# save1dir = '/data/ocp4/SuperstitionHills/Data_and_Figs/dummy_coherence/method_1_files/'

# loop through the dates 
for i in range(numIgrams):     #for now try with 3   #(numIgrams): #numIgrams if doing all of them at once
    # define the 2 dates. 
    date1=dates[i]
    date2=dates[i+1]
    print(date1); print(date2); print(i)

    # Read in 2 full SLCs to make interferogram 
    # have to load in more than just the pixels of interest to calculate coh at edge pixels 
   
    ds = gdal.Open(workdir+SLCdir+date1+"/"+date1+".slc.full", gdal.GA_ReadOnly)
    slc1 = ds.GetRasterBand(1).ReadAsArray(x1,y1,dx,dy)
    print('SLC 1 loaded.')
    ds = gdal.Open(workdir+SLCdir+date2+"/"+date2+".slc.full", gdal.GA_ReadOnly)
    slc2 = ds.GetRasterBand(1).ReadAsArray(x1,y1,dx,dy)
    print('SLC 2 loaded.')

    aa = slc1*np.conj(slc1)
    bb = slc2*np.conj(slc2)
    ab = slc1*np.conj(slc2)   

    for y in np.arange(int(alooks/2),dy-int(alooks/2),1): # started with this: np.arange(y2,y1,1)
        for x in np.arange(int(rlooks/2),dx-int(rlooks/2),1): # started with this: np.arange(x2,x1,1)
            # calculate coherence using this formula: <ab*>/sqrt(<aa*><bb*>)
            aa_temp = (np.mean(aa[int(y-alooks/2):int(y+alooks/2),int(x-rlooks/2):int(x+rlooks/2)]))
            bb_temp = (np.mean(bb[int(y-alooks/2):int(y+alooks/2),int(x-rlooks/2):int(x+rlooks/2)]))
            ab_temp = (np.mean(ab[int(y-alooks/2):int(y+alooks/2),int(x-rlooks/2):int(x+rlooks/2)]))
            # magnitude (abs) of complex coherence
            coh1[y,x] = np.abs(ab_temp/np.sqrt(aa_temp*bb_temp))
  
    # save it       
    save_file_name = 'coh_'+str(date1)+'_'+str(date2)+'_method1.r4'

    # For timing purposes, can save to a temporary file that gets overwritten each time 
    # save_file_name = 'coh_temp_method1.r4' # goes to the dummy folder 
    # colds = driver.Create(save_file_name,dx,dy,1,gdal.GDT_Float32) # putting in local folder, temporary

    colds = driver.Create(save1dir + save_file_name,dx,dy,1,gdal.GDT_Float32)
    colds.GetRasterBand(1).WriteArray(coh1)
    colds=None
    print('coh for igram '+str(i)+' done and saved.')
    
print('Complex coherence magnitude calculated for every igram for every pixel.')

# End the timer - calculated elapsed time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time method 1: {elapsed_time:.4f} seconds")
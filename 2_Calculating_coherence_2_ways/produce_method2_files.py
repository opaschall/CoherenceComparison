print('Producing files with coherence method 2: unit vector coherence')

# Run times: 
# 22341.2450 sec on Oct. 7, 2025
# 21734.9599 sec on Nov. 13, 2025
# 22565.9906 sec on Jul. 29, 2026

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

#METHOD 2: Unit vector coherence magnitude
# start with array of nans so that we can see if the calculation failed for any pixels 
coh2 = np.ndarray((dy,dx),dtype='float')*np.nan    

# window to calculate coherence over
alooks=4; rlooks=20 # x is range, y is azimuth 

# set the driver first, only do once.
driver=gdal.GetDriverByName('ISCE')

# set the folder to save these coh files to 
windowdir = 'method2/'
save2dir = workdir + cohdir + windowdir
# this one was just for testing the run time:
# save2dir = '/data/ocp4/SuperstitionHills/Data_and_Figs/dummy_coherence/method_2_files/'

# loop through the dates 
for k in range(numIgrams):     
    # define the 2 dates. 
    date1=dates[k]
    date2=dates[k+1]

    # Read in 2 full SLCs to make interferogram 
    # have to load in more than just the pixels of interest to calculate coh at edge pixels 
    ds = gdal.Open(workdir+SLCdir+date1+"/"+date1+".slc.full", gdal.GA_ReadOnly)
    slc1 = ds.GetRasterBand(1).ReadAsArray(x1,y1,dx,dy)
    ds = gdal.Open(workdir+SLCdir+date2+"/"+date2+".slc.full", gdal.GA_ReadOnly)
    slc2 = ds.GetRasterBand(1).ReadAsArray(x1,y1,dx,dy)

    ab = slc1*np.conj(slc2)  #need to add this back in so it isn't taking ab from method 1
    for y in np.arange(int(alooks/2),dy-int(alooks/2),1): 
            for x in np.arange(int(rlooks/2),dx-int(rlooks/2),1): 
                ab_subset = ab[int(y-alooks/2):int(y+alooks/2),int(x-rlooks/2):int(x+rlooks/2)]
                ab_norm = ab_subset/np.abs(ab_subset)
                coh2[y,x] = np.abs(np.mean(ab_norm))

    # save it        
    save_file_name = 'coh_'+str(date1)+'_'+str(date2)+'_method2.r4'

    # For timing purposes, can save to a temporary file that gets overwritten each time 
    # save_file_name = 'coh_temp_method2.r4' # goes to the dummy folder 
    # colds = driver.Create(save_file_name,dx,dy,1,gdal.GDT_Float32) # putting in local folder, temporary

    colds = driver.Create(save2dir + save_file_name,dx,dy,1,gdal.GDT_Float32)
    colds.GetRasterBand(1).WriteArray(coh2)
    colds=None
    print('coh for igram '+str(k)+' done and saved.')
    
print('Unit vector coherence magnitude calculated for every igram for every pixel.')

# End the timer - calculated elapsed time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time method 2: {elapsed_time:.4f} seconds")
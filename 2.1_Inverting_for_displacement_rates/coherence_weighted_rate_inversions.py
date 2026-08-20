#IMPORT STUFF
import os,sys
import glob
from osgeo import gdal
from datetime import datetime
import numpy as np
from weighted_rate_inversion import weighted_rate_inversion

# Need this function to convert datetime objects to decimal years. Got this off of stackexchange. 
def datetime2year(dt): 
    year_part = dt - datetime(year=dt.year, month=1, day=1)
    year_length = (
        datetime(year=dt.year + 1, month=1, day=1)
        - datetime(year=dt.year, month=1, day=1)
    )
    return dt.year + year_part / year_length

#DEFINE DIRECTORIES, needs to be updated for specific project
workdir = '/data/ocp4/SuperstitionHills/Data_and_Figs/'  
cropdir = 'cropped_20000_2475_9000_1575/'  
fullResdir = '/data/ocp4/SuperstitionHills/Data_and_Figs/fullRes_unwrapped_interferograms/' # using full resolution unwrapped interferograms
unfiltUnwrappedDir = fullResdir + 'unfilt_unwrapped/'

#load in all dates from all SLCs currently downloaded (only for VV)
dates = [os.path.basename(x) for x in glob.glob(workdir+cropdir+'VV/merged/SLC/'+"/2*")] 
dates = sorted(dates)
num_dates = len(dates)
print(dates)
print(num_dates)
num_igrams = num_dates-1

#convert dates to datetime objects --> then to decimal dates
# convert to datetime objects 
slc_dates=[]
for i in range(0,len(dates)):
    slc_dates.append(datetime.strptime(str(dates[i]).replace('\n',''), '%Y%m%d'))
igram_dates = slc_dates[1::]

# convert to floats
slc_dates_floats = np.ndarray((num_dates,1),dtype='float')
for i in range(num_dates):
    slc_dates_floats[i] = datetime2year(slc_dates[i]) # now an array of floats in years

#define dimensions of each SLC
x1 = 0; y1= 0    #values are 0 if interferogram has already been cropped
dx= 9000; dy=1575  #actual dimensions

#ZOOM IN COORDS
#zooming in on the road going out of imperial into the top right corner
# these are set up: [x_right, y_top, x_left, y_top]
imperial_road = [6820, 100, 7520, 450]   
#transect roads (NS roads east of Imperial) 
transect_roads = [4500, 650, 6600, 1000]      
#el-centro naval base airport
ElCentro_airport = [4575, 980, 5275,1265]     
#pools in top right
pools = [7700,300, 8400, 650]     
#zoom in to Imperial airport and outside city
imperial_airport = [6600,800,7300,1075]   

#CREATE MASK
box_mask = np.zeros((dy,dx),dtype=float)

for y in range(dy):
    for x in range(dx):
        if x>=imperial_road[0] and x<=imperial_road[2] and y<=imperial_road[3] and y>=imperial_road[1]:
            box_mask[y,x] = 1
        if x>=transect_roads[0] and x<=transect_roads[2] and y<=transect_roads[3] and y>=transect_roads[1]:
            box_mask[y,x] = 2
        if x>=ElCentro_airport[0] and x<=ElCentro_airport[2] and y<=ElCentro_airport[3] and y>=ElCentro_airport[1]:
            box_mask[y,x] = 4
        if x>=pools[0] and x<=pools[2] and y<=pools[3] and y>=pools[1]:
            box_mask[y,x] = 5
        if x>=imperial_airport[0] and x<=imperial_airport[2] and y<=imperial_airport[3] and y>=imperial_airport[1]:
            box_mask[y,x] = 6

#need to flip box_mask left-right (currently have pixel coordinates saved for plotting not actual array coordinates)
box_mask = np.fliplr(box_mask)

# define the reference pixel coordinates
yR = int(1559)  
xR = int(9000 - 130) 

#REFERENCE
ref_phs = np.ndarray((num_dates-1,),dtype='float')
intDir = unfiltUnwrappedDir
for i in range(num_igrams): #for whole time period    #something about this not working
    date1 = dates[i]
    date2 = dates[i+1]

    int_premade = gdal.Open(intDir+date1+"_"+date2+'_'+"unfilt.unw", gdal.GA_ReadOnly)
    int_temp = int_premade.GetRasterBand(1).ReadAsArray(xR,yR,1,1)

    ref_phs[i] = int_temp[0,0]

driver=gdal.GetDriverByName('ISCE')

#LOOP THROUGH ALL POINTS
# point to correct directories - this will need updating according to the project the user is working on.
igramsDir =  intDir
cohDir_m1 =  workdir + cropdir + 'VV/merged/coherence/method1/'
cohDir_m2 =  workdir + cropdir + 'VV/merged/coherence/method3/'

phs_vals = np.ndarray((num_igrams,),dtype='float')
temp_coh_1 = np.ndarray((num_igrams,),dtype='float')
temp_coh_2 = np.ndarray((num_igrams,),dtype='float')
t = slc_dates_floats[1::].reshape((num_igrams,))

rates_coh_1 = np.ndarray((dy,dx), dtype='float')*np.nan 
rates_coh_2 = np.ndarray((dy,dx), dtype='float')*np.nan 

for y in range(dy):  
    for x in range(dx):
        if box_mask[y,x] > 0:
            #print('y: '+str(y)+'  x: '+str(x)) 
            for i in range(num_igrams): # for whole time period
                date1 = dates[i]
                date2 = dates[i+1]

                # load in igram disps for this pixel 
                igramFile = igramsDir+date1+'_'+date2+'_unfilt.unw'
                ds = gdal.Open(igramFile,gdal.GA_ReadOnly)
                phs_vals[i] = ds.GetRasterBand(1).ReadAsArray(x,y,1,1)[0,0]
                reffed_phs = phs_vals - ref_phs     
    
                # load in coherence values for this pixel -- complex coherence magnitude
                cohFile_1 = 'coh_'+date1+'_'+date2+'_method1.r4'
                ds = gdal.Open(cohDir_m1+cohFile_1, gdal.GA_ReadOnly)
                temp_coh_1[i] = ds.GetRasterBand(1).ReadAsArray(x,y,1,1)[0,0]

                # load in coherence values for this pixel -- unit vector coherence
                cohFile_3 = 'coh_'+date1+'_'+date2+'_method3.r4'
                ds = gdal.Open(cohDir_m2+cohFile_3, gdal.GA_ReadOnly)
                temp_coh_2[i] = ds.GetRasterBand(1).ReadAsArray(x,y,1,1)[0,0]

            #calculate weighted rate - use the function defined in the other file
            weighted_rate_1 = weighted_rate_inversion(slc_dates_floats,reffed_phs,temp_coh_1)
            weighted_rate_2 = weighted_rate_inversion(slc_dates_floats,reffed_phs,temp_coh_2)
         
            rates_coh_1[y,x] = weighted_rate_1
            rates_coh_2[y,x] = weighted_rate_2


    # print an update every 10 rows
    if(y!=0 and np.remainder(y,50)==0):   #change to every 50 rows
        print('Row '+str(y)+' weighted inversions done.')
    
#SAVE IMAGES
# set the driver first, only do once.
driver=gdal.GetDriverByName('ISCE')

file_name_1 = '/mnt/data/SuperstitionHills/Data_and_Figs/rate_maps/coh_1_weighted_rate_map.r4'  #change
print(file_name_1)
colds = driver.Create(file_name_1,dx,dy,1,gdal.GDT_Float32)
colds.GetRasterBand(1).WriteArray(rates_coh_1) # this is in rad/yr
colds=None

file_name_3 = '/mnt/data/SuperstitionHills/Data_and_Figs/rate_maps/coh_2_weighted_rate_map.r4' #change
print(file_name_3)
colds = driver.Create(file_name_3,dx,dy,1,gdal.GDT_Float32)
colds.GetRasterBand(1).WriteArray(rates_coh_2) # this is in rad/yr
colds=None

print('Weighted rates, using both coherence methods, for all pixels inverted and saved.')
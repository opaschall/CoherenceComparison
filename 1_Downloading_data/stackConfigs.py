#!/usr/bin/env python3

import numpy as np

# this is how many images you want to work on in a single batch. 
#   Can't always do them in one go (because if it fails, you have wasted lots of time)
targetNumDates = 100 # this works for me but I have to be pretty confident the run will not fail 
#                      to commit to downloading 100 SLCs at a time 

# This is the folder where everything will go. 
workdir  = '/mnt/data/SuperstitionHills/Data_and_Figs' # make sure this exists
dem      = '/mnt/data/SuperstitionHills/Data_and_Figs/DEM/demLat_N32_N33_Lon_W116_W115.dem.wgs84' #make sure this exists too! 
#replace with your DEM! (DEM must include whole polygon and have to go in specific increments - whole num lat,long?)

# From ASF Vertex in top panel/search options area:
polygon = "&intersectsWith=POLYGON((-115.8836 32.8054,-115.523 32.8054,-115.523 32.9841,-115.8836 32.9841,-115.8836 32.8054))"
# Also referred to as "relative orbit" 
track   = "&relativeOrbit=173" 

# Start and end dates of stack 
date1   = '&start=2018-06-10'  # start of search date period
date2   = '&end=2025-01-26'    # end of search date period
pltdate = '20180610_20180622'  # pair that you will plot in a later step. Needs to be real dates from your stack!

rlooks     = 10 # range looks
alooks     = 3  # azimuth looks
nconnect   = 3  # how many int. connections to make 
noverlap   = 1  # used in ESD
looks      = ' -r '+str(rlooks)+' -z '+str(alooks)+' ' # final looks of your large-area interferograms
swaths     = ' -n \'1 2\''    # list of swaths if you know you only need one or two, otherwise all.
connects   = ' -c '+str(nconnect)+' ' # number of interferogram connections
nESD       = ' -O '+str(noverlap)+' ' # number overlaps used in ESD

# This is the area you want to use to select bursts but may need be adjusted after your first iteration of stackSentinel_VH
# This is my larger area/poly for now, used for plotting to check if download/coregistration worked properly.
narrowpoly = ' -b \'32.8387 32.9525 -115.8258 -115.5585\' '

# This is what you will eventually crop your image to.
# Come back once you have run run_all.ipynb once to narrow in on what polygon(s) you want to crop to.
croppoly = np.array([[2000*rlooks, 825*alooks, 900*rlooks, 525*alooks]]) # xstart,ystart,dx,dy

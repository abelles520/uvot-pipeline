import numpy as np
import sys

# edit below to specify where the UVOT data analysis packages are located
# The below may not work due to the removal of the hypen in between uvot and download.
sys.path.append('uvotdownload/uvotdownload')

from download_heasarc import download_heasarc as download

import glob


from query_heasarc import query_heasarc as query

# The query function takes either a str or a text file and queries the archive to get a list of the different UVOT
# observations that exist. Running this function will create directories with the name of each target and create a
# file that specifies the obsid of all available data. This file is then used to download the actual data.

query("names.txt", list_opt=True, search_radius=17,
      table_params=['obsid','uvot_expo_w2','uvot_expo_m2','uvot_expo_w1', 
                    'uvot_expo_uu', "uvot_expo_bb", 'uvot_expo_vv'],
       create_folder=True)


download_files = glob.glob('*/heasarc_obs.dat')

print(download_files)

# This downloaded the queried data and unzips the data as well. Depending on the volume of data being downloaded, 
# it is important to be cognizant of the amount of available storage space. If only specific filters are of
# interest, the download_filters list can be edited. The min_exp argument specifies the minimum length of an 
# observation that is downloaded. This won't have a large impact but is set at 200 s to avoid any SIP segments.

download(download_files, unzip=True, download_all=True,
         download_filters=['w2','m2','w1','uu','bb','vv'], min_exp=200)

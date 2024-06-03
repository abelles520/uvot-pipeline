import numpy as np
import sys

sys.path.append('uvotdownload/uvotdownload')

from download_heasarc import download_heasarc as download

import glob

'''
from query_heasarc import query_heasarc as query

query("names.txt", list_opt=True, search_radius=17,
      table_params=['obsid','uvot_expo_w2','uvot_expo_m2','uvot_expo_w1', 
                    'uvot_expo_uu', "uvot_expo_bb", 'uvot_expo_vv'],
       create_folder=True)
'''

download_files = glob.glob('*/heasarc_obs.dat')

print(download_files)

download(download_files, unzip=True, download_all=True,
         download_filters=['w2','m2','w1','uu','bb','vv'], min_exp=200)
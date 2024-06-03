import sys, os
import glob 
import numpy as np
from astropy.io import fits
import pandas as pd 

sys.path.append('uvot-galphot/uvot-galphot')

from surface_phot import surface_phot
from make_aperture_image import make_aperture_image
from phot_plot import phot_plot

# add optical bands info

zeropt_dict = {'w1': 18.95,'w2': 19.11,'m2': 18.54, 'uu':19.36, 'bb':18.98, 'vv':17.88}
zeropt_err = 0.03  # mags

def phot(name, ra, dec, a, b, pa, mask):

    ap = 1
   
    os.chdir(name)

    print('\nStarting {}....\n'.format(name))

    offset_annphot = []
    nonoffset_annphot = []

    # perform check that files exist

    ex_files = glob.glob(name+'_??_ex.fits')

    filts = [name.split('_')[1] for name in ex_files]


    for filt in filts:
        # perform phot for each filter
        print(filt)

        # nonoffset
        # change _corr_ to _

        try:
            surface_phot(name+'_corr_'+filt+'_', ra, dec, a, b, pa,
                     2, zeropt_dict[filt], zeropoint_err=zeropt_err,
                     aperture_factor=ap, sky_aperture_factor=1.0,
                     mask_file=mask, offset_file=False,
                     verbose=False)
        except OSError as e:
            print(e)
            continue

        nonoffset_annphot.append(name+'_corr_'+filt +'_')

       
        # offset
        # change _corr_offset_ to _offset_
        try:
            surface_phot(name+'_corr_offset_'+filt+'_', ra, dec, a, b, pa,
                     2, zeropt_dict[filt], zeropoint_err=zeropt_err,
                     aperture_factor=ap, sky_aperture_factor=1.0,
                     mask_file=mask, offset_file=True,
                     verbose=False)
        except OSError as e:
            print(e)
            continue

        offset_annphot.append(name+'_corr_offset_'+filt +'_')

    offset_ann = [i+'phot_annprofile.dat' for i in offset_annphot]
   
    nonoffset_ann = [i+'phot_annprofile.dat' for i in nonoffset_annphot]

    offset_tot = [i+'phot_totprofile.dat' for i in offset_annphot]
    nonoffset_tot = [i+'phot_totprofile.dat' for i in nonoffset_annphot]

   
    phot_plot(offset_ann, offset_tot,
              filts, name+'_corr_offset_phot_plot.png',
              color_list=None,
              asym_mag_list=None)
   
    phot_plot(nonoffset_ann, nonoffset_tot,
              filts, name+'_corr_phot_plot.png',
              color_list=None,
              asym_mag_list=None)

    # make aperture image
    make_aperture_image(name+'_corr_offset_', filts,
                        ra, dec, 2*a, 2*b, pa)

    os.chdir('..')


if __name__=='__main__':
    df = pd.read_csv('gal_info.txt', delim_whitespace=True, header=None)
    df.columns = ['Name', 'RA', 'Dec', 'a', 'b', 'PA']
    issues = []
    for ind, row in df.iterrows():
        maskfile = f"/Users/alex/Documents/nearby_ulxs/masks/{row['Name'].lower()}_nuv_gauss7p5_stars.reg"
        try:
            phot(row['Name'], row['RA'], row['Dec'], row['a'], row['b'], row['PA']+90,  maskfile) # None)#
        except Exception as e:
            print(e)
            issues.append(row['Name']+str(e))
            os.chdir('/Users/alex/Documents/nearby_ulxs')
        break
    print(issues)

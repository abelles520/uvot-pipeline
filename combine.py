import sys, os
import glob 
import numpy as np
from astropy.io import fits
import datetime
import subprocess
import traceback
import pdb

sys.path.append('uvot-mosaic/uvot-mosaic')

from uvot_deep import uvot_deep
from offset_mosaic import offset_mosaic

# run uvot deep on all images
# apply sens loss correction
# uvotimsum 
# offset_mosaic

# sensitivity loss using the look-up table

def apply_sens_loss_corr(cr, date, filt):
    """
    inputs:
    cr - float or array that contains count rate information, it will be
         multipled by a correction factor
    date - string denoting date that data was taken
    filt - string that denotes which Swift/UVOT filter to correct 
    
    returns:
    cr_corr - float or array that contains the corrected 
    """
    
    data_date = datetime.datetime.strptime(date.split('T')[0], '%Y-%m-%d')
    start_date = datetime.datetime(2005,1,1)
    
    difference = data_date-start_date
    duration_in_s = difference.total_seconds()
    t = duration_in_s/(365.25*24*60*60) # total seconds in a year
        
    # use look up table corresponding to filt
    if filt in ['w2', 'm2', 'w1']:
        corr_file = glob.glob('/Users/alex/Documents/nearby_ulxs/correction_factors_'+filt+'.txt')

        df = np.loadtxt(corr_file[0]).T
        t_array = df[0]
        factor_array = df[2]

        factor = np.interp(t, t_array, factor_array)
    elif filt=='bb': 
        #1/(1-R*t), t is years since launch
        R = 0.0092
        factor = 1/(1-R*t)
    elif filt=='uu':
        R = 0.0099
        factor = 1/(1-R*t)
    elif filt=='vv':
        # quadratic
        c1 = -0.0184223
        c2 = 0.00469391
        factor = 1/(1+c1*t+c2*t**2)
    else:
        print(filt)

    return cr*factor

def sens_loss(name):

    os.chdir(name)

    print('Sensitivity loss correction for {}'.format(name))

    sk_all = glob.glob(name+'_??_sk_all.fits')

    for i in sk_all:
        file = fits.open(i)
        corr_hdu_list = fits.HDUList()
        for hdu in file:
            # save primary HDU
            if isinstance(hdu, fits.hdu.image.PrimaryHDU):
                corr_hdu_list.append(hdu)
                continue
            # for image HDU, create copy and modify
            tmp_copy = hdu.copy()
            date = hdu.header['DATE-OBS']
            filt = hdu.header['FILTER']
            if filt in ['U', 'B', 'V']:
                filt = filt.lower()*2
            else:
                filt = filt[2:].lower()

            updated_cr = apply_sens_loss_corr(tmp_copy.data, date, filt)
           
            tmp_copy.data = updated_cr
           
            corr_hdu_list.append(tmp_copy)

        new_name = file.filename().split('_')
        new_name.insert(1, 'corr')
        new_name = '_'.join(new_name)
        corr_hdu_list.writeto(str(new_name), overwrite=True)
        file.close()
        corr_hdu_list.close()
        # sum counts image and exposure image with same prefix
        # counts image
        tmp = str(new_name).split('_')
        tmp.remove('sk')
        tmp.remove('all.fits')
        tmp.append('sk.fits')
        out_sk = '_'.join(tmp)
       
        cmd = 'uvotimsum infile=' + str(new_name) + ' outfile=' +str(out_sk) +' exclude=none clobber=yes'
        subprocess.run(cmd, shell=True)

        # exposure map
        # create symlinks for ex_all and summed ex file
        # only the counts image gets scaled for the sensitivity loss

       
        tmp = str(out_sk).split('_')
        tmp.remove('sk.fits')
        tmp.append('ex.fits')
        ex_corr = '_'.join(tmp)
        tmp = ex_corr.split('_')
        tmp.remove('corr')
        tmp.remove('ex.fits')
        tmp.append('ex_all.fits')
        ex_all = '_'.join(tmp)
       
        tmp = ex_all.split('_')
        tmp.insert(1,'corr')
        ex_all_corr = '_'.join(tmp)
        # make symlink for ex_all file
        cmd = 'ln -sf {} {}'.format(ex_all, ex_all_corr)
        subprocess.run(cmd, shell=True)

        tmp = ex_corr.split('_')
        tmp.remove('corr')
        ex = '_'.join(tmp)
        # make symlink for ex file
        cmd = 'ln -sf {} {}'.format(ex, ex_corr)
        subprocess.run(cmd, shell=True)

    os.chdir('..')

def stack(name, mask):
   
    os.chdir(name)
    # use offset mosaic on corrected images
   
    prefix = name + '_corr'

    ex_files = glob.glob(f'{name}_??_ex.fits')

    filts = [name.split('_')[1] for name in ex_files]

    #try:
    offset_mosaic(prefix+'_', prefix+'_offset_', filts,
                                            min_exp_w2=50, min_exp_m2=50, min_exp_w1=50, restack_id=True, mask_file=mask)
    #except Exception as error:
    #    print(error)
    #    pdb.set_trace()
    #    print(traceback.print_exc())
   
    # use offset mosaic on noncorrected images
    prefix = name
    try: #make sure this does run again
        offset_mosaic(prefix+'_', prefix+'_offset_', filts,
                                            min_exp_w2=50, min_exp_m2=50, min_exp_w1=50, restack_id=True, mask_file=mask)
    except Exception as error:
        print(error)
        print(traceback.print_exc())
        pdb.set_trace()
   

    os.chdir('..')




if __name__=='__main__':
    gals = glob.glob('n*/')

    for gal in gals[1:]:
        #os.chdir(gal)
        #obs_id = glob.glob('0*')

        #uvot_deep(obs_id, f'{gal[:-1]}_')
        #os.chdir('..')

        #sens_loss(gal[:-1])  
        maskfile = f"/Users/alex/Documents/nearby_ulxs/masks/{gal[:-1]}_nuv_gauss7p5_stars.reg"
        stack(gal[:-1], mask=maskfile)

# uvot-pipeline
Repo with example scripts for downloading, processing, and measuring photometry from Swift/UVOT data

### Requirements  

These scripts can be used to run the [UVOT-data-analysis](https://github.com/UVOT-data-analysis/) repos written by Lea Hagen (see my own forks for slight modifications and changes). To run, these scripts must be pointed to the installation of uvot-download, uvot-mosaic, and uvot-galphot. These also require the [HEAsoft](https://heasarc.gsfc.nasa.gov/docs/software/heasoft/download.html) tools to be installed. 

The requirements.txt file in this repo should have the packages and version numbers of the required packages. The code has not been tested with newer versions of various packages and may not be compatible with previous versions as well. 

### Contents


#### Scripts

```download.py```

This script downloads data. It is used by specifying the name of the target and a search radius. All data within the specified search radius of the target are downloaded.


```combine.py```

Once data are downloaded, they must be processed and combined into mosaics for photometry. 


```phot.py```

Aperture photometry and total magntiudes are calculated using this script. An input file specifying where the data are located and the aperture size and shape are needed. 

```masking_data.ipynb```

Masks from the z0 Massive Galaxy Synthesis (z0MGS) can be used to mask foreground stars. For many nearby galaxies, they have GALEX NUV 7.5" resolution masks that can be downloaded from [here](https://irsa.ipac.caltech.edu/data/WISE/z0MGS/index.html).

#### Data Files

```correction_factors_??.txt```

Due to sensitivity loss of the UVOT detectors, there is a time dependent sensitivity loss correction that needs to be applied. These files give the correction factors for the UV filters. The optical filters have simpler corrections (as of 2024) that are hardcoded in. 

```names.txt```

This file contains the names of the objects to be downloaded. 

```gal_info.txt```

This file contains the aperture photometry information needed to do the photometry calculation. The columns are name, ra, dec, semimajor, semiminor, and PA. Be careful about whether the code requires the semi-major axis or the major axis (2a). There is not consistency across these packages. 


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

#### Data Files

```correction_factor_??.txt```

Due to sensitivity loss of the UVOT detectors, there is a time dependent sensitivity loss correction that needs to be applied. These files give the correction factors for the UV filters. The optical filters have simpler corrections (as of 2024) that are hardcoded in. 

``` ```



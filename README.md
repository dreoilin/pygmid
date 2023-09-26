![Tests](https://github.com/madrasalach/pygmid/actions/workflows/run-tests.yml/badge.svg?branch=main)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pygmid)
[![DOI](https://zenodo.org/badge/510693980.svg)](https://zenodo.org/badge/latestdoi/510693980)

<p align="center">
  <a>
    <img src="https://github.com/madrasalach/pygmid/blob/main/docs/img/icon.png?raw=true" width="80">
  </a>

  <h3 align="center">pygmid</h3>

  <p align="center">
    A python3 implementation of the gm/ID starter kit
    <br>
    <a href="https://www.github.com/madrasalach/pygmid/issues/new?template=bug.md">Report bug</a>
    ·
    <a href="https://www.github.com/madrasalach/pygmid/issues/new?template=feature.md&labels=feature">Request feature</a>
  </p>
</p>

## Table of contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)

## About

pygmid is a Python 3 version of the gm/ID starter kit by Prof. Boris Murmann 
of Stanford University. The package also offers some scripts from the Paul Jesper's book.

If you find this package useful for your research, please consider citing it.

For the gm/ID starter kit, written for MATLAB, please refer to the 'Links'
section at Prof. Murmann's website: https://web.stanford.edu/~murmann.

## Installation

To install pygmid from source, download from Github and run pip:

`pip install .`

 in the root directory.

 pygmid can also be installed from PyPI:

`pip install pygmid`

## Usage

### Scripting with the Lookup Class
A gm/ID lookup object can be generated with the `Lookup` class. The lookup object requires lookup data for initialisation. Both `.mat` files generated using MATLAB or `.pkl` files generated using pygmid's own characterisation script are supported.

You can create a lookup object as follows:

```python
from pygmid import Lookup as lk

NCH = lk('180nch.mat')
```
### Access MOS Data
The `Lookup` class allows for pseudo array access of the MOS matrix data. You can access data as follows:

```python
# get VGS data as array from NCH
VGS_array = NCH['VGS']
```

Data is returned as a deep copy of the array contained in the `Lookup` object.

### Lookup functionality 

Lookup of interpolated data occurs as follows:

```python
VDSs = NCH['VDS'] 
VGSs = np.arange(0.4, 0.6, 0.05)
# Plot ID versus VDS
ID = NCH.look_up('ID', vds=VDSs, vgs=VGSs)
# alias function lookup can also be used
ID = NCH.lookup('ID', vds=VDSs, vgs=VGSs)
# check bias
VGS = NCH.look_upVGS(GM_ID = 10, VDS = 0.6, VSB = 0.1, L = 0.18)
print(f'VGS is: {VGS}')

plt.plot(VDSs, np.transpose(ID))
```

Modes 1 (Simple parameter lookup), mode 2 (arbitrary ratio lookup) and mode 3 (cross lookup of ratios) are implemented. The companion lookupVGS function is also included.

### Technology Extraction Functions

The EKV extraction function can be used as follows:

```python
from pygmid import EKV_param_extraction, XTRACT

(VDS, n, VT, JS, d1n, d1VT, d1logJS, d2n, d2VT, d2logJS)\
        = EKV_param_extraction(NCH, 1, L = 0.18, VDS = 0.6, VSB = 0.0)

```

Sample usage of this and other utility functions can be found in `debug_utility.py` .

### Examples

Usage of lookup scripts are given in `debug_lookup.py` and `debug_lookupVGS.py`.

Sample outputs for the 180nm generic pdk used in the Murmann starter pack are given below:

![image](https://github.com/madrasalach/pygmid/blob/main/docs/img/IDvVDS.png?raw=true)

![image](https://github.com/madrasalach/pygmid/blob/main/docs/img/vtvsL.png?raw=true)

![image](https://github.com/madrasalach/pygmid/blob/main/docs/img/gm_gds.png?raw=true)

![image](https://github.com/madrasalach/pygmid/blob/main/docs/img/ft.png?raw=true)

![image](https://github.com/madrasalach/pygmid/blob/main/docs/img/idwVDS.png?raw=true)

![image](https://github.com/madrasalach/pygmid/blob/main/docs/img/IDWvsgmID.png?raw=true)

The generic PDK data is hosted <a href="https://github.com/bmurmann/Book-on-gm-ID-design">here</a>.

### Sweeping a Technology

`pygmid` also features a CLI which can be used to run techweeps to generate transistor data.

*Documentation will be added in due course. This functionality is in a state of flux.*

## Authors

- Cian O'Donnell : cian.odonnell@mcci.ie
- Tiarnach Ó Riada : tiarnach.oriada@tyndall.ie
- Danylo Galach

## Contributors

- José Rui Custódio

A special thanks to Prof. Boris Murmann for giving permission to use his work and release this package under the Apache 2.0 License.

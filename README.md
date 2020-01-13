[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub last commit](https://img.shields.io/github/last-commit/hungpham2017/pyWannier90.svg?color=green)
![GitHub issues](https://img.shields.io/github/issues-raw/hungpham2017/pyWannier90.svg?color=crimson)

# pyWannier90: A Python interface for wannier90
[wannier90](http://www.wannier.org/) is a well-established package to construct maximally-localied Wannier functions (MLWFs) and perform MLWF-based analysis.
wannier90 can be used in the library mode via pyWannier90 in conjunction with an ab initio code (e.g., PySCF, VASP) 

<img src="https://github.com/hungpham2017/pyWannier90/blob/master/doc/Si_sp3.png" width="500" align="middle">

## News:
- pyWannier90 is now available for wannier90 community, check it out [here](http://www.wannier.org/download/).
- pyWannier90 only supports wannier90-3.0.0 from now on. 

## Supported ab initio codes:
- PySCF > 1.5 
- VASP via the [MCU package](https://hungpham2017.github.io/mcu/)

## Why pyWannier90?
- If you would like to construct MLWFs from a PySCF calcultion.
- pyWannier90 can construct MLWFs from a WAVECAR containing plane-wave coefficients.
Hence, only one VASP calculation is needed to produce WAVECAR and no special compilation for VASP.
VASP has its own interface (pw2wannier90.x) and must be compiled with this function turned on. 
However, anytime one call wannier90 (for example using different initial guess), a SCF must be run.
This is quite expensive and unneccessary. 

## Future functions:
- Topological analysis using MLWFs 

## How to cite?
Please cite this paper when you use pyWannier90 code in your research:
H. Q. Pham, M. R. Hermes, L. Gagliardi; Periodic Electronic Structure Calculations with the Density Matrix Embedding Theory, [**J. Chem. Theory Comput.**, **2019**](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.9b00939), ASAP.
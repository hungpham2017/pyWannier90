[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub last commit](https://img.shields.io/github/last-commit/hungpham2017/pyWannier90.svg?color=green)
![GitHub issues](https://img.shields.io/github/issues-raw/hungpham2017/pyWannier90.svg?color=crimson)

# pyWannier90: A Python interface for wannier90
[wannier90](http://www.wannier.org/) is a well-established package to construct maximally-localied Wannier functions (MLWFs) as well as to perform MLWF-based analysis.
pyWannier90 uses the library-mode of wannier90 to perform the wannierization on the wave function obtained by PySCF or VASP.

<img src="https://github.com/hungpham2017/pyWannier90/blob/master/doc/Si_sp3.png" width="500" align="middle">

## News:
- pyWannier90 is now available for wannier90 community, check it out [here](http://www.wannier.org/download/).
- pyWannier90 only supports the wannier90 v3.0.0 or newer.

## pyWannier90 can use the wave function obtained by:
- PySCF 1.5 and 
- VASP via the [MCU package](https://hungpham2017.github.io/mcu/)

## Why pyWannier90?
- If you would like to construct MLWFs for the wave function obtained by [PySCF](https://github.com/pyscf/pyscf)
- pyWannier90 for VASP can construct MLWFs using only the WAVECAR and vasprun.xml obtained by VASP.
That means you won't need to rerun the VASP calculation everytime you change some wannierization parameters with the wannier90 build-in library (pw2wannier90.x).
One should note that the MLWFs constructed by pyWannier90 may be not identical to that by VASP since only the pseudo wave function (WAVECAR) is used.
However, I have not experienced any significant discrepancy between the two approaches. 

## How to install libwannier90
libwannier90 needs to be installed first before one can call pyWannier90 from the code of choice (PySCF or MCU).
- Replace /wannier90-xxx/src/wannier_lib.F90 with /pyWannier90/src/wannier_lib.F90
- Go to /wannier90-xxx, modify make.inc with your favorite compiler and important adding this line to it:
	```
	FCOPTS = -O3 -fPIC -g
	```
- Compile wannier90-xxx:
	```
	make & make lib
	```
- Go to /pyWannier90/src, modify Makefile and compile libwannier90:
	```
	make
	```
- Modify the path of libwannier90 in pyWannier90.py (in /pyscf/pbc/tools or in /mcu/wannier90)
	
- Test libwannier90 library:
	```
	python -c "import libwannier90"		#Should return nothing if the compilation was successful
	```
	
## How to cite?
Please cite this paper when you use pyWannier90 code in your research:
- pyWannier90 for PySCF: Q. Sun et al.,Recent developments in the PySCF program package, [**J. Chem. Phys**](https://doi.org/10.1063/5.0006074), **2020**, Just Accepted
- pyWannier90 for VASP: H. Q. Pham, MCU: a Multipurpose Python Library to Analyze the Electronic Wave Function of Solid-State Materials, Manuscript under preparation, [MCU package](https://hungpham2017.github.io/mcu/)
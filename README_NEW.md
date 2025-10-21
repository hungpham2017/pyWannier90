[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub last commit](https://img.shields.io/github/last-commit/hungpham2017/pyWannier90.svg?color=green)
![GitHub issues](https://img.shields.io/github/issues-raw/hungpham2017/pyWannier90.svg?color=crimson)

# pyWannier90: A Python interface for Wannier90

[wannier90](http://www.wannier.org/) is a well-established package to construct maximally-localized Wannier functions (MLWFs) as well as to perform MLWF-based analysis.
pyWannier90 uses the library-mode of wannier90 to perform wannierization on wave functions obtained by PySCF or VASP.

<img src="https://github.com/hungpham2017/pyWannier90/blob/master/doc/Si_sp3.png" width="500" align="middle">

## News

- **v2.0 (NEW)**: Simplified architecture! Removed C++ layer, now uses f2py directly
  - ✅ No more pybind11 dependency
  - ✅ No C++ compiler needed
  - ✅ Simpler installation: `pip install .`
  - ✅ 100% backward compatible API
  - See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for details

- pyWannier90 is now available for the wannier90 community, check it out [here](http://www.wannier.org/download/)
- pyWannier90 only supports wannier90 v3.0.0 or newer

## Supported Wave Function Sources

pyWannier90 can use wave functions obtained by:
- **PySCF** 1.5+ (periodic DFT/HF calculations)
- **VASP** via the [MCU package](https://hungpham2017.github.io/mcu/)

## Why pyWannier90?

- **For PySCF users**: Construct MLWFs directly from PySCF periodic calculations
- **For VASP users**: Construct MLWFs using only WAVECAR and vasprun.xml (no need to rerun VASP when changing wannierization parameters!)
- **Simplified architecture**: Pure Python + Fortran, no C++ complexity
- **Easy installation**: Standard Python packaging (`pip install`)

## Requirements

- Python 3.6+
- NumPy 1.16+ (includes f2py)
- SciPy 1.3+
- PySCF 1.5+
- Wannier90 3.0.0+ (compiled as library)
- LAPACK/BLAS libraries
- Fortran compiler (gfortran or ifort)

**No longer needed:**
- ❌ C++ compiler
- ❌ pybind11

## Installation

### Quick Install (Recommended)

```bash
# 1. Set paths to Wannier90 and LAPACK
export W90DIR=/path/to/wannier90-3.x.x
export LIBDIR=/usr/lib  # or /opt/homebrew/opt/lapack on macOS

# 2. Install with pip
pip install .

# For development mode
pip install -e .
```

### Manual Build

If you prefer to build manually:

```bash
# 1. Prepare Wannier90 library
cd /path/to/wannier90-3.x.x
# Replace src/wannier_lib.F90 with pyWannier90's version
cp /path/to/pyWannier90/src/wannier_lib.F90 src/
# Edit make.inc to add: FCOPTS = -O3 -fPIC -g
make && make lib

# 2. Build pyWannier90
cd /path/to/pyWannier90/src
# Edit Makefile.f2py with correct paths
make -f Makefile.f2py

# 3. Test
python -c "import libwannier90; print('Success!')"
```

### Detailed Installation Steps

#### Step 1: Prepare Wannier90 Library

```bash
cd /path/to/wannier90-3.x.x

# Replace wannier_lib.F90
cp /path/to/pyWannier90/src/wannier_lib.F90 src/

# Edit make.inc and add this line:
# FCOPTS = -O3 -fPIC -g

# Compile
make
make lib  # Creates libwannier.a
```

#### Step 2: Install pyWannier90

**Option A: Using setup.py (easiest)**
```bash
cd /path/to/pyWannier90
export W90DIR=/path/to/wannier90-3.x.x
export LIBDIR=/usr/lib  # adjust for your system
pip install .
```

**Option B: Using Makefile**
```bash
cd /path/to/pyWannier90/src
# Edit Makefile.f2py:
#   W90DIR = /path/to/wannier90-3.x.x
#   LIBDIR = /path/to/lapack
make -f Makefile.f2py
```

#### Step 3: Configure Path in PySCF

Edit `/path/to/pyWannier90/src/pywannier90.py`:
```python
W90LIB = '/path/to/pyWannier90/src'
```

Or use environment variable:
```bash
export PYTHONPATH=/path/to/pyWannier90/src:$PYTHONPATH
```

#### Step 4: Test Installation

```bash
# Test libwannier90 module
python -c "import libwannier90; print('libwannier90 OK')"

# Test full package
python -c "from pyscf.pbc.tools import pywannier90; print('pyWannier90 OK')"

# Run example
cd examples/PySCF
python h2.py
```

## Usage Example

```python
from pyscf.pbc import gto, scf
from pyscf.pbc.tools import pywannier90

# Define unit cell
cell = gto.Cell()
cell.atom = '''
Si 0.00 0.00 0.00
Si 0.25 0.25 0.25
'''
cell.basis = 'gth-dzvp'
cell.pseudo = 'gth-pbe'
cell.a = [[0, 2.7, 2.7], [2.7, 0, 2.7], [2.7, 2.7, 0]]
cell.build()

# Run DFT calculation
kmesh = [2, 2, 2]
kpts = cell.make_kpts(kmesh)
kmf = scf.KRHF(cell, kpts).run()

# Wannierization
num_wann = 8  # 8 sp3 orbitals for 2 Si atoms
w90 = pywannier90.W90(kmf, cell, kmesh, num_wann)
w90.kernel()
w90.plot_wf()  # Generate Wannier function plots
```

## Architecture

### Simplified Design (v2.0+)

```
User Code (Python)
    ↓
pywannier90.py (Python interface)
    ↓
libwannier90 (f2py auto-generated bindings)
    ↓
wannier_lib.F90 (Fortran wrapper)
    ↓
Wannier90 Library (Fortran)
```

**Key improvements:**
- Removed 687 lines of C++ glue code
- Direct Python ↔ Fortran interface via f2py
- Pure NumPy implementation of FFT functions
- Simpler build system

### Old Design (v1.x)

```
User Code (Python)
    ↓
pywannier90.py
    ↓
libwannier90.cpp (C++ + pybind11) ← Removed!
    ↓
wannier_lib.F90
    ↓
Wannier90 Library
```

See [ARCHITECTURE_ANALYSIS.md](ARCHITECTURE_ANALYSIS.md) for detailed comparison.

## Examples

### PySCF Examples

Located in `examples/PySCF/`:
- `h2.py` - H₂ molecule with 2 Wannier functions
- `ch3.py` - CH₃ radical
- `ch4.py` - CH₄ methane with sp³ hybridization

### VASP Examples

Located in `examples/VASP/Si/`:
- `test.py` - Silicon with MCU interface

### Test Suite

Located in `lib-test/`:
- `test-si.py` - Silicon (64 k-points, 12 bands)
- `test-cu.py` - Copper (FCC structure)
- `test-pb.py` - Lead

Run tests:
```bash
cd lib-test
python test-si.py
python test-cu.py
python test-pb.py
```

## Features

- ✅ Spin-restricted (RHF/RKS) calculations
- ✅ Spin-unrestricted (UHF/UKS) with Roothaan effective orbitals
- ✅ Band structure interpolation
- ✅ Hamiltonian construction (k-space and real-space)
- ✅ Wannier function visualization (VESTA format)
- ✅ Initial guess generation (sp, sp², sp³, sp³d, sp³d² orbitals)
- ✅ Checkpoint/restore functionality
- ✅ Gamma-point calculations
- ✅ Spinor support

## Documentation

- [Installation Guide](MIGRATION_GUIDE.md) - Detailed installation and migration guide
- [Architecture Analysis](ARCHITECTURE_ANALYSIS.md) - Design decisions and comparison
- [User Manual](doc/pyWannier90.pdf) - Complete user guide
- [Wannier90 Documentation](http://www.wannier.org/user_guide.html) - Official Wannier90 docs

## Troubleshooting

### "Module libwannier90 not found"
```bash
# Make sure you've built the module
cd src/
make -f Makefile.f2py
# Or install with pip
pip install .
```

### "Cannot find -lwannier"
```bash
# Check Wannier90 library exists
ls /path/to/wannier90/libwannier.a
# If not, compile it:
cd /path/to/wannier90
make lib
```

### "f2py not found"
```bash
# f2py comes with NumPy
pip install numpy
# Test:
python -m numpy.f2py --help
```

## Platform Support

Tested on:
- macOS (M1/M2 and Intel)
- Linux (Ubuntu, CentOS, Fedora)
- Should work on Windows with MinGW/gfortran

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## How to Cite

Please cite these papers when you use pyWannier90:

**For PySCF:**
> Q. Sun et al., Recent developments in the PySCF program package,
> [J. Chem. Phys.](https://doi.org/10.1063/5.0006074) **153**, 024109 (2020)

**For VASP/MCU:**
> H. Q. Pham, MCU: A Multipurpose Python Library to Analyze the Electronic
> Wave Function of Solid-State Materials, Manuscript under preparation,
> [MCU package](https://hungpham2017.github.io/mcu/)

**For Wannier90:**
> A. A. Mostofi et al., An updated version of wannier90: A Tool for Obtaining
> Maximally-Localised Wannier Functions,
> [Comput. Phys. Commun.](http://dx.doi.org/10.1016/j.cpc.2014.05.003)
> **185**, 2309 (2014)

## License

BSD 3-Clause License. See [LICENSE](LICENSE) for details.

## Author

Hung Q. Pham (pqh3.14@gmail.com)

## Acknowledgments

- Wannier90 development team
- PySCF development team
- NumPy f2py developers

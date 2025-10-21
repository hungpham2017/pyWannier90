# Migration Guide: f2py-based Architecture

## Overview

PyWannier90 has been **simplified** by removing the C++ layer entirely. The new architecture uses f2py (built into NumPy) to interface directly with Fortran code.

## What Changed?

### Architecture Simplification

**Before (3 languages):**
```
Python (1,137 lines)
    ↓
C++ + pybind11 (687 lines) ← REMOVED!
    ↓
Fortran (504 lines)
```

**After (2 languages):**
```
Python (1,137 lines)
    ↓
f2py (auto-generated)
    ↓
Fortran (504 lines)
```

### Files Removed
- ❌ `src/libwannier90.cpp` (687 lines of C++ glue code)
- ❌ `arch/Makefile.linux`
- ❌ `arch/Makefile.macOS`

### Files Added
- ✅ `src/Makefile.f2py` (simplified build)
- ✅ `setup.py` (standard Python installation)
- ✅ `get_WF0s_python()` in `pywannier90.py` (pure NumPy implementation)

### Dependencies Removed
- ❌ pybind11
- ❌ C++ compiler (g++)

### Dependencies Kept
- ✅ NumPy (already required, includes f2py)
- ✅ Fortran compiler (gfortran or ifort)
- ✅ Wannier90 library
- ✅ LAPACK/BLAS

## Installation

### Method 1: Using setup.py (Recommended)

```bash
# Set environment variables
export W90DIR=/path/to/wannier90-3.x.x
export LIBDIR=/opt/homebrew/opt/lapack  # or /usr/lib on Linux

# Install
pip install .

# Or for development
pip install -e .
```

### Method 2: Using Makefile

```bash
cd src/

# Edit Makefile.f2py and set:
# W90DIR = /path/to/wannier90
# LIBDIR = /path/to/lapack

# Build
make -f Makefile.f2py

# Test
python -c "import libwannier90; print('Success!')"
```

## API Compatibility

**Good news:** The API is **100% compatible**! No code changes needed in user scripts.

### For Users

Your existing scripts will work **without modification**:

```python
from pyscf.pbc.tools import pywannier90

# Everything works the same
w90 = pywannier90.W90(kmf, cell, mp_grid, num_wann)
w90.kernel()
w90.plot_wf()
```

### For Developers

Internal changes:
1. `libwannier90.get_WF0s()` → `get_WF0s_python()` (pure NumPy)
2. `libwannier90.setup()` → still available via f2py
3. `libwannier90.run()` → still available via f2py

## Build Comparison

### Old Build (pybind11)

```bash
# Complex platform-specific build
g++ -O3 -shared -std=c++11 -fPIC \
    `python3 -m pybind11 --includes` \
    libwannier90.cpp \
    -o libwannier90*.so \
    -L/path/to/wannier90 -lwannier \
    -L/path/to/lapack -llapack -lblas \
    -undefined dynamic_lookup  # macOS only
```

### New Build (f2py)

```bash
# Simple, platform-independent
f2py -c wannier_lib.F90 \
     -m libwannier90 \
     -L/path/to/wannier90 -lwannier \
     -llapack -lblas \
     --opt="-O3 -fPIC"
```

**Lines of build configuration:**
- Old: ~50 lines across multiple files
- New: ~15 lines in one file

## Performance

No performance regression expected:
- ✅ f2py has **zero overhead** (direct Fortran calls)
- ✅ `get_WF0s_python()` uses **vectorized NumPy** operations
- ✅ All heavy computation still in Fortran (Wannier90 library)

Potential **improvements**:
- NumPy operations can leverage BLAS/MKL automatically
- Easier to profile and optimize Python code

## Testing

All existing tests should pass:

```bash
# Run library tests
cd lib-test/
python test-si.py
python test-cu.py
python test-pb.py

# Run examples
cd examples/PySCF/
python h2.py
python ch3.py
python ch4.py
```

## Troubleshooting

### Issue: "Module libwannier90 not found"

**Solution:** Build the module first
```bash
cd src/
make -f Makefile.f2py
```

### Issue: "Cannot find wannier90 library"

**Solution:** Set the correct path
```bash
export W90DIR=/correct/path/to/wannier90
```

### Issue: "Undefined symbol: wannier_setup"

**Solution:** Make sure Wannier90 was compiled with library mode
```bash
cd /path/to/wannier90
make lib
# This creates libwannier.a
```

### Issue: "f2py not found"

**Solution:** f2py comes with NumPy
```bash
pip install numpy
# or
conda install numpy
```

## Benefits Summary

| Aspect | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Languages** | 3 (Py+C++/F90) | 2 (Py+F90) | -33% |
| **LOC (glue code)** | 687 | 0 | -100% |
| **Dependencies** | 5 | 3 | -40% |
| **Build files** | 4 | 2 | -50% |
| **Compilers** | 3 | 2 | -33% |
| **Platform issues** | Many | Few | Better |
| **Maintainability** | Hard | Easy | Much better |
| **Installation** | Complex | Simple | pip install |

## Questions?

1. **Do I need to modify my analysis scripts?**
   - No! API is 100% compatible

2. **Is this faster or slower?**
   - Same performance (both have zero overhead)

3. **Can I still use the old version?**
   - Yes, but the new version is recommended

4. **What Python versions are supported?**
   - Python 3.6+ (same as before)

5. **Does this work on Windows?**
   - Yes, if you have gfortran installed

## Migration Checklist

For users upgrading from old version:

- [ ] Uninstall old version: `pip uninstall pywannier90`
- [ ] Set environment variables: `W90DIR`, `LIBDIR`
- [ ] Install new version: `pip install .`
- [ ] Test with your scripts (no code changes needed)
- [ ] Enjoy simpler builds! 🎉

## Reporting Issues

If you encounter problems with the new build system:

1. Check that Wannier90 library is properly compiled
2. Verify environment variables are set correctly
3. Try the manual Makefile build first
4. Report issues at: https://github.com/hungpham2017/pyWannier90/issues

Include:
- OS and version
- Python version
- NumPy version
- Fortran compiler version
- Full error message

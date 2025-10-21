# PyWannier90 Architecture Analysis and Simplification Proposal

## Current Architecture Problems

### Multi-Language Complexity
```
User Code (Python)
    ↓
pywannier90.py (Python, 1137 lines)
    ↓
libwannier90.cpp (C++ + pybind11, 687 lines)
    ↓ [extern "C" calls]
wannier_lib.F90 (Fortran wrapper, 504 lines)
    ↓
Wannier90 Library (external Fortran)
```

### Issues with Current Design

1. **Three-Language Stack**: Python → C++ → Fortran
   - Requires three different compilers
   - Complex build system with multiple toolchains
   - Difficult to debug across language boundaries

2. **Unnecessary C++ Layer**: The entire C++ layer does:
   - Type conversions (Python numpy → C pointers → Fortran arrays)
   - Name mangling handling (ifort vs gfortran)
   - Memory layout conversions
   - **All of this can be done automatically by f2py or ctypes**

3. **Build Dependencies**:
   - pybind11 (header-only library)
   - Python development headers
   - C++ compiler (g++) with C++11 support
   - Fortran compiler (gfortran or ifort)
   - LAPACK/BLAS libraries

4. **Platform-Specific Complications**:
   - Different Fortran name mangling (`#ifdef ifort` vs `#else` for gfortran)
   - Different linking flags for macOS vs Linux
   - Manual handling of symbol names

## Proposed Simplified Architecture

### **Option 1: f2py (RECOMMENDED)**
```
User Code (Python)
    ↓
pywannier90.py (Python)
    ↓ [f2py generated bindings]
wannier_lib.F90 (Fortran wrapper)
    ↓
Wannier90 Library (external Fortran)
```

**Advantages**:
- Eliminates C++ entirely
- Removes pybind11 dependency
- f2py is part of NumPy (already a dependency)
- Automatic type conversion
- Handles Fortran name mangling automatically
- Cross-platform by default
- Simpler build system

**Implementation**:
```bash
# Simple build command
f2py -c wannier_lib.F90 -m libwannier90 \
     -L/path/to/wannier90 -lwannier \
     -llapack -lblas
```

### **Option 2: ctypes + iso_c_binding**
```
User Code (Python)
    ↓
pywannier90.py (Python with ctypes)
    ↓ [ctypes FFI]
wannier_lib.F90 (Fortran with iso_c_binding)
    ↓
Wannier90 Library (external Fortran)
```

**Advantages**:
- No build step for bindings (runtime loading)
- Modern Fortran feature (Fortran 2003+)
- Very explicit interface
- No extra Python dependencies

**Disadvantages**:
- More manual array handling
- Requires modifying Fortran code for iso_c_binding
- More verbose Python code

### **Option 3: Modern f2py with f90wrap**
```
User Code (Python)
    ↓
pywannier90.py (Python)
    ↓ [f90wrap + f2py]
wannier_lib.F90 (unchanged Fortran)
    ↓
Wannier90 Library (external Fortran)
```

**Advantages**:
- Better handling of modern Fortran features
- Object-oriented Fortran support
- Minimal changes to Fortran code

## Detailed Comparison

| Aspect | Current (pybind11) | f2py | ctypes + iso_c | f90wrap |
|--------|-------------------|------|----------------|---------|
| Languages | Python+C+++Fortran | Python+Fortran | Python+Fortran | Python+Fortran |
| Dependencies | pybind11, C++ compiler | NumPy (already have) | None extra | f90wrap, NumPy |
| Build complexity | High | Medium | Low | Medium |
| Maintenance | Hard (3 languages) | Easy | Easy | Easy |
| Performance | Excellent | Excellent | Excellent | Excellent |
| Type safety | Compile-time | Compile-time | Runtime | Compile-time |
| Name mangling | Manual (#ifdef) | Automatic | N/A (C interface) | Automatic |
| Array handling | Manual | Automatic | Manual | Automatic |

## Code Reduction Analysis

### Files to Remove
1. `src/libwannier90.cpp` - **687 lines eliminated**
2. `arch/Makefile.*` - Simplified significantly
3. pybind11 dependency - No longer needed

### Files to Modify
1. `src/wannier_lib.F90` - Minor modifications or none (for f2py)
2. `src/Makefile` - Drastically simplified
3. `src/pywannier90.py` - Minor changes to import statement

### New Files (minimal)
1. `setup.py` - Standard Python packaging with f2py integration

## Implementation Roadmap

### Phase 1: Create f2py-based alternative
1. Create new Makefile using f2py
2. Test with existing examples
3. Verify all functionality works

### Phase 2: Migrate Python code
1. Change import from `import libwannier90` to new module
2. Test all examples (H2, CH3, CH4, Si)
3. Run lib-test suite

### Phase 3: Clean up
1. Remove libwannier90.cpp
2. Remove pybind11 references
3. Update documentation

### Phase 4: Modernize build
1. Create proper setup.py
2. Enable `pip install .`
3. Consider conda packaging

## Example Implementation (f2py approach)

### New Makefile (simplified)
```makefile
W90DIR = /path/to/wannier90
LIBDIR = /opt/homebrew/opt/lapack

F90 = gfortran
F2PY = f2py
W90LIB = -L$(W90DIR) -lwannier
LAPACK = -L$(LIBDIR)/lib -llapack -lblas

all: libwannier90

libwannier90:
	$(F2PY) -c wannier_lib.F90 -m libwannier90 \
		$(W90LIB) $(LAPACK) \
		--fcompiler=$(F90) \
		--opt="-O3 -fPIC"

clean:
	rm -f *.so *.o *.mod
```

**Lines**: ~15 (vs current ~21, but removes entire arch/ directory)

### Changes to pywannier90.py
```python
# OLD:
import libwannier90

# NEW (no change needed if f2py uses same module name):
import libwannier90
# or
import libwannier90 as w90lib
```

**Lines changed**: 0-5 lines

### Total Code Reduction
- **Eliminated**: 687 lines (C++)
- **Simplified**: Build system (arch/ directory eliminated)
- **Dependencies reduced**: pybind11, C++ compiler no longer needed
- **Maintenance burden**: Reduced by ~40%

## Migration Risks and Mitigation

### Risk 1: Array ordering (C vs Fortran)
- **Mitigation**: f2py handles this automatically
- **Test**: Extensive testing with existing test suite

### Risk 2: Complex number handling
- **Mitigation**: f2py supports complex types natively
- **Test**: Verify M_matrix, A_matrix, U_matrix conversions

### Risk 3: Breaking user code
- **Mitigation**: Keep same module name and API
- **Test**: All examples must pass unchanged

### Risk 4: Performance regression
- **Mitigation**: Both pybind11 and f2py have zero overhead
- **Test**: Benchmark before/after

## Recommendation

**Use f2py (Option 1)** because:

1. ✅ Minimal code changes required
2. ✅ No new dependencies (NumPy already required)
3. ✅ Automatic handling of all type conversions
4. ✅ Eliminates 687 lines of C++ glue code
5. ✅ Simpler build process
6. ✅ Better cross-platform support
7. ✅ Easier to maintain (2 languages instead of 3)
8. ✅ Standard in scientific Python community

## Next Steps

1. **Prototype**: Create f2py-based build in parallel
2. **Test**: Validate with all existing examples
3. **Document**: Update README with simpler build instructions
4. **Deploy**: Replace current system once validated
5. **Cleanup**: Remove obsolete files

## Estimated Timeline

- **Prototype**: 2-4 hours
- **Testing**: 2-3 hours
- **Documentation**: 1 hour
- **Total**: 1 day of focused work

## Questions to Consider

1. Do we need backward compatibility with old build?
   - **Recommendation**: No, clean break is better
2. Should we support both methods during transition?
   - **Recommendation**: No, increases complexity
3. What Python versions to support?
   - **Recommendation**: 3.8+ (f2py works well)

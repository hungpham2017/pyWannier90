# pyWannier90: A Wannier90 python interface for PySCF 


<img src="https://github.com/hungpham2017/pyWannier90/blob/master/doc/Si_sp3.png" width="500" align="middle">


### How to compile pyWannier90
 - Required: g++, gfortran, cmake, pybind11, openmp (Optional)
 - First compile the wannier90 (http://www.wannier.org/): note that the flag "-fPIC" is needed in make.inc.
   Only wannier90-2.1.0 has been tested.
 - Modify the Wannier90 directory in the install.sh
 - For the OpenMP version, simply replace "libwannier90.cpp" by "libwannier90_omp.cpp" in the CMakeLists.txt file
 - Compile the libwannier90 library: 
    source install.sh
 - Modify the libwannier90 directory in the pywannier90.py
 - In general, the libwannier90 library can be incorporated in any python-based electronic structure codes. However, it is highly recommended to use it with PySCF via pywannier90.py module
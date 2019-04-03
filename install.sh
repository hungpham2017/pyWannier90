# Compile Wannier90 library with the new plot.f90 (bug fixed) then pyWannier90


# How to compile pyWannier90:
# - Required: g++, gfortran, cmake, pybind11, openmp (Optional)
# - First compile the wannier90 (http://www.wannier.org/): note that the flag "-fPIC" is needed in make.inc.
#   Only wannier90-2.1.0 has been tested.
# - Modify the Wannier90 directory in the install.sh
# - For the OpenMP version, simply replace "libwannier90.cpp" by "libwannier90_omp.cpp" in the CMakeLists.txt file
# - Compile the libwannier90 library: 
#    source install.sh
# - Modify the libwannier90 directory in the pywannier90.py
# - In general, the libwannier90 library can be incorporated in any python-based electronic structure codes. However, it is highly recommended to use it with PySCF via pywannier90.py interface

# User changes this path to the wannier90 source
W90="/panfs/roc/groups/6/gagliard/phamx494/wannier90-2.1.0"

#copy the obj from the compiled wannier90
if [ ! -d "./obj" ]; then 
mkdir ./obj
fi
cp -rf $W90/src/obj/* ./obj/

#copy the modified version of wannier_lib.F90
cp ./wannier_lib.F90 ./obj/wannier_lib.F90


# Compile Code
gfortran -fPIC -O3 -c ./obj/wannier_lib.F90

cmake ./
make




	

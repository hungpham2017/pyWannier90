#########################################
# pyWannier90                           #                                
# User defines the compiling parameters #
#----------------START------------------#
W90DIR =/panfs/roc/groups/6/gagliard/phamx494/wannier90-3.0.0
#LIBDIR =/panfs/roc/groups/6/gagliard/phamx494/intel
LIBDIR =/panfs/roc/intel/x86_64/2018/parallel_studio_xe_msi/compilers_and_libraries_2018.0.128/linux
USE_INTEL = yes
#-----------------END-------------------#

ifeq ($(USE_INTEL), yes)
	CPP = icpc
	LIBS = -L$(LIBDIR)/mkl/lib/intel64 -lmkl_core -lmkl_intel_lp64 -lmkl_sequential \
	-Wl,-rpath,$(LIBDIR)/lib/intel64 -L$(LIBDIR)/lib/intel64 -limf -lintlc -liomp5 -lifcore \
	-Wl,-rpath,$(W90DIR) -L$(W90DIR) -lwannier
    all: libwannier90_intel
else
	CPP = g++
	LIBS = -L$(LIBDIR)/lib -llapack -lblas -Wl,-rpath,$(W90DIR) -L$(W90DIR) -lwannier
    all: libwannier90_gf
endif

CPPFLAGS = -O3 -Wall -shared -std=c++11 -fPIC -D_UF 

libwannier90_intel:
	sed -i '/#define*/c\#define ifort' libwannier90.cpp
	$(CPP) $(CPPFLAGS) `python3 -m pybind11 --includes` libwannier90.cpp -o libwannier90`python3-config --extension-suffix` $(LIBS)

libwannier90_gf:
	sed -i '/#define*/c\#define gfortran' libwannier90.cpp
	$(CPP) $(CPPFLAGS) `python3 -m pybind11 --includes` libwannier90.cpp -o libwannier90`python3-config --extension-suffix` $(LIBS)

     
clean:
	rm -rf obj
	rm -f *.so *.o *.mod
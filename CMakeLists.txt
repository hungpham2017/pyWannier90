cmake_minimum_required(VERSION 3.1 FATAL_ERROR)
project(libwannier90)

set(anaconda "/nfs/roc/groups/6/gagliard/phamx494/anaconda")

# Set INCLUDE and LIB 
LINK_DIRECTORIES(${anaconda}/lib)
INCLUDE_DIRECTORIES(${anaconda}/include)

# Find the LAWrap for mkl_blas/lapack, pybind11
find_package(LAWrap CONFIG REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
message(STATUS "Found LAWrap: ${LAWrap_CONFIG}")
message(STATUS "Found pybind11: ${pybind11_CONFIG}")

# Set python
set(PYTHON_EXECUTABLE)

# Openmp
include(FindOpenMP)
if(OPENMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

# Set pybind11 c++ standard
set(PYBIND11_CPP_STANDARD -std=c++11)

# Creates a python module named "module_name"
pybind11_add_module(libwannier90 MODULE libwannier90.cpp)
target_link_libraries(libwannier90 ${CMAKE_CURRENT_SOURCE_DIR}/obj/constants.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/disentangle.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/hamiltonian.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/io.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/kmesh.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/overlap.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/parameters.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/plot.o	
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/sitesym.o                        
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/transport.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/utility.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/wannierise.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/ws_distance.o					
						${CMAKE_CURRENT_SOURCE_DIR}/wannier_lib.o gfortran lapack blas)
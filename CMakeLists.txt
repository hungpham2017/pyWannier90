cmake_minimum_required(VERSION 3.1 FATAL_ERROR)
project(libwannier90)

set(anaconda "/panfs/roc/groups/6/gagliard/phamx494/anaconda")

# Set INCLUDE and LIB 
LINK_DIRECTORIES(${anaconda}/lib)
INCLUDE_DIRECTORIES(${anaconda}/include)

# Find the LAWrap for mkl_blas/lapack, pybind11
find_package(LAWrap CONFIG REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
message(STATUS "Found LAWrap: ${LAWrap_CONFIG}")
message(STATUS "Found pybind11: ${pybind11_CONFIG}")

# Creates a python module named "module_name"
pybind11_add_module(libwannier90 MODULE libwannier90.cpp)
target_link_libraries(libwannier90 ${CMAKE_CURRENT_SOURCE_DIR}/obj/constants.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/io.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/utility.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/parameters.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/hamiltonian.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/kmesh.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/overlap.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/disentangle.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/wannierise.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/plot.o			
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/transport.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/sitesym.o
 						${CMAKE_CURRENT_SOURCE_DIR}/obj/ws_distance.o					
						${CMAKE_CURRENT_SOURCE_DIR}/wannier_lib.o gfortran lapack blas)
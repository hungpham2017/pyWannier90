# Compile Wannier90 library with the new plot.f90 (bug fixed) then pyWannier90

# Change to the wannier90 source
W90="/panfs/roc/groups/6/gagliard/phamx494/wannier90-2.1.0"

#copy the obj from the compiled wannier90
if [ ! -d "./obj" ]; then 
mkdir ./obj
fi
cp -rf $W90/src/obj/* ./obj/

#copy the modified version of wannier_lib.F90
cp ./plot.F90 ./obj/plot.F90
cp ./wannier_lib.F90 ./obj/wannier_lib.F90


# Compile Code
gfortran -fPIC -O3 -c ./obj/plot.F90
mv ./w90_plot.mod ./obj/w90_plot.mod
mv ./plot.o ./obj/plot.o
gfortran -fPIC -O3 -c ./obj/wannier_lib.F90

cmake ./
make




	

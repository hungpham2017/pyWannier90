## How to install pyWannier90
(1) Replace /wannier90-xxx/src/wannier_lib.F90 with /pyWannier90/src/wannier_lib.F90
(2) Go to /wannier90-xxx, modify make.inc and compile wannier90-xxx:
	-- make & make lib
(3) Go to /pyWannier90/src, modify Makefile and compile libwannier90:
	make
(4) Modify the path of libwannier90 in pyWannier90.py
	
## Test libwannier90 library:
	python -c 'import libwannier90'		#Should return nothing if the compilation was successful


	

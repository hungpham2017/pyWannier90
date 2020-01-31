## How to install pyWannier90
- Replace /wannier90-xxx/src/wannier_lib.F90 with /pyWannier90/src/wannier_lib.F90
- Go to /wannier90-xxx, modify make.inc with your favorite compiler and important adding this like:
	FCOPTS = -O3 -fPIC -g
- Compile wannier90-xxx:
	"make & make lib"
- Go to /pyWannier90/src, modify Makefile and compile libwannier90:
	"make"
- Modify the path of libwannier90 in pyWannier90.py
	
## Test libwannier90 library:
	'python -c "import libwannier90"'		#Should return nothing if the compilation was successful


	

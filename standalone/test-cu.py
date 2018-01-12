'''
Testing C++ wrapper for Wannier90
Hung Q. Pham
mail: pqh3.14@gmail.com
'''

import numpy as np
import libwannier90
import cmath, os



name = "copper"
# copy the target win file and remove the current wannier90.wout file
os.system("cp copper.win wannier90.win")
os.system("if [ ! -f ./wannier90.wout ];then rm wannier90.wout; fi")  

#example04: Copper
num_bands_tot = 12
num_kpts_loc = 64
mp_grid_loc = [4, 4, 4]
real_lattice_loc = np.asarray([[-1.8050235, 0.0000, -1.8050235],[0.0000, 1.8050235, 1.8050235],[1.8050235, 1.8050235, 0.0000]], dtype = float) #in C order
recip_lattice_loc = 2*np.pi*np.linalg.inv(real_lattice_loc.T)

kpt_latt_loc = np.empty([64,3],dtype = float)
#Create the k-point list
x = np.linspace(0, 0.75, 4)
grid = np.meshgrid(x,x,x, sparse = False)
kpt_latt_loc[:,0] = grid[0].reshape(64)
kpt_latt_loc[:,1] = grid[2].reshape(64) 
kpt_latt_loc[:,2] = grid[1].reshape(64) 

num_atoms_loc = 1
atom_symbols_loc = ['Cu']
atom_atomic_loc = ['29']
atoms_frac_loc = np.asarray([0.0, 0.0, 0.0]) #in C order
atoms_cart_loc = atoms_frac_loc.T.dot(real_lattice_loc)
gamma_only_loc = False
spinors_loc = False

if gamma_only_loc == True: 
	gamma_only_boolean = 1
else:
	gamma_only_boolean = 0
	
if gamma_only_loc == True: 
	spinors_boolean = 1
else:
	spinors_boolean = 0
					
#RUN WANNIER90
seed__name = "wannier90"
real_lattice_loc = real_lattice_loc.flatten()
recip_lattice_loc = recip_lattice_loc.flatten()
kpt_latt_loc = kpt_latt_loc.flatten()
atoms_cart_loc = atoms_cart_loc.flatten()

bands_wann_nntot, nn_list, proj_site, proj_l, proj_m, proj_radial, proj_z, proj_x, proj_zona, exclude_bands, proj_s, proj_s_qaxis = \
libwannier90.setup(seed__name, mp_grid_loc, num_kpts_loc, real_lattice_loc, \
					recip_lattice_loc, kpt_latt_loc, num_bands_tot, num_atoms_loc, \
					atom_atomic_loc, atoms_cart_loc, gamma_only_boolean, spinors_boolean)		


# Convert outputs to the correct data type
num_bands_loc, num_wann_loc, nntot_loc = np.int32(bands_wann_nntot)
nn_list = np.int32(nn_list)
proj_l = np.int32(proj_l)
proj_m = np.int32(proj_m)
proj_radial = np.int32(proj_radial)
exclude_bands = np.int32(exclude_bands)
proj_s = np.int32(proj_s)
					
# Reading A_matrix
A_matrix_loc = np.empty([num_kpts_loc, num_wann_loc, num_bands_loc], dtype = complex)
file = open(name + ".amn")
file.readline()
file.readline() 
num_data = num_bands_loc * num_wann_loc * num_kpts_loc

lines = []	
for point in range(num_data):	
	lines.append(file.readline().split())

for i in range(num_kpts_loc):
	for j in range(num_wann_loc):
		for k in range(num_bands_loc):
			x = float(lines[i*num_wann_loc*num_bands_loc + j*num_bands_loc + k][3])
			y = float(lines[i*num_wann_loc*num_bands_loc + j*num_bands_loc + k][4])			
			A_matrix_loc[i,j,k] = complex(x,y)		
	
# Reading M_matrix (as M1 and M2)	
num_mmn = nntot_loc * num_kpts_loc
M_kpt2 = np.empty([num_mmn, 5], dtype = int)
M_matrix_loc = np.empty([num_kpts_loc, nntot_loc, num_bands_loc, num_bands_loc], dtype = complex)
file = open(name + ".mmn")
file.readline()
file.readline() 

lines = []	
for nkp in range(num_mmn):
	line = np.asarray(file.readline().split(), dtype = int)
	M_kpt2[nkp, :] = line
	for k in range(num_bands_loc):
		for l in range(num_bands_loc):
			lines.append(file.readline().split())		

M1 = num_bands_loc
M2 = M1 * num_bands_loc
M3 = M2 * nntot_loc 			
for nkp in range(num_kpts_loc):
	for nn in range(nntot_loc): 
		nn_index = 0
		for nn2 in range(nntot_loc):
			if (M_kpt2[nkp*nntot_loc + nn, 1] == nn_list[nn2, nkp, 0]):
				nn_index = nn2;
				break;
				
		for n in range(num_bands_loc):
			for m in range(num_bands_loc):
				x = float(lines[nkp*M3 + nn*M2 + n*M1 + m ][0])
				y = float(lines[nkp*M3 + nn*M2 + n*M1 + m ][1])
				M_matrix_loc[nkp, nn_index, n, m] = complex(x,y)	
				
# Reading eigenvals_matrix	
eigenvalues_loc	= np.empty([num_kpts_loc, num_bands_loc], dtype = float)	
file = open(name + ".eig")

for i in range(num_kpts_loc):
	for j in range(num_bands_loc):
		line = file.readline().split()	
		eigenvalues_loc[i, j] = float(line[2])
		
A_matrix_loc = A_matrix_loc.flatten()
M_matrix_loc = M_matrix_loc.flatten()
eigenvalues_loc = eigenvalues_loc.flatten()
		
U_matrix, U_matrix_opt, lwindow, wann_centres, wann_spreads, spread = \
libwannier90.run(seed__name, mp_grid_loc, num_kpts_loc, real_lattice_loc, \
					recip_lattice_loc, kpt_latt_loc.flatten(order='F'), num_bands_tot, num_bands_loc, num_wann_loc, nntot_loc, num_atoms_loc, \
					atom_atomic_loc, atoms_cart_loc, gamma_only_boolean, \
					M_matrix_loc, A_matrix_loc, eigenvalues_loc)
					
# Convert outputs to the correct data type
lwindow = np.int32(lwindow.real)
lwindow = (lwindow == 1)
wann_centres = wann_centres.real
wann_spreads = wann_spreads.real
spread = spread.real
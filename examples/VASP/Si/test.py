import sys
from mcu.vasp import pywannier90_vasp as pyw90
import subprocess 

nk = [3, 3, 3] 
num_wann = 4
keywords = \
'''
exclude_bands : 5-8
Begin Projections     
c=0.,0.,0. : sp3 
End Projections   
num_iter : 3
'''

w90 = pyw90.W90(nk, num_wann, other_keywords = keywords)
# w90.make_win()
# w90.setup()
# A0 = w90.read_A_mat()
# A1 = w90.get_A_mat()
# for i in range(27):
    # print((A0[i].real/A0[i].imag).sum(), (A1[i].real/A1[i].imag).sum())
subprocess.call('rm wannier90.wout', shell=True)
w90.kernel()
subprocess.call('grep "================       Omega D      =" wannier90.wout', shell=True)
subprocess.call('sed -i -e "s/num_bands       = 8/num_bands       = 4/g" wannier90.win', shell=True)

# '''Test the unk export here and from VASP'''
# import mcu
# import numpy as np
# from mcu.vasp import pywannier90_vasp as pyw90
# wave = mcu.WAVECAR()
# ngrid = [16,16,16]
# kpt = 5
# coords, weights = pyw90.periodic_grid(wave.cell[0], ngrid, supercell = [1,1,1], order = 'F')
# exp_ikr = np.exp(1j*coords.dot(wave.kpts[kpt].dot(wave.cell[1]))).reshape(ngrid, order = 'F') 
# u0 = wave.get_unk(kpt=kpt+1, band=2, ngrid=ngrid)
# psi0 = np.einsum('xyz,xyz->xyz', exp_ikr, u0, optimize = True)
# wave.write_vesta(u0,filename='unk')
# wave.write_vesta(psi0,filename='psi')



# for kpt in range(27):
    # for band in range(4):
        # u0 = wave.get_unk(kpt=kpt+1, band=band+1, ngrid=ngrid)
        # u1 = mcu.read_unk(path='./unk', kpt=kpt+1, band=band+1)
        # print("Error:", abs(u0-u1).max())
        
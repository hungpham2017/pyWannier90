'''
Testing C++ wrapper for Wannier90
Hung Q. Pham
email: pqh3.14@gmail.com
'''

'''
a CH4 in a box
Construct four sp3-like WFs from 9 Bloch states
'''

import numpy as np
from pyscf import scf, gto
from pyscf.pbc import gto, dft, df
import pywannier90

cell = gto.Cell()
cell.atom = '''
C 0.725 2.000 2.000
C 1.925 2.000 2.000
'''
cell.basis = '6-31g'
cell.a = np.asarray([[2.65,0.0,0.0],[0.0,4.0,0.0],[0.0,0.0,4.0]])
cell.ke_cutoff = 100
#cell.gs = [12 18 18]
cell.verbose = 5
cell.build()

nk = [5,1,1]
abs_kpts = cell.make_kpts(nk)
kmf = dft.KRKS(cell, abs_kpts).mix_density_fit()
kmf.xc = 'pbe'
ekpt = kmf.run()


num_wann = 2
keywords = \
'''
exclude_bands : 1,2,3,4,7,8,9,10,11,12,13,14,15,16,17,18
'''

w90 = pywannier90.W90(kmf, nk, num_wann, gamma = False, other_keywords = keywords)
w90.use_bloch_phases = True
w90.kernel()
w90.plot_wf(wf_list=[0,1], supercell = [1,1,1], grid = [50,50,50])
w90.export_unk(grid = [50,50,50])

keywords = \
'''
exclude_bands : 1,2,3,4,7,8,9,10,11,12,13,14,15,16,17,18
wannier_plot = True
wannier_plot_supercell = 1
'''

w90 = pywannier90.W90(kmf, nk, num_wann, gamma = False, other_keywords = keywords)
w90.use_bloch_phases = True
w90.kernel()

'''
Testing C++ wrapper for Wannier90
Hung Q. Pham
email: pqh3.14@gmail.com
'''

'''
a CH3 radical in a box
Construct four sp3-like WFs from 9 Bloch states
'''

import numpy as np
from pyscf import scf, gto
from pyscf.pbc import gto, dft, df
import pywannier90

cell = gto.Cell()
cell.atom = '''
 C                  3.17500000    3.17500000    3.17500000
 H                  2.54626556    2.54626556    2.54626556
 H                  3.80373444    3.80373444    2.54626556
 H                  2.54626556    3.80373444    3.80373444
'''
cell.basis = 'sto-3g'
cell.a = np.eye(3) * 6.35
cell.gs = [15] * 3
cell.spin = 1
cell.verbose = 5
cell.build()


nk = [1, 1, 1]
abs_kpts = cell.make_kpts(nk)
kmf = dft.KUKS(cell, abs_kpts).mix_density_fit()
kmf.xc = 'pbe'
ekpt = kmf.run()
	
num_wann = 4
keywords = \
'''
begin projections
C:sp3
end projections
'''

w90 = pywannier90.W90(kmf, nk, num_wann, gamma = True, spin_up = False, other_keywords = keywords)
w90.kernel()
w90.plot_wf(wf_list=[0,1,2,3], supercell = [1,1,1])
w90.export_unk()


keywords = \
'''
begin projections
C:sp3
end projections
wannier_plot = True
wannier_plot_supercell = 1
'''

w90 = pywannier90.W90(kmf, nk, num_wann, gamma = True, spin_up = False, other_keywords = keywords)
w90.kernel()
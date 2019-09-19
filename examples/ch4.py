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
from pyscf.pbc import gto, dft, df
from pyscf.pbc.tools import pywannier90

cell = gto.Cell()
cell.atom = '''
 C                  3.17500000    3.17500000    3.17500000
 H                  2.54626556    2.54626556    2.54626556
 H                  3.80373444    3.80373444    2.54626556
 H                  2.54626556    3.80373444    3.80373444
 H                  3.80373444    2.54626556    3.80373444
'''
cell.basis = 'sto-3g'
cell.a = np.eye(3) * 6.35
cell.gs = [15] * 3
cell.verbose = 5
cell.build()


nk = [1, 1, 1]
abs_kpts = cell.make_kpts(nk)
kmf = dft.KRKS(cell, abs_kpts).mix_density_fit()
kmf.xc = 'pbe'
ekpt = kmf.run()
	
num_wann = 4
keywords = \
'''
exclude_bands : 1,6-9
begin projections
C:sp3
end projections
'''

w90 = pywannier90.W90(kmf, cell, nk, num_wann, other_keywords = keywords)
w90.kernel()
w90.plot_wf(grid=[25,25,25], supercell=nk)
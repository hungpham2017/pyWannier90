'''
Testing C++ wrapper for Wannier90
Hung Q. Pham
email: pqh3.14@gmail.com
'''

'''
a H2 in a box
Construct one sigma-like WF from 2 Bloch states
'''

import numpy as np
from pyscf.pbc import gto, dft, df
from pyscf.pbc.tools import pywannier90


cell = gto.Cell()
cell.atom = '''
H 1.5 1.5 1
H 1.5 1.5 2
'''
cell.basis = '6-31g'
cell.a = np.eye(3) * 3
cell.gs = [10] * 3
cell.verbose = 5
cell.build()

nk = [2, 2, 2]
abs_kpts = cell.make_kpts(nk)
kmf = dft.KRKS(cell, abs_kpts)
kmf.xc = 'pbe'
ekpt = kmf.run()

num_wann = 2
keywords = \
'''
exclude_bands : 3,4
begin projections
H:s
end projections
wannier_plot = True
wannier_plot_supercell = 3 3 3
'''

w90 = pywannier90.W90(kmf, cell, nk, num_wann, other_keywords = keywords)
w90.make_win()
w90.setup()
w90.export_unk(grid = [25,25,25])
w90.kernel() 
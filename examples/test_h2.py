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
from pyscf import scf, gto
from pyscf.pbc import gto, dft, df
import pywannier90


cell = gto.Cell()
cell.atom = '''
H 1.5 1.5 1
H 1.5 1.5 2
'''
cell.basis = 'cc-pCVDZ'
cell.a = np.eye(3) * 3
cell.gs = [10] * 3
cell.verbose = 5
cell.build()

nk = [2, 2, 2]
abs_kpts = cell.make_kpts(nk)
kmf = dft.KRKS(cell, abs_kpts)
kmf.xc = 'pbe'
ekpt = kmf.run()

num_wann = 1
w90 = pywannier90.W90(kmf, nk, num_wann, gamma = False)
w90.use_bloch_phases = True
w90.kernel()
w90.plot_wf(supercell = [1,1,1])
w90.export_unk(grid = [50,50,50])

keywords = \
'''
wannier_plot = True
wannier_plot_supercell = 1
'''

w90 = pywannier90.W90(kmf, nk, num_wann, gamma = False, other_keywords = keywords)
w90.use_bloch_phases = True
w90.kernel()
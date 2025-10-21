"""
pyWannier90: Python interface to Wannier90
==========================================

Simplified f2py-based build system (no C++ required)
"""

from numpy.distutils.core import setup, Extension
import os
import sys

# Configuration - users should set these via environment variables or edit here
W90DIR = os.environ.get('W90DIR', '/usr/local/wannier90')
LIBDIR = os.environ.get('LIBDIR', '/usr/lib')

# Check if Wannier90 library exists
if not os.path.exists(W90DIR):
    print(f"WARNING: Wannier90 directory not found: {W90DIR}")
    print("Please set W90DIR environment variable or edit setup.py")
    print("Example: export W90DIR=/path/to/wannier90")

# Platform-specific settings
if sys.platform == 'darwin':
    # macOS
    extra_link_args = [f'-Wl,-rpath,{W90DIR}']
    lapack_libs = ['lapack', 'blas']
elif sys.platform == 'linux':
    # Linux
    extra_link_args = [f'-Wl,-rpath={W90DIR}']
    lapack_libs = ['lapack', 'blas']
else:
    # Other platforms
    extra_link_args = []
    lapack_libs = ['lapack', 'blas']

# Define the extension module
libwannier90_ext = Extension(
    name='libwannier90',
    sources=['src/wannier_lib.F90'],
    include_dirs=[f'{W90DIR}/src'],
    library_dirs=[W90DIR, f'{LIBDIR}/lib'],
    libraries=['wannier'] + lapack_libs,
    extra_link_args=extra_link_args,
    extra_f90_compile_args=['-O3', '-fPIC'],
)

# Setup configuration
setup(
    name='pyWannier90',
    version='2.0.0',
    description='Python interface to Wannier90 (simplified f2py-based)',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Hung Q. Pham',
    author_email='pqh3.14@gmail.com',
    url='https://github.com/hungpham2017/pyWannier90',
    license='BSD-3-Clause',

    # Package data
    py_modules=['pywannier90'],
    package_dir={'': 'src'},

    # Extension modules
    ext_modules=[libwannier90_ext],

    # Dependencies
    install_requires=[
        'numpy>=1.16',
        'scipy>=1.3',
        'pyscf>=1.5',
    ],

    # Python version requirement
    python_requires='>=3.6',

    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Fortran',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)

from distutils.core import setup
from Cython.Build import cythonize

setup(name = 'python wrapper',
      ext_modules = cythonize(['wrapper.pyx']))

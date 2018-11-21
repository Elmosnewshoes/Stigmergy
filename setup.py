from distutils.core import setup
from Cython.Build import cythonize

setup(name = 'location modules',
      ext_modules = cythonize(['cythonic/plugins/*.pyx',
                              'cythonic/wrapper.pyx',
                              'cythonic/core/*.pyx',
	]))

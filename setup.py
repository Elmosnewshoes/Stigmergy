from distutils.core import setup
from Cython.Build import cythonize

setup(name = 'stigmergy',
      ext_modules = cythonize(['cythonic/plugins/*.pyx',
                              'cythonic/*.pyx',
                              'cythonic/core/*.pyx',],
                              compiler_directives={'embedsignature': True,
                                                   'boundscheck': False,
                                                   'wraparound': False,
                                                   'nonecheck': False,
                                                   'cdivision': True,
                                                   'initializedcheck': False,
                                                   'profile': True,
                                                   'language_level':3}))

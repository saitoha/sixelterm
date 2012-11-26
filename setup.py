# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sixelterm import __version__, __license__, __author__

setup(name                  = 'sixelterm',
      version               = __version__,
      description           = 'Display JPEG/PNG image with cat command, on some terminals support SIXEL (RLogin/mlterm/tanasinn). Inspired by GateOne.',
      long_description      = open("README.rst").read(),
      py_modules            = ['sixelterm'],
      eager_resources       = [],
      classifiers           = ['Development Status :: 4 - Beta',
                               'Topic :: Terminals',
                               'Environment :: Console',
                               'Intended Audience :: End Users/Desktop',
                               'License :: OSI Approved :: GNU General Public License (GPL)',
                               'Programming Language :: Python'
                               ],
      keywords              = 'sixel terminal',
      author                = __author__,
      author_email          = 'user@zuse.jp',
      url                   = 'https://github.com/saitoha/sixelterm',
      license               = __license__,
      packages              = find_packages(exclude=[]),
      zip_safe              = True,
      include_package_data  = False,
      install_requires      = ['PySixel ==0.0.5, <0.1.0', 'tff >=0.0.10, <0.1.0'],
      entry_points          = """
                              [console_scripts]
                              sixelterm = sixelterm:main
                              """
      )


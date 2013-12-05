# encoding: utf-8

from __future__ import absolute_import

try:
    from ._audiocalc import *
    print("Using Cython implementation of 'audiocalc'.")
except ImportError:
    from .py_audiocalc import *
    print("Using Python implementation of 'audiocalc'.")

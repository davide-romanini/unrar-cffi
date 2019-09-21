import os
from cffi import FFI

#unrarsrc = os.path.realpath(os.path.dirname(__file__))
unrarsrc = "unrarsrc"

builder = FFI()
with open(os.path.join(unrarsrc, "dll.preprocessed.h")) as f:
     builder.cdef(f.read())

builder.set_source("_unrarlib",
"""
#include "raros.hpp"
#include "dll.hpp"
""",     
     extra_objects=["%s/libunrar.a" % unrarsrc],
     include_dirs=[unrarsrc],
     libraries=["stdc++"]
)

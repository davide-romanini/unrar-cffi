import os
from cffi import FFI

unrarsrc = "unrarsrc"

builder = FFI()
with open(os.path.join(unrarsrc, "dll.preprocessed.h")) as f:
     builder.cdef(f.read(), packed=True)

builder.set_source("unrar.cffi._unrarlib",
"""
#include "raros.hpp"
#include "dll.hpp"
""",     
     extra_objects=["%s/libunrar.a" % unrarsrc],
     include_dirs=[unrarsrc],
     libraries=["stdc++"]     
)

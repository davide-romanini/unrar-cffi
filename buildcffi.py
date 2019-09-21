import os
from cffi import FFI

unrarsrc = "unrarsrc"

builder = FFI()
with open("unrarlib_py.preprocessed.h") as f:
     builder.cdef(f.read(), packed=True)

with open("unrarlib_ext.c") as f:
     builder.set_source("unrar.cffi._unrarlib",f.read(),     
          extra_objects=["%s/libunrar.a" % unrarsrc],
          include_dirs=[".", unrarsrc],
          libraries=["stdc++"]     
     )

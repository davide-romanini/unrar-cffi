from cffi import FFI
from buildconf import SOURCE_PARAMETERS

builder = FFI()
with open("unrarlib_py.preprocessed.h") as f:
     builder.cdef(f.read(), packed=True)

with open("unrarlib_ext.c") as f:
     builder.set_source("unrar.cffi._unrarlib", f.read(), **SOURCE_PARAMETERS)

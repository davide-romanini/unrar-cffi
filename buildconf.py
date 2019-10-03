import platform
import subprocess
from os import getenv
from os.path import realpath, dirname, join
from distutils import log
from distutils.cmd import Command

UNRARSRC = "unrarsrc"

# UNIX like OS
SOURCE_PARAMETERS = {
     'extra_objects': ["{}/libunrar.a".format(UNRARSRC)],
     'include_dirs': ["unrar/cffi", UNRARSRC],
     'libraries': ["stdc++"]  
}
DATA_FILES = []
BUILD_CMD = [getenv("MAKE", 'make'), "-C", UNRARSRC, "lib"]
PREPROCESS_CMD = [
    getenv("CC", "cc"),
    "-I", UNRARSRC,
    "-P",
    "-U", "__cplusplus",
    "-E", "unrar/cffi/unrarlib_py.h"
]

if platform.system() == 'Windows':
    bits = platform.architecture()[0][0:2]
    build_platform = "x64" if bits == "64" else "Win32"
    build_dir = join(realpath(dirname(__file__)), "unrar/cffi")
    build_platform_toolset = getenv("PLATFORM_TOOLSET", "v141")
    SOURCE_PARAMETERS = {                    
        'library_dirs': [build_dir],
        'include_dirs': ["unrar/cffi", UNRARSRC],
        'libraries': ["unrar"],
        'extra_link_args': ["/DEF:{}/dll.def".format(UNRARSRC)]          
    }
    DATA_FILES = [
        ('unrar/cffi', ['{}/unrar.dll'.format(build_dir)])
    ]
    BUILD_CMD = [
        "MSBuild.exe", 
        "{}/UnRARDll.vcxproj".format(UNRARSRC), 
        "/p:PlatformToolset={}".format(build_platform_toolset), 
        "/p:Configuration=Release", 
        "/p:Platform={}".format(build_platform),
        "/p:OutDir={}".format(build_dir)
    ]
    
    PREPROCESS_CMD = [
        "CL.exe",
        "/EP",
        "/I{}".format(UNRARSRC),
        "/D", "CALLBACK=WINAPI",
        "/D", "PASCAL=WINAPI",
        "/U", "__cplusplus",
        "unrar/cffi/unrarlib_py.h"
    ]


class BuildUnrarCommand(Command):
    description = 'build unrar library'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        log.info("compiling unrar library")
        subprocess.check_call(BUILD_CMD) 

def create_builder():
    from cffi import FFI
    log.info("preprocessing extension headers")
    preprocess = subprocess.check_output(PREPROCESS_CMD, universal_newlines=True)
    
    builder = FFI()
    builder.cdef(preprocess, packed=True)

    with open("unrar/cffi/unrarlib_ext.c") as f:
        builder.set_source("unrar.cffi._unrarlib", f.read(), **SOURCE_PARAMETERS)
    return builder

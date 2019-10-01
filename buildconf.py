import platform

UNRARSRC = "unrarsrc"

# UNIX like OS
SOURCE_PARAMETERS = {
     'extra_objects': ["{}/libunrar.a".format(UNRARSRC)],
     'include_dirs': [".", UNRARSRC],
     'libraries': ["stdc++"]  
}
DATA_FILES = []

if platform.system() == 'Windows':
    bits = platform.architecture()[0][0:2]
    build_dir = "{}/build/unrardll{}/Release".format(UNRARSRC, bits)
    SOURCE_PARAMETERS = {                    
        'library_dirs': [build_dir],
        'include_dirs': [".", UNRARSRC],
        'libraries': ["unrar"],
        'extra_link_args': ["/DEF:{}/dll.def".format(UNRARSRC)]          
    }
    DATA_FILES = [
        ('unrar/cffi', ['{}/unrar.dll'.format(build_dir)])
    ]
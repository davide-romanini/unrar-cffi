from ._unrarlib import ffi
from ._unrarlib.lib import RAROpenArchiveEx, RARCloseArchive

RAR_OM_LIST_INCSPLIT = 2
SUCCESS = 0

def is_rarfile(filename):
    """Return true if file is a valid RAR file."""
    archive = new_RAROpenArchiveDataEx(filename, RAR_OM_LIST_INCSPLIT)
    
    handle = RAROpenArchiveEx(archive)    
    
    RARCloseArchive(handle)
    return archive.OpenResult == SUCCESS

def new_RAROpenArchiveDataEx(filename, mode):
    return ffi.new("struct RAROpenArchiveDataEx *", {
        'ArcNameW': ffi.new("wchar_t[]", filename),
        'OpenMode': mode
    })
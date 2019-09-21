from ._unrarlib import ffi
from ._unrarlib.lib import \
    RAROpenArchiveEx, \
    RARCloseArchive, \
    RARReadHeaderEx, \
    RARSetCallbackPtr, \
    RARProcessFileW, \
    UCM_PROCESSDATA, \
    PyUNRARCALLBACKStub

ERAR_END_ARCHIVE = 10
RAR_OM_LIST_INCSPLIT = 2
RAR_OM_EXTRACT = 1
RAR_SKIP = 0
RAR_TEST = 1
RAR_EXTRACT = 2
SUCCESS = 0

@ffi.def_extern('PyUNRARCALLBACKStub')
def PyUNRARCALLBACKSkeleton(msg, user_data, p1, p2):    
    callback = ffi.from_handle(user_data)
    return callback(msg, p1, p2)

class RarArchive(object):
    @staticmethod
    def open(filename):
        return RarArchive(filename, RAR_OM_LIST_INCSPLIT)
        
    @staticmethod
    def open_to_extract(filename):
        return RarArchive(filename, RAR_OM_EXTRACT)

    def __init__(self, filename, mode):
        archive = RAROpenArchiveDataEx(filename, mode)
        self.handle = RAROpenArchiveEx(archive)
        assert archive.OpenResult == SUCCESS

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        result = RARCloseArchive(self.handle)
        assert result == SUCCESS

    def headers(self):
        header_data = RARHeaderDataEx()
        res = RARReadHeaderEx(self.handle, header_data)    
        while res == SUCCESS:
            yield RarHeader(self.handle, header_data)
            header_data = RARHeaderDataEx()
            res = RARReadHeaderEx(self.handle, header_data)

class RarHeader(object):
    def __init__(self, handle, headerDataEx):
        self.handle = handle
        self.headerDataEx = headerDataEx
    
    @property
    def FileNameW(self):
        return ffi.string(self.headerDataEx.FileNameW)
    
    def skip(self):
        RARProcessFileW(self.handle, RAR_SKIP, ffi.NULL, ffi.NULL)

    def test(self, callback):
        def wrapper(msg, p1, p2):
            if msg == UCM_PROCESSDATA:
                chunk = ffi.buffer(ffi.cast("char *", p1), p2)                
                callback(bytes(chunk))
            return 1
        user_data = ffi.new_handle(wrapper)
        RARSetCallbackPtr(self.handle, PyUNRARCALLBACKStub, user_data)
        RARProcessFileW(self.handle, RAR_TEST, ffi.NULL, ffi.NULL)
        RARSetCallbackPtr(self.handle, ffi.NULL, ffi.NULL)


def RAROpenArchiveDataEx(filename, mode):
    return ffi.new("struct RAROpenArchiveDataEx *", {
        'ArcNameW': ffi.new("wchar_t[]", filename),
        'OpenMode': mode
    })

def RARHeaderDataEx():
    return ffi.new("struct RARHeaderDataEx *")
from ._unrarlib import ffi
from ._unrarlib.lib import \
    RAROpenArchiveEx, \
    RARCloseArchive, \
    RARReadHeaderEx, \
    RARSetCallbackPtr, \
    RARProcessFileW, \
    UCM_PROCESSDATA, \
    PyUNRARCALLBACKStub, \
    C_RAR_OM_LIST_INCSPLIT, \
    C_RAR_OM_EXTRACT, \
    C_RAR_SKIP, \
    C_RAR_TEST, \
    C_RAR_EXTRACT, \
    C_ERAR_SUCCESS, \
    C_RHDF_DIRECTORY

FLAGS_RHDF_DIRECTORY = C_RHDF_DIRECTORY

@ffi.def_extern('PyUNRARCALLBACKStub')
def PyUNRARCALLBACKSkeleton(msg, user_data, p1, p2):    
    callback = ffi.from_handle(user_data)
    return callback(msg, p1, p2)

class RarArchive(object):

    @staticmethod
    def open_for_metadata(filename):
        return RarArchive(filename, C_RAR_OM_LIST_INCSPLIT)
        
    @staticmethod
    def open_for_processing(filename):
        return RarArchive(filename, C_RAR_OM_EXTRACT)

    def __init__(self, filename, mode):
        self.comment = ''
        archive = RAROpenArchiveDataEx(filename, mode)        
        self.handle = RAROpenArchiveEx(archive.value)
        if archive.value.OpenResult != C_ERAR_SUCCESS:
            raise BadRarFile("Cannot open {}: OpenResult is {}".format(filename, archive.value.OpenResult))
        self.comment = ffi.string(archive.value.CmtBufW)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        result = RARCloseArchive(self.handle)        
        assert result == C_ERAR_SUCCESS

    def iterate_headers(self):
        header_data = RARHeaderDataEx()
        res = RARReadHeaderEx(self.handle, header_data)    
        while res == C_ERAR_SUCCESS:
            yield RarHeader(self.handle, header_data)
            header_data = RARHeaderDataEx()
            res = RARReadHeaderEx(self.handle, header_data)

def null_callback(*args):
    pass

class RarHeader(object):
    def __init__(self, handle, headerDataEx):
        self.handle = handle
        self.headerDataEx = headerDataEx
    
    @property
    def FileNameW(self):
        return ffi.string(self.headerDataEx.FileNameW)
    
    @property
    def FileTime(self):
        return self.headerDataEx.FileTime
    
    @property
    def PackSize(self):
        return self.headerDataEx.PackSize    

    @property
    def PackSizeHigh(self):
        return self.headerDataEx.PackSizeHigh

    @property
    def UnpSize(self):
        return self.headerDataEx.UnpSize

    @property
    def UnpSizeHigh(self):
        return self.headerDataEx.UnpSizeHigh

    @property
    def UnpVer(self):
        return self.headerDataEx.UnpVer

    @property
    def FileCRC(self):
        return self.headerDataEx.FileCRC

    @property
    def Flags(self):
        return self.headerDataEx.Flags

    @property
    def HostOS(self):
        return self.headerDataEx.HostOS

    @property
    def Method(self):
        return self.headerDataEx.Method

    def skip(self):
        RARProcessFileW(self.handle, C_RAR_SKIP, ffi.NULL, ffi.NULL)

    def test(self, callback = null_callback):
        def wrapper(msg, p1, p2):
            if msg == UCM_PROCESSDATA:
                chunk = ffi.buffer(ffi.cast("char *", p1), p2)                
                callback(bytes(chunk))
            return 1
        user_data = ffi.new_handle(wrapper)
        RARSetCallbackPtr(self.handle, PyUNRARCALLBACKStub, user_data)
        result = RARProcessFileW(self.handle, C_RAR_TEST, ffi.NULL, ffi.NULL)
        RARSetCallbackPtr(self.handle, ffi.NULL, ffi.NULL)
        if result != C_ERAR_SUCCESS:
            raise BadRarFile("Rarfile corrupted: error code is %d" % result)
        
class BadRarFile(Exception):
    pass

class RAROpenArchiveDataEx(object):
    def __init__(self, filename, mode):
        COMMENT_MAX_SIZE = 64 * 1024        
        self.arcNameW = ffi.new("wchar_t[]", filename)
        self.cmtBufW = ffi.new("wchar_t[{}]".format(COMMENT_MAX_SIZE))
        self.value = ffi.new("struct RAROpenArchiveDataEx *", {
            'ArcNameW': self.arcNameW,
            'OpenMode': mode,
            'CmtBufSize': ffi.sizeof("wchar_t") * COMMENT_MAX_SIZE,
            'CmtBufW': self.cmtBufW
        })
    
    def value(self):
        return self.value

def RARHeaderDataEx():
    return ffi.new("struct RARHeaderDataEx *")

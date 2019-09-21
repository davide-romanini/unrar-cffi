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

def is_rarfile(filename):
    """Return true if file is a valid RAR file."""
    archive = RAROpenArchiveDataEx(filename, RAR_OM_LIST_INCSPLIT)    
    handle = RAROpenArchiveEx(archive)    
    RARCloseArchive(handle)
    return archive.OpenResult == SUCCESS

class RarFile(object):
    def __init__(self, filename):
        """Load RAR archive file with mode read only "r"."""
        self.filename = filename
        archive = RAROpenArchiveDataEx(filename, RAR_OM_LIST_INCSPLIT)
        handle = RAROpenArchiveEx(archive)
    
        assert archive.OpenResult == SUCCESS
        self.filenames = []
        header_data = RARHeaderDataEx()
        res = RARReadHeaderEx(handle, header_data)
        while res == SUCCESS:                 
            self.filenames.append(ffi.string(header_data.FileNameW))
            header_data = RARHeaderDataEx()
            RARProcessFileW(handle, RAR_SKIP, ffi.NULL, ffi.NULL)
            res = RARReadHeaderEx(handle, header_data)
        print(res)

        RARCloseArchive(handle)

    def namelist(self):
        return self.filenames

    def read(self, member):
        #if isinstance(member, RarInfo):
        #    member = member.filename

        archive = RAROpenArchiveDataEx(self.filename, RAR_OM_EXTRACT)
        handle = RAROpenArchiveEx(archive)
        assert archive.OpenResult == SUCCESS        

        processor = RarDataProcessor()
        data_holder = ffi.new_handle(processor)
        header_data = RARHeaderDataEx()
        RARSetCallbackPtr(handle, PyUNRARCALLBACKStub, data_holder)
        res = RARReadHeaderEx(handle, header_data)        
        while res == SUCCESS:
            if ffi.string(header_data.FileNameW) == member:
                RARProcessFileW(handle, RAR_TEST, ffi.NULL, ffi.NULL)
                break
            else:
                RARProcessFileW(handle, RAR_SKIP, ffi.NULL, ffi.NULL)
            res = RARReadHeaderEx(handle, header_data)

        RARCloseArchive(handle)
        return processor.data


class RarDataProcessor:
    def __init__(self):
        self.data = b''
    def __call__(self, msg, p1, p2):
        if msg == UCM_PROCESSDATA:
            chunk = ffi.buffer(ffi.cast("char *", p1), p2)                
            self.data += bytes(chunk)
        return 1

@ffi.def_extern('PyUNRARCALLBACKStub')
def PyUNRARCALLBACKSkeleton(msg, user_data, p1, p2):    
    callback = ffi.from_handle(user_data)
    return callback(msg, p1, p2)

def RAROpenArchiveDataEx(filename, mode):
    return ffi.new("struct RAROpenArchiveDataEx *", {
        'ArcNameW': ffi.new("wchar_t[]", filename),
        'OpenMode': mode
    })

def RARHeaderDataEx():
    return ffi.new("struct RARHeaderDataEx *")
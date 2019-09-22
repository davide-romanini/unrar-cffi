import io
from .unrarlib import RarArchive, BadRarFile

def is_rarfile(filename):
    """Return true if file is a valid RAR file."""
    try:
        with RarArchive.open_for_metadata(filename):        
            return True
    except:
        return False

class RarFile(object):
    def __init__(self, filename):
        """Load RAR archive file with mode read only "r"."""
        self.filename = filename
        self.filenames = []
        
        with RarArchive.open_for_metadata(filename) as rar:
            for header in rar.iterate_headers():
                self.filenames.append(header.FileNameW)
                header.skip()

    def namelist(self):
        return self.filenames

    def open(self, member):
        with RarArchive.open_for_processing(self.filename) as rar:
            for header in rar.iterate_headers():
                if header.FileNameW == member:
                    callback = InMemoryCollector()
                    header.test(callback)
                    return callback.bytes_io
                header.skip()

    def read(self, member):
        return self.open(member).read()
    
    def testrar(self):
        with RarArchive.open_for_processing(self.filename) as rar:
            for header in rar.iterate_headers():
                try:
                    header.test()
                except BadRarFile:
                    return header.FileNameW

class InMemoryCollector:
    def __init__(self):
        self._data = b''
    def __call__(self, chunk):              
        self._data += chunk

    @property
    def bytes_io(self):
        return io.BytesIO(self._data)
    
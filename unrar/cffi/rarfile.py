from .unrarlib import RarArchive

def is_rarfile(filename):
    """Return true if file is a valid RAR file."""
    try:
        with RarArchive.open(filename):        
            return True
    except:
        return False

class RarFile(object):
    def __init__(self, filename):
        """Load RAR archive file with mode read only "r"."""
        self.filename = filename
        self.filenames = []
        
        with RarArchive.open(filename) as rar:
            for header in rar.headers():
                self.filenames.append(header.FileNameW)
                header.skip()

    def namelist(self):
        return self.filenames

    def read(self, member):
        #if isinstance(member, RarInfo):
        #    member = member.filename
        with RarArchive.open_to_extract(self.filename) as rar:
            for header in rar.headers():
                if header.FileNameW == member:
                    processor = RarDataProcessor()
                    header.test(processor)
                    return processor.data
                header.skip()

class RarDataProcessor:
    def __init__(self):
        self.data = b''
    def __call__(self, chunk):              
        self.data += chunk
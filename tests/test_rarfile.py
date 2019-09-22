from os.path import realpath, dirname, join
from pytest import fixture
from unrar.cffi.rarfile import is_rarfile, RarFile

thisdir = realpath(dirname(__file__))

@fixture
def rar():
    return RarFile(join(thisdir, 'test_rar.rar'))

@fixture
def bad_rar():
    return RarFile(join(thisdir, 'test_corrupted.rar'))


def test_is_rarfile_good():
    good_rar = join(thisdir, 'test_rar.rar')
    assert is_rarfile(good_rar) == True

def test_is_rarfile_bad():
    non_rar = __file__
    assert is_rarfile(non_rar) == False

def test_is_rarfile_not_existing():
    non_existing = join(thisdir, 'non_existing.rar')
    assert is_rarfile(non_existing) == False

def test_rar_namelist(rar):
    assert rar.namelist() == ['test_file.txt', 'test_file2.txt']

def test_rar_read(rar):
    assert rar.read('test_file.txt') == b'This is for test.'
    assert rar.read('test_file2.txt') == b'This is another test!\n'

def test_rar_open(rar):
    assert rar.open('test_file.txt').read() == b'This is for test.'

def test_rar_testrar_good(rar):
    assert rar.testrar() == None

def test_rar_testrar_bad(bad_rar):
    assert bad_rar.testrar() == 'test_file.txt'

def test_rar_infolist(rar):
    info1 = {
        'filename': 'test_file.txt',
        'date_time': (2013,4,14,19,3,36),
        'compress_type': 0x33,
        'create_system': 3,
        'extract_version': 29,        
        'flag_bits': 0,
        'CRC': 2911469160,
        'compress_size': 29,
        'file_size': 17
    }
    info2 = {
        'filename': 'test_file2.txt',
        'date_time': (2019,9,21,22,47,34),
        'compress_type': 0x30,
        'create_system': 3,
        'extract_version': 29,        
        'flag_bits': 0,
        'CRC': 1864074135,
        'compress_size': 22,
        'file_size': 22
    }
    assert rar.infolist()[0].__dict__ == info1
    assert rar.infolist()[1].__dict__ == info2
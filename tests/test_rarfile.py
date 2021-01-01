from os.path import realpath, dirname, join
from pytest import fixture, raises
from unrar.cffi.rarfile import is_rarfile, RarFile, RarFileError

thisdir = realpath(dirname(__file__))

@fixture
def rar():
    return RarFile(join(thisdir, 'test_rar.rar'))

@fixture
def rar_no_comment():
    return RarFile(join(thisdir, 'test_no_cmt.rar'))

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

def test_open_not_existing():
    with raises(RarFileError):
        RarFile(join(thisdir, 'non_existing.rar'))

def test_rar_namelist(rar):
    assert rar.namelist() == ['test_file.txt', 'test_file2.txt', join('testdir', 'testfile'), 'testdir']

def test_rar_read(rar):
    assert rar.read('test_file.txt') == b'This is for test.'
    assert rar.read('test_file2.txt') == b'This is another test!\n'
    assert rar.read(rar.getinfo('test_file2.txt')) == b'This is another test!\n'

def test_rar_open(rar):
    assert rar.open('test_file.txt').read() == b'This is for test.'
    assert rar.open(rar.getinfo('test_file.txt')).read() == b'This is for test.'
    with raises(ValueError):
        rar.open('not_existing')

def test_rar_comment(rar):
    assert rar.comment == bytes('this is a test rar comment àòùç€\n', 'utf-8')

def test_rar_comment_empty(rar_no_comment):
    assert rar_no_comment.comment == b''

def test_rar_testrar_good(rar):
    assert rar.testrar() == None

def test_rar_testrar_bad(bad_rar):
    assert bad_rar.testrar() == 'test_file.txt'

@fixture
def info_test_file_txt():
    return {
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

@fixture
def info_test_file2_txt():
    return {
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

def test_rar_infolist(rar, info_test_file_txt, info_test_file2_txt):
    assert rar.infolist()[0].__dict__ == info_test_file_txt
    assert rar.infolist()[1].__dict__ == info_test_file2_txt

def test_rar_getinfo(rar, info_test_file_txt):
    assert rar.getinfo('test_file.txt').__dict__ == info_test_file_txt
    with raises(KeyError):
        rar.getinfo('not_existing')

def test_rar_is_dir(rar):
    assert rar.getinfo(join('testdir', 'testfile')).is_dir() == False
    assert rar.getinfo('testdir').is_dir()

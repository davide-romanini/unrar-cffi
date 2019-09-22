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
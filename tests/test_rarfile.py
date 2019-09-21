from os.path import realpath, dirname, join
from pytest import fixture
from unrar.cffi.rarfile import is_rarfile

thisdir = realpath(dirname(__file__))

def test_is_rarfile_good():
    good_rar = join(thisdir, 'test_rar.rar')
    assert is_rarfile(good_rar) == True

def test_is_rarfile_bad():
    non_rar = __file__
    assert is_rarfile(non_rar) == False

def test_is_rarfile_not_existing():
    non_existing = join(thisdir, 'non_existing.rar')
    assert is_rarfile(non_existing) == False
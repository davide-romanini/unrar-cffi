from unrar.cffi._unrarlib.lib import RARGetDllVersion

def test_rar_version():
    assert RARGetDllVersion() == 8
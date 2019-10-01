from buildconf import DATA_FILES
from setuptools import setup, find_packages

setup(
    name='unrar-cffi',
    use_scm_version=True,
    packages=(
        'unrar.cffi',
    ),
    install_requires=[
        "cffi"      
    ],
    setup_requires=[
        "cffi",
        "pytest-runner",
        "wheel",
        "setuptools_scm"
    ],
    tests_require=[
        "pytest"
    ],
    data_files=DATA_FILES,
    cffi_modules=["buildcffi.py:builder"]      
)


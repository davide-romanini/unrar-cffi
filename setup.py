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
    cffi_modules=["buildcffi.py:builder"]      
)


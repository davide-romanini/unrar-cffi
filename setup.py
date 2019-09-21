from setuptools import setup, find_packages

setup(
    name='unrar-cffi',
    packages=(
        'unrar.cffi',
    ),
    install_requires=[
        "cffi"      
    ],
    setup_requires=[
        "cffi",
        "pytest-runner",
        "wheel"
    ],
    tests_require=[
        "pytest"
    ],    
    cffi_modules=["buildcffi.py:builder"]      
)


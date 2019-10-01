from setuptools import setup
from buildconf import BuildUnrarCommand

setup(
    cmdclass={
        'build_unrar': BuildUnrarCommand
    },
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
    package_dir={
        'unrar.cffi': 'unrar/cffi'
    },
    package_data={
        'unrar.cffi': ['*.dll']
    },
    include_package_data=True,
    cffi_modules=["buildconf.py:create_builder"]  
)


[![Build Status](https://travis-ci.org/davide-romanini/unrar-cffi.svg?branch=develop)](https://travis-ci.org/davide-romanini/unrar-cffi)

# unrar-cffi -- Work with RAR files.

## Description

unrar-cffi is a python extension that exposes [unrar library](https://rarlab.com/rar_add.htm)
functionality through a [`zipfile`](https://docs.python.org/3/library/zipfile.html)-like interface.

## Features

The package implements the following `RarFile` functions:

 * `namelist()`
 * `infolist()`
 * `getinfo()`
 * `read()`
 * `open()`
 * `testrar()`
 * `rarfile.is_rar_file()`

## Usage

 1. Install with PIP:

    `pip install unrar-cffi`

 2. Use from code:

```python
    from unrar.cffi import rarfile

    rar = rarfile.RarFile('sample.rar')

    assert rar.testrar() == None

    for filename in rar.namelist():
        info = rar.getinfo(filename)
        print("Reading {}, {}, {} bytes ({} bytes compressed)".format(info.filename, info.date_time, info.file_size, info.compress_size))
        data = rar.read(filename)
        print("\t{}...\n".format(data[:100]))
```

## Build

### Requirements

Linux:
 * gcc compiler suite (`build-essential` packages should be enough)
 * docker (only for `buildmanylinux`)

Windows:
 * VS2017 Build Tools (PLATFORM_TOOLSET=v141)
 * Visual C++ compiler suite

### Compile and test

 1. `./build.sh init`
 2. `./build.sh build`
 3. `./build.sh test`

If you have docker installed, you can build all the [manylinux](https://github.com/pypa/manylinux) 
wheels:

 1. `./build.sh within [manylinux docker image] buildmanylinux`
 2. `./build.sh within [manylinux docker image] testmanylinux`

By deafult the image `quay.io/pypa/manylinux2010_x86_64` will be used.
Use `$DOCKER_IMAGE` and `$PLAT` variables to customize the build.
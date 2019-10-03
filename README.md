# unrar-cffi

`ZipFile` like interface to RAR files, read only.

Similar to [python-unrar](https://github.com/matiasb/python-unrar) but using
CFFI instead of ctypes.


## Build

 1. `./build.sh init`
 2. `./build.sh build`
 3. `./build.sh test`

To build all [manylinux2010](https://github.com/pypa/manylinux) wheels:

 1. `./build.sh manylinux`

Note that you'll need `docker` installed. 
By deafult the image `quay.io/pypa/manylinux2010_x86_64` will be used.
Use `$DOCKER_IMAGE` and `$PLAT` variables to customize the build.
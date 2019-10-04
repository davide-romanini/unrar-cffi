#!/bin/sh
set -o nounset
set -o errexit

PYTHON=${PYTHON:-python}
PIP=${PIP:-pip}
UNRAR_VERSION="5.8.2"
OS=${OS:-unix}
DOCKER_IMAGE=${DOCKER_IMAGE:-quay.io/pypa/manylinux2010_x86_64}
PLAT=${PLAT:-manylinux2010_x86_64}
PYTEST=${PYTEST:-pytest}

init () {
    $PIP install -r requirements.txt
    mkdir -p unrarsrc
	curl https://www.rarlab.com/rar/unrarsrc-$UNRAR_VERSION.tar.gz |tar -xz -C unrarsrc --strip-components=1
}

build () {
    if [ "$OS" = "Windows_NT" ]; then
        cmd "/C build_win.bat $PIP wheel . -w dist"
    else
        $PIP wheel . -w dist
    fi
}

test () {
    $PIP install unrar-cffi -f dist/
    $PYTEST
}

sdist () {
    $PYTHON setup.py sdist
}

manylinux () {
    docker run --rm -t -v $PWD:/io -w /io $DOCKER_IMAGE \
       sh -c 'for PYBIN in /opt/python/cp3*/bin; do export PIP="$PYBIN/pip" && ./build.sh build; done'
    
    docker run --rm -t -e PLAT=$PLAT -v $PWD:/io -w /io $DOCKER_IMAGE \
       sh -c 'for whl in dist/*.whl; do auditwheel repair "$whl" --plat $PLAT -w dist/; done'

    docker run --rm -t -v $PWD:/io -w /io $DOCKER_IMAGE \
       sh -c 'for PYBIN in /opt/python/cp3*/bin; do export PIP="$PYBIN/pip" && export PYTEST="$PYBIN/pytest" && $PIP install -r requirements.txt && ./build.sh test; done'

}

"$@"
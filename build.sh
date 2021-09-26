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
SETUPTOOLS_SCM_PRETEND_VERSION=${SETUPTOOLS_SCM_PRETEND_VERSION:-}

init () {
    $PIP install -r requirements.txt
    mkdir -p unrarsrc
	curl https://www.rarlab.com/rar/unrarsrc-$UNRAR_VERSION.tar.gz |tar -xz -C unrarsrc --strip-components=1
}

build () {
    destination=${1:-dist}
    if [ "$OS" = "Windows_NT" ]; then
        cmd "/C build_win.bat $PIP wheel . -w $destination --no-deps"
    else
        $PIP wheel . -w $destination --no-deps
    fi
}

test () {
    rm -Rf tests/__pycache__
    $PIP install unrar-cffi -f dist/
    $PYTEST
}

publish () {
    twine upload --skip-existing dist/*
}

# to be run from ci system
buildci () {
    os=${1:-linux}
    init
    if [ "$os" = "linux" ]; then
        $PYTHON setup.py sdist
        within $DOCKER_IMAGE buildmanylinux
    else
        build dist
    fi
}

testci () {
    os=${1:-linux}    
    if [ "$os" = "linux" ]; then        
        within $DOCKER_IMAGE testmanylinux
    else
        test
    fi
}

within () {
    image=${1:-$DOCKER_IMAGE}
    shift
    docker run --rm -t -e PLAT=$PLAT -e SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION \
       -v $PWD:/io -w /io $image ./build.sh "$@"
}

# to be run inside manylinux docker image
buildmanylinux () {
    for PYBIN in /opt/python/cp3[5,6,7,8,9]*/bin; do
        PIP="$PYBIN/pip"
        build /tmp
    done
    for whl in /tmp/*.whl; do 
        auditwheel repair "$whl" --plat $PLAT -w dist/
    done
}

testmanylinux () {
    for PYBIN in /opt/python/cp3[5,6,7,8,9]*/bin; do
        PIP="$PYBIN/pip"
        PYTEST="$PYBIN/pytest"
        $PIP install pytest 
        test
    done
}

"$@"
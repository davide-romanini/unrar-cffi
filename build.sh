#!/bin/sh
set -o nounset
set -o errexit

PYTHON=${PYTHON:-python}
UNRAR_VERSION="5.8.2"

init () {
    mkdir -p unrarsrc
	curl https://www.rarlab.com/rar/unrarsrc-$UNRAR_VERSION.tar.gz |tar -xz -C unrarsrc --strip-components=1
}

build () {
    if [ "$OS" = "Windows_NT" ]; then
        cmd "/C build_win.bat setup.py build_unrar build_ext"
    else
        $PYTHON setup.py build_unrar build_ext
    fi    
}

test () {
    if [ "$OS" = "Windows_NT" ]; then
        cmd "/C build_win.bat setup.py test"
    else
        $PYTHON setup.py test
    fi    
}

package () {
    if [ "$OS" = "Windows_NT" ]; then
        cmd "/C build_win.bat setup.py sdist bdist_wheel"
    else
        $PYTHON setup.py sdist bdist_wheel
    fi
}

"$@"
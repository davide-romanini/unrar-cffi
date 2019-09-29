UNRAR_VERSION := 5.8.2

all: unrarsrc
	# generate header file from dll.hpp for cffi cdef()
	cc -I unrarsrc -P -U __cplusplus -E unrarlib_py.h > unrarlib_py.preprocessed.h
	python setup.py build_ext develop

unrarsrc:
	mkdir -p unrarsrc
	curl https://www.rarlab.com/rar/unrarsrc-$(UNRAR_VERSION).tar.gz |tar -xz -C unrarsrc --strip-components=1
	$(MAKE) -C unrarsrc lib
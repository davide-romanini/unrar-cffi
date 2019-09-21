all: unrarsrc
	# generate header file from dll.hpp for cffi cdef()
	cd unrarsrc; cc -P -include raros.hpp -U __cplusplus -E dll.hpp > dll.preprocessed.h
	python setup.py build_ext

unrarsrc:
	mkdir -p unrarsrc
	wget https://www.rarlab.com/rar/unrarsrc-5.8.1.tar.gz -O -|tar -xz -C unrarsrc unrar --strip-components=1
	$(MAKE) -C unrarsrc lib
UNRAR_VERSION := 5.8.2
PYTHON ?= python
all: unrarsrc
	$(PYTHON) setup.py build_unrar build_ext develop

unrarsrc:
	mkdir -p unrarsrc
	curl https://www.rarlab.com/rar/unrarsrc-$(UNRAR_VERSION).tar.gz |tar -xz -C unrarsrc --strip-components=1
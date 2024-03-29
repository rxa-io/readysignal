ifeq ($(OS), Windows_NT)
	BIN = Scripts
	OS_PYTHON = python
	ACTIVATE = activate.bat
else
	BIN = bin
	OS_PYTHON = python3
	ACTIVATE = activate
endif

PYTHON = $(OS_PYTHON)

.PHONY: tests

html:
	# Running sphinx-build to build html files in build folder.
	rm -r docs
	mkdir docs
	sphinx-build -M html doc_source docs
	rsync -a docs/html/ docs/
	rm -r docs/html

release:
	$(PYTHON) -m build

tests:
	# Running unittests
	@$(PYTHON) -m unittest

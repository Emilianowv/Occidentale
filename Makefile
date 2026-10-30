.PHONY: test check build
test:
	python3 -m unittest discover -s tests -v
check: test
	./romancescript test
	python3 scripts/check_windows_klc.py
	python3 scripts/audit.py
build:
	python3 scripts/build.py

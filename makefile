
.PHONY: clean run_app run_celery set_pythonpath


PYTHON=$(shell pwd)/.venv/bin/python
PYTHONPATH=$(shell pwd)/core

run_app:export PYTHONPATH:=$(PYTHONPATH)
run_app:
	$(PYTHON) -m uvicorn app:app --workers 1 --host 192.168.9.31 --port 7002



clean:
	@echo "Cleaning up..."

PY ?= python3
NPROC ?= $(shell nproc)

.PHONY: install test test-fast lint exp001 exp002 exp003 exp004 exp005 exp006 experiments report clean

install:
	$(PY) -m pip install -e ".[dev]"

test-fast:
	$(PY) -m pytest -q -m "not validation and not slow"

test:
	$(PY) -m pytest -q

lint:
	ruff check src tests experiments

exp001:
	$(PY) experiments/001_midsize_isoC_60mph_load_sweep/run.py --workers $(NPROC)
exp002:
	$(PY) experiments/002_roads_speeds_vehicles/run.py --workers $(NPROC)
exp003:
	$(PY) experiments/003_class8/run.py --workers $(NPROC)
exp004:
	$(PY) experiments/004_transmission_ratio/run.py --workers $(NPROC)
exp005:
	$(PY) experiments/005_bias_ratio_travel/run.py --workers $(NPROC)
exp006:
	$(PY) experiments/006_flywheel_tornado/run.py --workers $(NPROC)

experiments: exp001 exp002 exp003 exp004 exp005 exp006

# Regenerate every figure and table from the parquet results (no simulation).
report:
	$(PY) -m aks_lab.viz.report

clean:
	find . -name __pycache__ -type d -exec rm -rf {} +

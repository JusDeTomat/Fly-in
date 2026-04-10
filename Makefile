PYTHON			= python3
VENV			= .venv
VENV_BIN		= $(VENV)/bin
V_PYTHON		= $(VENV_BIN)/python
V_PIP			= $(VENV_BIN)/python -m pip
FLAKE			= $(VENV_BIN)/flake8
MYPY			= $(VENV_BIN)/mypy
DEPENDENCIES	= raylib flake8 mypy
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(V_PIP) install --upgrade pip

install: $(VENV)
	$(V_PIP) install $(DEPENDENCIES)

run: install
	$(V_PYTHON) Fly-in.py $(ARGS)

clean:
	rm -rf $(VENV) build_venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache
	rm -rf $(OUTPUT_FILE) dist/

lint: install
	$(FLAKE) . --exclude '$(VENV)'
	$(MYPY) $(MYPY_FLAGS) src

lint-strict: install
	$(FLAKE) . --exclude '$(VENV)'
	$(MYPY) $(MYPY_FLAGS) --strict src
	
.DEFAULT_GOAL := run
.PHONY: install run clean lint lint-strict
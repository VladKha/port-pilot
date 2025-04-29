.PHONY: setup

setup: create_venv install_requirements

create_venv:
	@echo "Creating Python virtual environment..."
	python -m venv .venv
	source .venv/bin/activate

install_requirements:
	@echo "Installing requirements..."
	pip install -U pip
	pip install -r requirements.txt

run_app:
	@echo "Starting AI agent chat..."
	python app.py
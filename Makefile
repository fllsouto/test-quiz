
ENV_FOLDER=.venv
ENV_ACTIVATE=.venv/bin/activate

setup_env:
	echo "Setting up virtual environment..."
	python3 -m venv $(ENV_FOLDER)

install_deps: setup_env
	echo "Installing dependencies..."
	. $(ENV_ACTIVATE) && pip install -r requirements.txt

setup_python: install_deps
	echo "Setting up Python environment"

test:
	echo "Running tests..."
	. $(ENV_ACTIVATE) && pytest tests.py
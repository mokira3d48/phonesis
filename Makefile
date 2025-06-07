full-install:
	python3 -m venv .venv
	.venv/bin/python3 --version
	.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m pip install -r requirements.txt
	.venv/bin/python3 -m pip install -e .

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest tests

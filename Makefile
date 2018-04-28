init:
	pip install codecov coverage
	pip install pipenv
	pipenv install --dev

test:
	pipenv run coverage run setup.py test

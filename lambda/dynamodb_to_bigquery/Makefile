SHELL = /bin/bash

all: dynamodb_to_bigquery.zip

dynamodb_to_bigquery.zip: ./venv/lib/python3.9/site-packages lambda_function.py
	cd ./venv/lib/python3.9/site-packages && \
	zip -x '**/__pycache__/*' -r9 ../../../../dynamodb_to_bigquery.zip .
	zip -g dynamodb_to_bigquery.zip lambda_function.py

./venv/lib/python3.9/site-packages: venv/updated

venv/updated: requirements.txt venv
	. venv/bin/activate ; \
	pip install -r requirements.txt google-cloud-bigquery ; \
	deactivate
	touch venv/updated

venv:
	[[ -d venv ]] || python3.9 -m venv venv

clean:
	rm -f dynamodb_to_bigquery.zip

deploy:
	AWS_PAGER= aws lambda update-function-code --function-name syncReservations --zip-file fileb://dynamodb_to_bigquery.zip

.PHONY: clean deploy

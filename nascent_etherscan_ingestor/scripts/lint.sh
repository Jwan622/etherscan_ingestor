#!/usr/bin/env bash
echo "Linting..."
poetry run flake8 ./src/* --count --select=E9,F63,F7,F82 --show-source --statistics
poetry run flake8 ./src/* --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

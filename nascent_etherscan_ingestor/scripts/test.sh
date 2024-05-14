#!/usr/bin/env bash
echo "Testing...using poetry"
poetry run pytest -s -vv --durations=0 tests

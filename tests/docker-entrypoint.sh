#!/bin/sh
./wait-for-it.sh postgres:5432 -t 10 -- echo "postgres is up"
alembic upgrade head
sleep 2
python -m coverage run -m pytest tests -p no:warnings
python -m coverage report
python3 -m flake8 bot
python3 -m flake8 tests

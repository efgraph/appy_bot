#!/bin/sh
./wait-for-it.sh postgres:5432 -t 10 -- echo "postgres is up"
alembic upgrade head
sleep 2
python3 -m pytest --cov=bot -p no:warnings
python3 -m flake8 bot

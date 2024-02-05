#!/bin/sh

python start_database.py
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 80
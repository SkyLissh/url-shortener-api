#!/usr/env/bin bash

set -o errexit
set -o nounset

alembic upgrade head
gunicorn -w 4 --bind 0.0.0.0:8000 app.main:app -k uvicorn.workers.UvicornWorker

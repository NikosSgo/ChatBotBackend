#!/bin/bash

echo "Run apply migrations.."
/app/.venv/bin/alembic upgrade head
echo "End apply migartions.."
exec /app/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

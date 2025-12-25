FROM python:3.11-slim AS base

WORKDIR /user_service

ENV PYTHONPATH=/user_service

COPY requirements.txt .

COPY --from=curlimages/curl:latest /usr/bin/curl /usr/bin/curl

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Wait for database to be fully ready, then retry logic with exponential backoff
CMD ["bash", "-c", "echo \"Waiting 5 seconds for database to be fully ready...\"; sleep 5; for i in {1..15}; do echo \"Attempt $i: Running migrations...\"; if alembic upgrade head; then echo \"Migrations successful!\"; break; else echo \"Migration failed, retrying in $((i*3)) seconds...\"; sleep $((i*3)); fi; done && granian --interface asgi --host 0.0.0.0 --port 8000 app.main:app"]

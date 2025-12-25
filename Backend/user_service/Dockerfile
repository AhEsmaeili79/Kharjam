FROM python:3.11-slim AS base

WORKDIR /user_service

ENV PYTHONPATH=/user_service

COPY requirements.txt .

COPY --from=curlimages/curl:latest /usr/bin/curl /usr/bin/curl

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "for i in {1..30}; do if alembic upgrade head 2>/dev/null; then echo \"Database migrations completed successfully\"; break; fi; echo \"Waiting for database... (attempt $i/30)\"; sleep 2; done && granian --interface asgi --host 0.0.0.0 --port 8000 app.main:app"]

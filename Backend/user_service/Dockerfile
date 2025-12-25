FROM python:3.11-slim AS base

WORKDIR /user_service

ENV PYTHONPATH=/user_service

COPY requirements.txt .

COPY --from=curlimages/curl:latest /usr/bin/curl /usr/bin/curl

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "alembic upgrade head && granian --interface asgi --host 0.0.0.0 --port 8000 app.main:app"]

# ─── build stage ───────────────────────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install -no‑cache-dir \
      -r requirements.txt \
      django>=5.2.0 uvicorn[standard]>=0.24.0 gunicorn>=21.0.0

# ─── runtime stage ─────────────────────────────────────────────────
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# copy installed deps from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages \
     /usr/local/lib/python3.11/site-packages

# copy your code
COPY . .

# static & migrations at runtime via entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
  && adduser --disabled-password --gecos '' appuser \
  && chown -R appuser /app

USER appuser
EXPOSE $PORT
ENTRYPOINT ["/entrypoint.sh"]

CMD exec gunicorn api.asgi:application \
      -k uvicorn.workers.UvicornWorker \
      --bind 0.0.0.0:$PORT \
      --workers 2 \
      --threads 4
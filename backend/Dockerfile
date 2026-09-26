# FROM python:3.11
# WORKDIR /app

# RUN python -m venv /opt/venv
# ENV PATH= "/opt/venv/bin:$PATH"

# # Install the application dependencies
# COPY requirements.txt ./
# RUN pip install --upgrade pip && pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# # --- final: slim runtime image, no compilers/build headers ---
# FROM python:3.12-slim

# # Runtime-only system deps: libpq for psycopg2 to talk to Postgres
# RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
#     && rm -rf /var/lib/apt/lists/*

# # Non-root user - containers shouldn't run as root
# RUN useradd --create-home --shell /bin/bash appuser
# WORKDIR /app

# COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# COPY app ./app
# COPY alembic ./alembic
# COPY alembic.ini .
# COPY scripts ./scripts

# RUN chown -R appuser:appuser /app
# USER appuser

# EXPOSE 8002

# # Setup an app user so the container doesn't run as the root
# RUN chown -R appuser:appuser /app
# USER appuser

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]



```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

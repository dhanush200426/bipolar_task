FROM python:3.12-slim

# Create a non-root user with a home directory
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Install Python dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application source
COPY . .

# Ensure appuser owns the application files
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Start-up: apply migrations, conditionally seed, then run uvicorn on $PORT (defaults to 8000 for local docker compose)
CMD ["sh", "-c", "alembic upgrade head && if [ \"$SEED_ON_START\" = 'true' ]; then python scripts/seed.py; fi && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

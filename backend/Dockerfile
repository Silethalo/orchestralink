# 1. Use a slim base image to reduce container size
FROM python:3.9-slim

# 2. Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disc
# PYTHONUNBUFFERED: Ensures logs are flushed immediately (vital for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies (if needed for psycopg2)
# We clean up apt lists afterwards to keep the image small.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. OPTIMIZATION: Install Python dependencies FIRST
# Docker caches layers. If requirements.txt hasn't changed, this step 
# is skipped, saving you minutes of build time during development.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
# This is done LAST so that code changes don't trigger a re-install of pip packages.
COPY . .

# 7. SECURITY: Create a non-root user
# Running as root is a security risk. We create a user 'appuser' and switch to it.
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# 8. Expose the port the app runs on
EXPOSE 8000

# 9. Define the entrypoint command
# We use uvicorn to run the FastAPI app.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
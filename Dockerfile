# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV FLASK_APP=app/app.py

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python3 -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . /app
COPY . /ml/models

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
RUN addgroup --system appgroup --gid 101 && adduser --uid 101 --system --no-create-home --ingroup appgroup appuser
RUN chown -R appuser:appgroup /app
RUN touch /app/app.log && chown appuser:appgroup /app/app.log
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
#  CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.app:app"]
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
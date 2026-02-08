FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set up working directory at project root
WORKDIR /app
COPY . /app

# Install the package and dependencies
RUN uv pip install --system -e .

# Run migrations and start server from sample_project
WORKDIR /app/sample_project
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

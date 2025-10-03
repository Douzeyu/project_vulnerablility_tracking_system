FROM python:3.13.7-alpine3.22 AS build

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

# Copy the application into the container
COPY . /app

# Install the application dependencies using uv
WORKDIR /app
RUN uv sync --frozen --no-cache

# add venv to search path
ENV PATH=/app/.venv/bin:$PATH

# Expose the port the app listens on
EXPOSE 8000

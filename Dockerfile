FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation for performance
ENV UV_COMPILE_BYTECODE=1

# Use copy mode for mounted volumes (dev best practice)
ENV UV_LINK_MODE=copy

# Install dependencies only (no project code yet, for better caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Now copy the rest of the project and install it
COPY . /app
# Persistent cache at /root/.cache/uv for builds.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# CMD ["fastapi", "dev", "--host", "0.0.0.0", "src.main:app"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8032"]

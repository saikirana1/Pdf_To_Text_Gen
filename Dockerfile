# 1. Base image
FROM python:3.12-slim

# 2. Environment variables
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

# 3. Set working directory
WORKDIR /app

# 4. Install curl and uv (modern Python package manager)
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    export PATH="/root/.local/bin:$PATH" && \
    uv --version && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. Ensure uv is always on PATH for next steps
ENV PATH="/root/.local/bin:$PATH"

# 6. Copy dependency files
COPY pyproject.toml uv.lock* requirements.txt* ./

# 7. Install dependencies (safe fallback logic)
RUN if [ -f uv.lock ]; then \
    uv sync --frozen; \
    elif [ -f pyproject.toml ]; then \
    uv pip install .; \
    elif [ -f requirements.txt ]; then \
    uv pip install -r requirements.txt; \
    fi

# 8. Copy the rest of the project
COPY . .

# 9. Expose FastAPI port
EXPOSE 8000

# 10. Run with uvicorn through uv
CMD ["uv", "run", "uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]

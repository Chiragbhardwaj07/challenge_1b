FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install packages with platform specification
RUN pip install --no-cache-dir --only-binary=all -r requirements.txt \
    && pip cache purge

# Remove build tools
RUN apt-get remove -y gcc g++ && apt-get autoremove -y

# Copy project files
COPY . .

# Environment variables
ENV HF_HUB_OFFLINE=1
ENV FLASHRANK_CACHE_DIR=/app/models/flashrank
ENV PYTHONPATH=/app/src:/app
ENV PYTHONDONTWRITEBYTECODE=1

# Create output directory
RUN mkdir -p /app/output

CMD ["python", "src/main.py"]

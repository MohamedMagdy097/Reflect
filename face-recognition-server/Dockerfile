# Use Python slim image (not alpine - TensorFlow has issues with musl)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create uploads directory
RUN mkdir -p uploads

# Create deepface cache directory (will be mounted as volume)
# DeepFace uses DEEPFACE_HOME env var, or falls back to ~/.deepface
RUN mkdir -p /app/.deepface/weights

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///./database.db
ENV UPLOAD_DIR=uploads
ENV SIMILARITY_THRESHOLD=0.55
# Set explicit DeepFace cache location (easier to mount as volume)
ENV DEEPFACE_HOME=/app/.deepface

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

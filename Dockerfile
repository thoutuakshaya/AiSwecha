FROM python:3.10-slim

# Install ffmpeg (includes ffprobe), audio & system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg portaudio19-dev build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.enableCORS=false"]

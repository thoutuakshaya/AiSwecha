FROM python:3.10-slim

# Install PyAudio system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        portaudio19-dev ffmpeg build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run the app
CMD ["streamlit", "run", "app.py"]

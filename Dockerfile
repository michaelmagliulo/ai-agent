FROM python:3.13-slim

WORKDIR /app

# Install dependencies separately so Docker can cache this layer.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the project into the image.
COPY src/ ./src/

CMD ["python", "src/agent_with_narrative.py"]
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# gRPC server port. The platform's HTTP-oriented port inference may not suit a
# pure gRPC (HTTP/2-only) server — that is part of what this test probes.
EXPOSE 50051
CMD ["python", "server.py"]

FROM python:3.11-slim
RUN apt-get update && apt-get install -y clamav clamav-daemon && rm -rf /var/lib/apt/lists/*
RUN pip install flask
COPY clamav_api.py /app/clamav_api.py
WORKDIR /app
CMD ["sh", "-c", "freshclam ; clamd ; python3 clamav_api.py"]
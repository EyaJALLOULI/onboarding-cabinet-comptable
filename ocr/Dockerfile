FROM python:3.11-slim
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-fra poppler-utils && rm -rf /var/lib/apt/lists/*
RUN pip install flask pytesseract pdf2image Pillow requests
COPY ocr_server.py /app/ocr_server.py
WORKDIR /app
CMD ["python3", "ocr_server.py"]
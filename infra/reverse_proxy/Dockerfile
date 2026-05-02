FROM python:3.11-slim

WORKDIR /app

COPY proxy.py .
COPY aes ./aes

RUN chmod +x ./aes

CMD ["python", "proxy.py"]
FROM python:3.11

RUN apt-get update && \
    apt-get install -y default-mysql-client

WORKDIR /app/bot


COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
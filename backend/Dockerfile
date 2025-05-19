FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

RUN chmod +x ./docker/entrypoint.sh

ENTRYPOINT ["./docker/entrypoint.sh"]

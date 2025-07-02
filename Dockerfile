FROM python:3.13-alpine

WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache build-base libffi-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

COPY *.py /app/

EXPOSE 80

CMD ["gunicorn", "--conf", "gunicorn_conf.py",  "main:app"]
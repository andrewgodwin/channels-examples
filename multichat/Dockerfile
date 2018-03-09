FROM python:3.6-stretch
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN python manage.py migrate


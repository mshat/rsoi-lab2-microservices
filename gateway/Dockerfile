# Dockerfile содержит список инструкций для образа
# Image: список инструкций для всех программных пакетов в ваших проектах
# Container: экземпляр образа во время выполнения

# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/reservation

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD python3 manage.py runserver  0.0.0.0:$PORT
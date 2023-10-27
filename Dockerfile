# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/my_blog

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/my_blog/entrypoint.sh
RUN chmod +x /usr/src/my_blog/entrypoint.sh

# copy project
COPY . .
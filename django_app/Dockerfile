FROM python:3.6

# setup working directory:
WORKDIR /code

RUN apt-get update

# copy project:
COPY ./django_app/ /code/django_app
COPY ./environment/requirements.txt ./

# install dependencies:
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

WORKDIR /code/django_app

EXPOSE 8000
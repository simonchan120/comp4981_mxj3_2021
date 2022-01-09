#FROM python:3.8-alpine
#RUN apk add g++

FROM ubuntu:20.04

RUN apt-get -y update && apt-get -y install python3-pip
RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-dependencies -r requirements.txt
#RUN pip install rasa~=3.0.0
#RUN pip install --upgrade pymongo~=3.12.0
COPY ["/models","/models"]
COPY ["config.yml","config.yml"]

EXPOSE 5005

ENTRYPOINT ["python3","-m","rasa"]

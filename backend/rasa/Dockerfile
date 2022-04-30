#FROM python:3.8-alpine
#RUN apk add g++

FROM ubuntu:20.04

RUN apt-get -y update && apt-get -y install python3-pip
RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-dependencies -r requirements.txt
#RUN pip install rasa~=3.0.0
#RUN pip install --upgrade pymongo~=3.12.0
# COPY ["config.yml","config.yml"]
# COPY ["endpoints.yml","endpoints.yml"]
COPY ["/models","/models"]
COPY ["init.py","config.yml","endpoints.yml","/"]
COPY start.sh /
EXPOSE 5005

CMD ["/start.sh"]

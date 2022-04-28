# Set base image (host OS)
FROM ubuntu:20.04

RUN apt-get -y update && apt-get -y install python3-pip
RUN pip install --upgrade pip

COPY requirements.txt backend/requirements.txt
RUN pip install -r /backend/requirements.txt

#nltk data
RUN python3 -m nltk.downloader vader_lexicon

ENV FLASK_APP=backend
ENV PYTHOHUNBUFFERED=1
ENV PROPAGATE_EXCEPTIONS=1
RUN rm -rf backend

COPY ["data/dialogue.py","data/dataclass.py","/backend/data/"]
COPY ["models","/backend/models/"]
COPY ["__init__.py","requirements.txt","rasa.py","recommender.py","server.py","giphyUtil.py","/backend/"]
COPY ["a","celery_config","/backend/celery_config/"]
EXPOSE 8000

CMD ["gunicorn","--preload","--workers=3","--threads","2","-b","0.0.0.0:8000","backend:app","--timeout","30"]
#CMD ["flask","run","--host=0.0.0.0","--port=8000"]

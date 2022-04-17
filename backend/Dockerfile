# Set base image (host OS)
FROM python:3.8-alpine

COPY requirements.txt backend/requirements.txt

RUN pip install -r /backend/requirements.txt

ENV FLASK_APP=backend
ENV PYTHOHUNBUFFERED=1
ENV PROPAGATE_EXCEPTIONS=1
COPY ["data/dialogue.py","data/dataclass.py","/backend/data/"]
COPY ["__init__.py","requirements.txt","rasa.py","recommender.py","server.py","config.json","giphyUtil.py","/backend/"]
COPY ["celery_config","/backend/celery_config"]
EXPOSE 8000

#CMD ["gunicorn","--workers=3","-b","0.0.0.0:8000","backend:app"]
CMD ["flask","run","--host=0.0.0.0","--port=8000"]

# Set base image (host OS)
FROM python:3.8-alpine

COPY ["/backend/data","/backend/data"]
COPY ["/backend/__init__.py","/backend/requirements.txt","/backend/dataclass.py","/backend/rasa.py","/backend/recommender.py","/backend/server.py","/backend/config.json","/backend/giphyUtil.py","/backend/"]
COPY ["/backend/celery_config","/backend/celery_config"]
COPY backend/requirements.txt .

RUN pip install -r /backend/requirements.txt

ENV FLASK_APP=backend
ENV PYTHOHUNBUFFERED=1
ENV PROPAGATE_EXCEPTIONS=1
EXPOSE 8000

CMD ["gunicorn","--workers=3","-b","0.0.0.0:8000","backend:app"]

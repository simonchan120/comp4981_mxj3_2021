# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container


# Copy the dependencies file to the working directory
COPY ["/backend/data","/backend/data"]
COPY ["/backend/__init__.py","/backend/requirements.txt","/backend/dataclass.py","/backend/rasa.py","/backend/recommender.py","/backend/server.py","/backend/config.json","/backend/"]
COPY ["/backend/celery_config","/backend/celery_config"]
COPY backend/requirements.txt .
# Install any dependencies

#COPY backend backend
RUN pip install -r /backend/requirements.txt


ENV FLASK_APP=backend
#EXPOSE 5000
# Specify the command to run on container start
#CMD ["python","-c","import backend"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
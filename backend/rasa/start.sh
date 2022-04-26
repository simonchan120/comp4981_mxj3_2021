#!/bin/bash

/usr/bin/python3 init.py
/usr/bin/python3 -m rasa run -p 5005 -m /models --enable-api --cors * --endpoints endpoints.yml

#CMD ["python3","-m","rasa","run","-p","5005","-m","/models","--enable-api","--cors","*","--endpoints","endpoints.yml"]

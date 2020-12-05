FROM ubuntu:latest
MAINTAINER "chano22@naver.com"
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential
COPY . /chatserver
WORKDIR /chatserver
RUN pip3 install -r requirements.txt
CMD ["gunicorn","-k","geventwebsocket.gunicorn.workers.GeventWebSocketWorker","-w","4","-b","0.0.0.0:8000","chatserver"]
# TravlePlaneAssignment
Assignment for TravlePlane

install and excute guide

1. pythonInstall 폴도의 exe를 설치

2. 	pip install --upgrade pip
	pip install gevent
	pip install gevent-websocket
	pip install gunicorn
	pip install redis

3. vscode extention 에서 python 검색후 위에서 3개 설치하기

핵심 작업 : 
1.Redis Queue에 연결하기위한 파이썬 테스트코드 구현
2.Redis Queue pubsub 테스트코드 및 기능 구현
3.localhost:8000/chat 에 메세지 보내는 테스트코드구현, 즉 websocket client
3-1. 3초마다 메시지를 보내는 for 반복문 클라이언트를 구현하는것임.
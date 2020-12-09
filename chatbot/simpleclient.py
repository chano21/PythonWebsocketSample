import websocket
from multiprocessing import Process
from websocket import create_connection
import os
import time

#간단하게 만든 웹소켓 클라이언트 전용 함수
def newwebsocket():
    ws = create_connection("ws://localhost:8000/chat")
    while(True):
            time.sleep(3)
            text ='{"message":"'+str(os.getpid())+'"}'
            ws.send(text)
            result =  ws.recv()
            print("Received '%s'" % result)
        
if __name__ == "__main__":
    websocket.enableTrace(True)
    clientsize = 4 #클라이언트 사이즈 설정
    
    procs = []
    for i in range(clientsize):
        proc = Process(target=newwebsocket)
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
      
                    
  
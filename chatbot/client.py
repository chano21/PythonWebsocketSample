import websocket
from multiprocessing import Process
import time
import os
import gevent.pool

pool=gevent.pool.Pool(10)
def on_message(ws, message):
     print("Received '%s'" % message)
     #이 메서드가 발동이안되는데.. sender에서 비동기가 원만하게 해결이안된점, 아쉽게생각하고있습니다.    
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("client closed")

def on_open(ws):
    print('client open')
    pool.spawn(sender,ws)
    pool.join()

def sender(ws):
    while(True):
        time.sleep(3)
        text ='{"message":"'+str(os.getpid())+'"}'
        ws.send(text)
        
if __name__ == "__main__":
    websocket.enableTrace(True)
    #클라이언트 사이즈
    clientsize = 4

    procs = []

    ws = websocket.WebSocketApp("ws://localhost:8000/chat",
                              on_error = on_error,
                              on_close = on_close)
    ws.on_message = on_message
    ws.on_open = on_open
  
    for i in range(clientsize):
        proc = Process(target=ws.run_forever)
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
            
                    
  
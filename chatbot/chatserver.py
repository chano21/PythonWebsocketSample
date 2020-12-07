import json
import uuid
import configparser
import redis
import gevent.pool
import time
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.resource import Resource, WebSocketApplication

pool = gevent.pool.Pool(1000)

publishs=[]    


class RedisConnector():
    
    def __init__(self):
        self.sockets = {}
        self.redisconfig='REDIS_SERVER'
        self.filedir='configs/redis_config.ini'
    def redisConnection(self):
        config = configparser.ConfigParser()
        config.read(self.filedir)
        print(self.redisconfig)
        password = config[self.redisconfig]['REQUIREPASS']
        host = config[self.redisconfig]['HOST']
        port = config[self.redisconfig]['PORT']
      
        r = redis.StrictRedis(host=host,port=port, db=0, encoding='utf-8',decode_responses=True)
        return r

redistool = RedisConnector()

class Broker():
    def __init__(self):
        self.r=redistool.redisConnection().pubsub()
        self.sockets = {}

    def subscribe(self, key, socket):
        if key not in self.sockets:
            self.sockets[key] = set()
        
        if socket in self.sockets[key]:
            return
        self.r.subscribe(key)
        self.sockets[key].add(socket)
    
    def publish(self, key,data):
        r=self.r
        message = 0
        while(True):
            rd=r.get_message()
            if(str(rd)=='None'):
                continue
            map= dict(rd)
            message = map.get('data')
            if (message!=1):
                break
       
        
         
        for socket in self.sockets[key]:
            publishs.append(pool.spawn(socket.on_broadcast(message)))
        gevent.joinall(publishs)
  
            
        
    def unsubscribe(self, key, socket):
        if key not in self.sockets: return

        self.sockets[key].remove(socket)

broker = Broker()


class Chat(WebSocketApplication):
    
    def on_open(self, *args, **kwargs):
        start = time.time()
        self.userid = uuid.uuid4()
        broker.subscribe('room1', self)
        print('on_open ' +str(time.time() - start))

    def on_close(self, *args, **kwargs):
        start = time.time()
        broker.unsubscribe('room1', self)
        print('on_close ' +str(time.time() - start))

    def on_message(self, message, *args, **kwargs):
        start = time.time()
        if not message: return

        data = json.loads(message)
        data['user'] = self.userid.hex
        serial=json.dumps(data, ensure_ascii=False).encode('utf-8')

        redistool.redisConnection().publish('room1',serial)
        broker.publish('room1', data)

        print('on_message ' +str(time.time() - start))
        
    def on_broadcast(self, data):
        start = time.time()
        print('dump before ' +str(time.time() - start))
        start = time.time()
        self.ws.send(str(data))
        print('dump after ' +str(time.time() - start))
       

def index(environ, start_response):
    start_response('200 OK', [('Content-type','text/html')])
    htmgl = open('index.html', 'rb').read()
    return [htmgl]


application = Resource([
    ('^/chat', Chat),
    ('^/', index)
])


if __name__ == '__main__':
    WSGIServer('{}:{}'.format('0.0.0.0', 8000), application, handler_class=WebSocketHandler).serve_forever()
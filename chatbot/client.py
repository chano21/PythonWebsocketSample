import gevent
from gevent import monkey
monkey.patch_all()

from websocket import create_connection
ws = create_connection("ws://echo.websocket.org")

pool = gevent.pool.Pool(1000)

publishs=[]    

class RedisConnector():
    
    def __init__(self):
        self.sockets = {}
        self.redisconfig='REDIS_SERVER'
        self.filedir='../configs/redis_config.ini'
    def redisConnection(self):
        config = configparser.ConfigParser()
        config.read(self.filedir)
        password = config[self.redisconfig]['REQUIREPASS']
        host = config[self.redisconfig]['HOST']
        port = config[self.redisconfig]['PORT']
        r = redis.StrictRedis(host=host,port=port, db=0, encoding='utf-8',decode_responses=True)
        self.pubsub=r.pubsub()
        self.rc=r

#redistool = RedisConnector()

class GeventPool():
    pass

class MemoryBroker():
    def __init__(self):
        self.sockets = {}

    def subscribe(self, key, socket):
        if key not in self.sockets:
            self.sockets[key] = set()
        
        if socket in self.sockets[key]:
            return

        self.sockets[key].add(socket)
    
    def publish(self, key, data):
        for socket in self.sockets[key]:
 #           redistool.rc.publish(key,data)
 #           messages=redistool.pubsub.get_message()
 #           data = messages['data'];
            socket.on_broadcast(data)
            publishs.append(pool.spawn(socket.on_broadcast(data)))
        gevent.joinall(publishs)
  
            
        
    def unsubscribe(self, key, socket):
        if key not in self.sockets: return

        self.sockets[key].remove(socket)


# class MemoryBroker():
#     def __init__(self):
#         self.sockets = {}

#     def subscribe(self, key, socket):
#         if key not in self.sockets:
#             self.sockets[key] = set()

#         if socket in self.sockets[key]:
#             return

#         self.sockets[key].add(socket)

#     def publish(self, key, data):
#         for socket in self.sockets[key]:
#             socket.on_broadcast(data)

#     def unsubscribe(self, key, socket):
#         if key not in self.sockets: return

#         self.sockets[key].remove(socket)


broker = MemoryBroker()


class Chat(WebSocketApplication):
    
    def on_open(self, *args, **kwargs):
        start = time.time()
        self.userid = uuid.uuid4()
        broker.subscribe('room1', self)
  #      redistool.pubsub.subscribe(self.roomkey)
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
        
        broker.publish('room1', data)
        print('on_message ' +str(time.time() - start))
        
    def on_broadcast(self, data):
        start = time.time()
        message=json.dumps(data)
        print('dump before ' +str(time.time() - start))
        start = time.time()
        self.ws.send(message)
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
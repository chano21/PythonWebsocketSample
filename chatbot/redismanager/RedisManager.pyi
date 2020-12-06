import configparser
import redis
redisconfig='REDIS_SERVER'
filedir = '../configs/redis_config.ini'


class RedisConnector():
    def __init__(self):
        self.sockets = {}

    def redisConnection():
        config = configparser.ConfigParser()
        config.read(filedir)
        password = config[redisconfig]['REQUIREPASS']
        host = config[redisconfig]['HOST']
        port = config[redisconfig]['PORT']
        r = redis.StrictRedis(host=host,port=port, db=0, encoding='utf-8',decode_responses=True)

    def subscribe(self, key, socket):
        if key not in self.sockets:
            self.sockets[key] = set()

        if socket in self.sockets[key]:
            return

        self.sockets[key].add(socket)

    def publish(self, key, data):
        for socket in self.sockets[key]:
            socket.on_broadcast(data)

    def unsubscribe(self, key, socket):
        if key not in self.sockets: return

        self.sockets[key].remove(socket)

    
    
        # ps = r.pubsub()
        # ps.subscribe('room1')
        # r.publish('room1',"hello world")
        # ps.get_message()
        # messages=ps.get_message()
        # ps.get_message()
        # data = messages['data'];
        # print(data) 
        # print(data) 

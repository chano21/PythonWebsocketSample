import unittest
import configparser
import redis
redisconfig='REDIS_SERVER'
filedir = '../configs/redis_config.ini'

class RedisPubSubTest(unittest.TestCase):
  
    def testRedisClient(self):
        config = configparser.ConfigParser()
        config.read(filedir)
        host = config[redisconfig]['HOST']
        port = config[redisconfig]['PORT']
        r = redis.StrictRedis(host=host,port=port, db=0, encoding='utf-8',decode_responses=True)
        ps = r.pubsub()
        ps.subscribe('room1')
        r.publish('room1',"hello world1")
        r.publish('room1',"hello world2")
        r.publish('room1',"hello world3")
        while(ps.get_message()==1):
            pass
        messages=ps.get_message()
        print(messages)
        messages=ps.get_message()
        print(messages)
        
        data = messages['data'];
        print(data) 
if __name__ == '__main__':
    unittest.main()
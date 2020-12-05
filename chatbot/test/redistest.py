import unittest
import configparser
import redis
import time
redisconfig='REDIS_SERVER'
filedir = '../configs/redis_config.ini'

class RedisPubSubTest(unittest.TestCase):
  
    def testRedisClient(self):
        config = configparser.ConfigParser()
        config.read(filedir)
        password = config[redisconfig]['REQUIREPASS']
        host = config[redisconfig]['HOST']
        port = config[redisconfig]['PORT']
        r = redis.StrictRedis(host=host,port=port, db=0, encoding='utf-8',decode_responses=True)
        ps = r.pubsub()
        ps.subscribe('room1')
        r.publish('room1',"hello world")
        ps.get_message()
        messages=ps.get_message()
        ps.get_message()
        data = messages['data'];
        print(data) 
        print(data) 

if __name__ == '__main__':
    unittest.main()
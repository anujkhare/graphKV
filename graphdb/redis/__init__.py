import redis


class RedisBaseConnection():
    '''Defines a wrapper around Redis to support the particular operations of a
       graph like database.
       It does Not type check or know about the schema, those operations need
       to be handled by a separate layer.
       The idea is to encapsulate required database API so that we can change
       the underlying database in the future if required.
       Requires the address of the redis server.
    '''
    redis_args = {
                  'host': 'localhost',
                  'port': 6379,
                  'db': 0,
                  'charset': 'utf-8',
                  'decode_responses': True
                 }

    def __init__(self, **kwargs):
        '''Constructor takes the arguments for the redis instance connection
        '''
        self.connect_db(**kwargs)

    def connect_db(self, **kwargs):
        self.redis_conn = redis.StrictRedis(**kwargs)
        self.redis_args.update(kwargs)

    def _test_connection(self):
        try:
            self.redis_conn.ping()
        except(redis.exceptions.ConnectionError):
            print("UNABLE TO CONNECT TO THE SERVER")
            raise
        except:
            print("SOME RANDOM ERROR")
            raise

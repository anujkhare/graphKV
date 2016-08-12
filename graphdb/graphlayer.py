# This link: https://www.youtube.com/watch?v=EiOglTERPEo gives a very good idea
# about how to do dependency injection by multiple inheritance and mixins!
# So we'll have a (kind of pythonic) abstract class for the GraphDB with all
# required methods as "not implemented", which our code in the other component
# will inherit. To actually make this useful though, you need to have a specifi
# database linked implementation like GraphRedis, and create a new class which
import redis


class GraphLayer():
    def connect_db(self, **kwargs):
        raise NotImplementedError

    def set_attributes(self, source, attr, *values):
        ''' Set one attribute to a list of strings.
            Internally, the attributes are stored as sets, with keys
            "source:attr".
            Example: set_attributes('foo', 'skills', 'skill1', 'skill2')
        '''
        raise NotImplementedError

    def set_multiple_edges(self, **kwargs):
        '''Set variable list of edges, which are a dict containing {source,
           attr, dest}. Any invalid edges are ignored with a warning.
        '''
        raise NotImplementedError

    def save(self):
        '''Save the database on persistent storage. This is useful for the
           Redis backend.
        '''
        raise NotImplementedError


class GraphLayerRedis(GraphLayer):
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

    def set_attributes(self, source, attr, *values):
        ''' Set one attribute to a list of strings.
            Internally, the attributes are stored as sets, with keys
            "source:attr".
            Example: set_attributes('foo', 'skills', 'skill1', 'skill2')
        '''
        self._test_connection()
        key = source + ':' + attr
        self.redis_conn.sadd(key, *values)

    def set_multiple_edges(self, **kwargs):
        ''' For each source, provide a dict of attributes to be set. Attribute
            values must be a list.
            Ex: set_multiple_edges('rj': {'a':'2', 'w':'1'}, 'bob': {'a': '1'})
        '''
        self._test_connection()
        pipe = self.redis_conn.pipeline()
        for source, attr_dict in kwargs.items():
            for attr, values in attr_dict.items():
                key = source + ':' + attr
                pipe.sadd(key, *values)
                # print(key)
                # print(*values)
        pipe.execute()

    def save(self):
        '''Save the database on persistent storage. This is useful for the
           Redis backend.
        '''
        self._test_connection()
        self.redis_conn.save()

    def get_by_name(self, name):
        rval = self.redis_conn.hgetall(name)
        return rval

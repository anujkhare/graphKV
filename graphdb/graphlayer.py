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

    def set_edge(self, source, attr, dest):
        '''Set one edge. Each argument must be a string.
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
    redis_args = {'host': 'localhost', 'port': 6379, 'db': 0}

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

    def set_edge(self, source, attr, value):
        '''Set one edge. Each argument must be a string.
        '''
        self._test_connection()
        r = self.redis_conn

        print(r.ping())
        r.hset(source, attr, value)

    def set_multiple_edges(self, **kwargs):
        '''For each source, provide a dict of attributes to be set.
           Ex: set_multiple_edges('raj': {'a':'2', 'w':'1'}, 'bob': {'a': '1'})
        '''
        self._test_connection()
        pipe = self.redis_conn.pipeline()
        for key, value in kwargs.items():
            pipe.hmset(key, value)
        pipe.execute()

    def save(self):
        '''Save the database on persistent storage. This is useful for the
           Redis backend.
        '''
        self._test_connection()
        self.redis_conn.save()


if __name__ == '__main__':
    gr = GraphLayerRedis()
    gr.set_edge('anuj', 'age', '22')
    gr.set_edge('anuj', 'height', '182')
    gr.set_edge('raj', 'age', '22')

    l = {'anuj': {'age': '11', 'w': '12'}, 'babe': {'age': '33', 'w': '3'}}
    gr.set_multiple_edges(**l)
    gr.save()

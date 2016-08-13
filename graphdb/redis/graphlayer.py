from graphdb.core.graphlayer import GraphLayer
from graphdb.redis import RedisBaseConnection


class GraphLayerRedis(GraphLayer, RedisBaseConnection):
    def __init__(self):
        super().__init__()

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
            values must be a list or a set.
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

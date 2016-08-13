from graphdb.core.query import GraphQuery
from graphdb.redis import RedisBaseConnection


class GraphQueryRedis(RedisBaseConnection, GraphQuery):
    ''' NOTE: The key "query:<i>" is changed in this method. If the same redis
        instance is shared for other databases, be forewarned!
    '''
    _counter = 0
    _cur_entity_type = None

    def __init__(self, **kwargs):
        self.__class__._counter += 1
        self.query_key = 'query:' + str(self.__class__._counter)
        super().__init__(**kwargs)

    def by_xid(self, xid):
        ''' gets the entry by xid and stores in the memory
        '''
        self._test_connection()
        r = self.redis_conn
        r.delete(self.query_key)
        r.sadd(self.query_key, xid)

    def get_attr(self, attr):
        ''' Gets the attr of the current results and stores in the memory.
            NOTE: the attr must be a valid attr for the type of the results.
        '''
        # FIXME: Embarassingly serial!! Try to parallelize?
        self._test_connection()
        r = self.redis_conn
        query_key = self.query_key

        cur_keys = r.smembers(query_key)
        r.delete(query_key)
        for key in cur_keys:
            attr_key = key.decode('ascii') + ':' + attr
            # print(attr_key)
            r.sunionstore(query_key, query_key, attr_key)
            # print(r.smembers(query_key))

    def fetch(self):
        ''' Returns the list of xids in the results.
        '''
        self._test_connection()
        return self.redis_conn.smembers(self.query_key)

    def fetch_with_attributes(self):
        ''' Returns the entire list results along with all their attributes.
            This is NOT possible without the schema, because of the way the
            values are stored.
        '''
        raise(NotImplementedError)

    def intersection(self, *queries):
        ''' Takes the intersection of the results stored in each of the queries
            and stores it in it's memory.
            Each query must have the same type of result as this instance.
        '''
        self._test_connection()
        r = self.redis_conn
        query_key = self.query_key
        for ext_query in queries:
            r.sinterstore(query_key, query_key, ext_query.query_key)

    def union(self, *queries):
        self._test_connection()
        r = self.redis_conn
        query_key = self.query_key
        for ext_query in queries:
            r.sunionstore(query_key, query_key, ext_query.query_key)

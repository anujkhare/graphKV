from graphdb.core.query import GraphQuery
from graphdb.redis import RedisBaseConnection


class GraphQueryRedis(RedisBaseConnection, GraphQuery):
    ''' NOTE: The key "query:<i>" is changed in this method. If the same redis
        instance is shared for other databases, be forewarned!
    '''
    _counter = 0
    _cur_entity_type = None

    def __init__(self, *values, **kwargs):
        ' values: The initial strings to populate the results '
        self.__class__._counter += 1
        self.query_key = 'query:' + str(self.__class__._counter)
        super().__init__(**kwargs)
        self.clear()
        self.add_values(*values)

    # @classmethod
    # def init_with_values(cls, *values, **kwargs):
    #     instance = cls(**kwargs)
    #     instance.add_values(*values)
    #     return instance

    def add_values(self, *values):
        ''' adds the given values to the results set.
        '''
        if len(values) == 0:
            return 0
        self._test_connection()
        r = self.redis_conn
        r.sadd(self.query_key, *values)
        # return r.scard(self.query_key)
        return self

    def at_uids(self, *uids):
        ''' Stores the values at the given uids into the results set.
        '''
        if len(uids) != 0:
            self._test_connection()
            r = self.redis_conn
            for uid in uids:
                r.sunionstore(self.query_key, self.query_key, uid)
            # return r.scard(self.query_key)
        return self

    def get_attr(self, attr):
        ''' Gets the attr of the current results and stores in the memory.
            NOTE: the attr must be a valid attr for the type of the results.
        '''
        self._test_connection()
        r = self.redis_conn
        query_key = self.query_key

        cur_keys = r.smembers(query_key)
        r.delete(query_key)
        for key in cur_keys:
            attr_key = key.decode('ascii') + ':' + attr
            r.sunionstore(query_key, query_key, attr_key)
        # return r.scard(self.query_key)
        return self

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
            if r.scard(ext_query.query_key) == 0:
                r.delete(self.query_key)
            r.sinterstore(query_key, query_key, ext_query.query_key)
        # return r.scard(self.query_key)
        return self

    def union(self, *queries):
        self._test_connection()
        r = self.redis_conn
        query_key = self.query_key
        for ext_query in queries:
            r.sunionstore(query_key, query_key, ext_query.query_key)
        # return r.scard(self.query_key)
        return self

    def clear(self):
        self.redis_conn.delete(self.query_key)
        return self

    def filter_by_func(self, filter_func):
        ''' filter_func must take one uid, and return a True, indicating the
            entity is to be accepted, or False indicating the entity is to be
            discarded.
        '''
        self._test_connection()
        r = self.redis_conn

        cur_keys = r.smembers(self.query_key)
        to_remove = [key for key in cur_keys if not
                     filter_func(GraphQueryRedis(key))]

        r.srem(self.query_key, *to_remove)
        return self

import fakeredis
from graphdb.redis.graphlayer import GraphLayerRedis
from graphdb.redis.query import GraphQueryRedis


# For GraphLayerRedis MOCK using fakeredis
# NOTE: FakeRedis does not decode responses like Redis!
class MockGraphLayerRedis(GraphLayerRedis):
    def connect_db(self, **kwargs):
        self.redis_conn = fakeredis.FakeStrictRedis()
        self.redis_args.update(kwargs)


class MockGraphQueryRedis(GraphQueryRedis):
    def connect_db(self, **kwargs):
        self.redis_conn = fakeredis.FakeStrictRedis()
        self.redis_args.update(kwargs)

__all__ = ['fakeredis', 'MockGraphLayerRedis', 'GraphLayerRedis',
           'GraphQueryRedis']

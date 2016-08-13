import fakeredis
from graphdb.redis.graphlayer import GraphLayerRedis
from graphdb.redis.query import GraphQueryRedis


# For GraphLayerRedis MOCK using fakeredis
# NOTE: FakeRedis does not decode responses like Redis!
class FakeRedisConnect():
    def connect_db(self, **kwargs):
        self.redis_conn = fakeredis.FakeStrictRedis()
        self.redis_args.update(kwargs)


class MockGraphLayerRedis(FakeRedisConnect, GraphLayerRedis):
    pass


class MockGraphQueryRedis(FakeRedisConnect, GraphQueryRedis):
    pass

__all__ = ['fakeredis', 'MockGraphLayerRedis', 'MockGraphQueryRedis']

import fakeredis
import graphdb.graphlayer as graphlayer


# For GraphLayerRedis MOCK using fakeredis
# NOTE: FakeRedis does not decode responses like Redis!
class MockGraphLayerRedis(graphlayer.GraphLayerRedis):
    def connect_db(self, **kwargs):
        self.redis_conn = fakeredis.FakeStrictRedis()
        self.redis_args.update(kwargs)

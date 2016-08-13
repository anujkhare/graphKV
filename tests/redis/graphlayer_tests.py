from tests.redis import fakeredis, MockGraphLayerRedis


class TestGraphLayerRedis():
    def setUp(self):
        self.r = fakeredis.FakeStrictRedis()
        self.gr = MockGraphLayerRedis()

    def tearDown(self):
        self.r.flushall()

    def test_graphlayer_redis_set_edge(self):
        values = [b'skill1', b'skill2']
        self.gr.set_attributes('foo', 'skills', *values)

        val = self.r.smembers('foo:skills')
        assert val == set(values)

    def test_graphlayer_redis_set_multiple_edges(self):
        foo_a = set([b'1', b'2', b'3'])
        foo_b = set([b'5'])
        bar_a = set([b'11', b'22'])
        l = {
            'foo': {'a': foo_a, 'b': foo_b},
            'bar': {'a': bar_a}
            }
        self.gr.set_multiple_edges(**l)

        r_foo_a = self.r.smembers('foo:a')
        r_foo_b = self.r.smembers('foo:b')
        r_bar_a = self.r.smembers('bar:a')
        assert foo_a == r_foo_a
        assert foo_b == r_foo_b
        assert bar_a == r_bar_a

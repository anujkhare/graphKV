from tests.redis import fakeredis, MockGraphLayerRedis


class TestGraphLayerRedis():
    def setUp(self):
        self.r = fakeredis.FakeStrictRedis()
        self.gr = MockGraphLayerRedis()

    def tearDown(self):
        self.r.flushall()

    def test_graphlayer_redis_set_attributes(self):
        values = [b'skill1', b'skill2']
        self.gr.set_attributes('foo', 'skills', *values)

        val = self.r.smembers('foo:skills')
        assert val == set(values)

    # Attributes can be single str, lists or dicts!
    def test_graphlayer_redis_set_multiple_edges(self):
        foo_a = set([b'1', b'2', b'3'])
        foo_b = '11'
        bar_a = [b'11', b'22']
        l = {
            'foo': {'a': foo_a, 'b': foo_b},
            'bar': {'a': bar_a}
            }
        self.gr.set_multiple_edges(**l)

        r_foo_a = self.r.smembers('foo:a')
        r_foo_b = self.r.smembers('foo:b')
        r_bar_a = self.r.smembers('bar:a')
        assert foo_a == r_foo_a
        assert set(bar_a) == r_bar_a
        assert set([foo_b.encode()]) == r_foo_b

    # since internally we store sets, no duplicate values should arise.
    def test_graphlayer_redis_set_multiple_edges_duplicate_add(self):
        foo_a = set([b'1', b'2', b'3'])
        foo_b = '11'
        bar_a = [b'11', b'22']
        l = {
            'foo': {'a': foo_a, 'b': foo_b},
            'bar': {'a': bar_a}
            }
        self.gr.set_multiple_edges(**l)
        self.gr.set_multiple_edges(**l)

        r_foo_a = self.r.smembers('foo:a')
        r_foo_b = self.r.smembers('foo:b')
        r_bar_a = self.r.smembers('bar:a')
        assert foo_a == r_foo_a
        assert set(bar_a) == r_bar_a
        assert set([foo_b.encode()]) == r_foo_b

    def test_graphlayer_redis_set_multiple_edges_multiple_add(self):
        l1 = {'foo': {'a': ['1', '2']}}
        l2 = {'foo': {'a': [b'3', b'2']}}
        self.gr.set_multiple_edges(**l1)
        self.gr.set_multiple_edges(**l2)

        r_foo_a = self.r.smembers('foo:a')
        assert set([b'1', b'2', b'3']) == r_foo_a

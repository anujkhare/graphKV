from tests.redis import fakeredis, MockGraphQueryRedis, MockGraphLayerRedis


def setup_module():
    ''' Adds a basic mock database to the module level fakeredis instance.
    '''
    people_list = ['person:foo', 'person:bar', 'person:baz']
    company_list = ['company:a', 'company:b', 'company:c']
    mock_data = {
                 'person:foo': {
                                 'name': 'foo',
                                 'cur_company': 'company:a',
                                 'past_company': ['company:b', 'company:c']
                               },
                 'company:b': {
                                'name': 'b',
                                'employees': ['person:baz'],
                                'past_employees': ['person:bar', 'person:foo']
                              },
                 'people': {'list': people_list},
                 'companies': {'list': company_list}
                }

    MockGraphLayerRedis().set_multiple_edges(**mock_data)


# NOTE: fakeredis used in MockGraphQueryRedis does NOT support decoding
# strings. Hence, results are binary strings. Decoding is done in redis.
class TestGraphQueryRedis():
    def setUp(self):
        MockGraphQueryRedis._counter = 0
        self.r = fakeredis.FakeStrictRedis()
        self.gr = MockGraphQueryRedis()
        self.r.delete('query:1')
        self.r.delete('query:2')

    def tearDown(self):
        pass

    def test_graph_query_redis_counter(self):
        MockGraphQueryRedis._counter = 0
        MockGraphQueryRedis()
        assert MockGraphQueryRedis._counter == 1

        MockGraphQueryRedis()
        MockGraphQueryRedis()
        MockGraphQueryRedis()
        MockGraphQueryRedis()
        assert MockGraphQueryRedis._counter == 5

    def test_graph_query_redis_by_xid(self):
        xid = b'person:foo'
        self.gr.by_xid(xid)
        val = self.r.smembers('query:1')
        assert val == set([xid])

    def test_graph_query_redis_get_attr_single(self):
        xid = 'person:foo'
        attr = 'past_company'

        self.gr.by_xid(xid)
        self.gr.get_attr(attr)

        val = self.r.smembers('query:1')
        assert val == set([b'company:b', b'company:c'])

    def test_graph_query_redis_get_attr_multiple(self):
        xid = 'person:foo'
        attr1 = 'past_company'    # ['company:b', 'company:c']
        attr2 = 'past_employees'  # company:c does not have any, should be ok

        self.gr.by_xid(xid)
        self.gr.get_attr(attr1)
        self.gr.get_attr(attr2)

        val = self.r.smembers('query:1')
        assert val == set([b'person:foo', b'person:bar'])

    def test_graph_query_redis_fetch(self):
        xid = 'person:foo'
        attr = 'past_company'

        self.gr.by_xid(xid)
        self.gr.get_attr(attr)

        val = self.gr.fetch()
        assert val == set([b'company:b', b'company:c'])

    def test_graph_query_redis_intersection(self):
        xid = 'company:b'
        attr2 = 'past_employees'

        q2 = MockGraphQueryRedis()
        q2.by_xid(xid)
        q2.get_attr(attr2)

        self.gr.by_xid('person:bar')
        self.gr.intersection(q2)

        val = self.r.smembers('query:1')
        assert val == set([b'person:bar'])

    def test_graph_query_redis_union_single(self):
        xid = 'company:b'
        attr1 = 'employees'
        attr2 = 'past_employees'

        q2 = MockGraphQueryRedis()
        q2.by_xid(xid)
        q2.get_attr(attr2)

        self.gr.by_xid(xid)
        self.gr.get_attr(attr1)
        self.gr.union(q2)

        val = self.r.smembers('query:1')
        assert val == set([b'person:baz', b'person:foo', b'person:bar'])

    def test_graph_query_redis_clear(self):
        xid = 'person:foo'
        attr = 'past_company'

        self.gr.by_xid(xid)
        self.gr.get_attr(attr)
        self.gr.clear()
        val = self.r.smembers('query:1')
        assert val == set()

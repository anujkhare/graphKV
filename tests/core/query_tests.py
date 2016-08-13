from nose.tools import raises

from graphdb.core.query import GraphQuery


@raises(NotImplementedError)
def test_graph_query_by_xid():
    GraphQuery().by_xid('foo')


@raises(NotImplementedError)
def test_graph_query_get_attr():
    GraphQuery().get_attr('foo')


@raises(NotImplementedError)
def test_graph_query_fetch():
    GraphQuery().fetch()


@raises(NotImplementedError)
def test_graph_query_fetch_with_attributes():
    GraphQuery().fetch_with_attributes()


@raises(NotImplementedError)
def test_graph_query_intersection():
    GraphQuery().intersection()


@raises(NotImplementedError)
def test_graph_query_union():
    GraphQuery().union()

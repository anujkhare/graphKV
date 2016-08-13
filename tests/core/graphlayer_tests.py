from nose.tools import raises

from graphdb.core.graphlayer import GraphLayer


@raises(NotImplementedError)
def test_graphlayer_save():
    GraphLayer().save()


@raises(NotImplementedError)
def test_graphlayer_set_edge():
    GraphLayer().set_attributes('foo', 'bar', 'baz')


@raises(NotImplementedError)
def test_graphlayer_set_multiple_edges():
    GraphLayer().set_multiple_edges()

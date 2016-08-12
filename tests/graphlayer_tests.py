from nose.tools import raises

import graphdb.graphlayer as graphlayer


@raises(NotImplementedError)
def test_graphlayer_save():
    graphlayer.GraphLayer().save()


@raises(NotImplementedError)
def test_graphlayer_set_edge():
    graphlayer.GraphLayer().set_edge('foo', 'bar', 'baz')


@raises(NotImplementedError)
def test_graphlayer_set_multiple_edges():
    graphlayer.GraphLayer().set_multiple_edges()

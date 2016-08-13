# This link: https://www.youtube.com/watch?v=EiOglTERPEo gives a very good idea
# about how to do dependency injection by multiple inheritance and mixins!
# So we'll have a (kind of pythonic) abstract class for the GraphDB with all
# required methods as "not implemented", which our code in the other component
# will inherit. To actually make this useful though, you need to have a specifi
# database linked implementation like GraphRedis, and create a new class which


class GraphLayer():
    def connect_db(self, **kwargs):
        raise NotImplementedError

    def set_attributes(self, source, attr, *values):
        ''' Set one attribute to a list of strings.
            Internally, the attributes are stored as sets, with keys
            "source:attr".
            Example: set_attributes('foo', 'skills', 'skill1', 'skill2')
        '''
        raise NotImplementedError

    def set_multiple_edges(self, **kwargs):
        '''Set variable list of edges, which are a dict containing {source,
           attr, dest}. Any invalid edges are ignored with a warning.
        '''
        raise NotImplementedError

    def save(self):
        '''Save the database on persistent storage. This is useful for the
           Redis backend.
        '''
        raise NotImplementedError

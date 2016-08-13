from graphdb.core.query import GraphQuery


class GraphQueryRedis(GraphQuery):
    _counter = 0
    _cur_entity_type = None

    def __init__(self):
        self.__class__._counter += 1
        self.query_name = 'query:' + str(self.__class__._counter)

    def by_xid(self, xid):
        ''' gets the entry by xid and stores in the memory
        '''
        raise(NotImplementedError)
#
#   def get_attr(self, attr):
#       ''' Gets the attr of the current results and stores in the memory.
#           NOTE: the attr must be a valid attr for the type of the results.
#       '''
#       raise(NotImplementedError)
#
#   def fetch(self):
#       ''' Returns the list of xids in the results.
#       '''
#       raise(NotImplementedError)
#
#   def fetch_with_attributes(self):
#       ''' Returns the entire list results along with all their attributes.
#       '''
#       raise(NotImplementedError)
#
#   def intersection(self, *queries):
#       ''' Takes the intersection of the results stored in each of the queries
#           and stores it in it's memory.
#           Each query must have the same type of result as this instance.
#       '''
#       raise(NotImplementedError)
#
#   def union(self, *queries):
#       raise(NotImplementedError)

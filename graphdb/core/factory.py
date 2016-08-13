# Generate the classes for our data
# We use a JSON schema to define the entities, and attributes in our data. This
# file creates the appropriate data structures to handle them.
#
# I want the storage to be strongly typed.

# We will dynamically generate a dict of classes using the names of entites in
# our schema, and use metaclass to populate the attributes of the respective
# classes. A special class var attr_list will contain the list of the attribute
# for the entity. FIXME: Why not use introspection?
# To use the entire system, people will need to instantiate one object from the
# class factory, which will give them the set of entity classes, and one
# instance from GraphRedis class, which gives a connection pool and helper
# methods to databse store.
import warnings

import graphlayer


# class BaseEntity(GraphLayer):
class BaseEntity(object):
    # This is a class variable, and will be initialised once using the factory.
    # It will be used by all the entity classes to generate backlinks
    # attribute_to = None
    __isfrozen = False

    def _freeze(self):
        self.__isfrozen = True

    def __setattr__(self, key, value):
        """Ensures that you only set arguments that are a part of the schema.
        """
        if (self.__isfrozen and not hasattr(self, key)):
            rstr = ('"{classname}" has no attribute "{attr}" in the '
                    'schema, ignoring..').format(
                        classname=self.__class__.__name__,
                        attr=key)
            warnings.warn(rstr)
            return
        super(BaseEntity, self).__setattr__(key, value)

    def __init__(self):
        self.attributes = {}

    def get_attribute_list(self):
        print('get attribute list')
        return vars(self)

    # @attributes.setter
    def set_attributes(self, **kwargs):
        """To set multiple attributes using keywords
        """
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    # @propery # NEEds to be handled on DB side
    # def uid(self):
    #     return self.__classname__ + ':' + self.name

    def generate_backlinks(self):
        """Each entity class is given information
        """
        pass

    def add_to_graph_db(self, graph_redis):
        # assert issubclass(graph_redis, GraphLayerRedis)
        pass


class TestEntity(BaseEntity):
    def __init__(self):
        self.x = 10
        self.y = 20
        self._freeze()


class EntityFactory():
    _entities = None
    _attributes = None

    def __init__(self, schema_path):
        self._classes = {}
        self.set_schema(schema_path)

    def set_schema(self, schema_path):
        """ Takes a schema for the database to generate the entity classes.
            Ideally, use one instance per application.
        """
        # load the schema
        # generate subclasses of BaseEntity depending on the schema
        pass

    def _parse_schema(schema):
        pass

    @property
    def classes(self):
        return self._classes

# @classes.setter
# def classes(self, **kwargs):
#     print ("Can not modify classes! Please set_schema to change the schema")

# need to have constructor that will take kwargs, check correctness of
# attributes. provide a method to store the data in the db
# DO NOT connect to the GraphRedis instance here, just take an object of it,
if __name__ == '__main__':
    graphlayer.foo()
    graph_redis = graphlayer.GraphLayerRedis()
    e = BaseEntity()

    e.a = 10
    e.b = 20
    e.c = 30

    t = TestEntity()
    t.x = 10000
    t.y = 12
    print(t.__dict__)

    t.set_attributes(x=-1, y=22, z=111)
    print(t.__dict__)
# On first instantiation, it inputs the schema and parses it to get the
# type system of our dataset. On successive instantiations, it uses the
# same schema unless explicitly changed.

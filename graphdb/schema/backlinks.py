import json


class BacklinksHelper():
    def __init__(self, path_to_schema):
        self.parse_schema(path_to_schema)

    def parse_schema(self, path_to_schema):
        if not path_to_schema:
            print('Invalid path to schema file')
            raise(ValueError)
        with open(path_to_schema) as infile:
            schema = json.load(infile)
        # print(schema)
        self.entities = schema['entities']
        self.literals = schema['literals']

    def validate_attributes(self, entity_type, attr_dict):
        if entity_type not in self.entities:
            print('entity "', entity_type, '" is not defined in the schema')
            return False

        entity_attrs = self.entities[entity_type]
        for attr, _ in attr_dict.items():
            if attr not in entity_attrs:
                print('attr "', attr, '" is not a attribute of', entity_type)
                return False

        return True

    def get_backlinks(self, attr_dict):
        ''' Takes one entity's attribute dict and returns a dict with keys =
            uids, and values = attribute dictionaries for the respective
            entity.
        '''
        entity_type = attr_dict.get('type', None)
        if entity_type is None:
            print('No "type" attribute found in attr_dict.')
            raise(ValueError)

        if not self.validate_attributes(entity_type, attr_dict):
            raise(ValueError)

        schema_entity = self.entities[entity_type]
        out_data = {}
        for attr, values in attr_dict.items():
            back_entity = schema_entity[attr].get('to')
            back_attr = schema_entity[attr].get('reverse', None)
            if back_attr is None:
                continue

            if type(values) is str:
                values = [values]
            for val in values:
                if val not in out_data:
                    out_data[val] = {}

                out_data[val]['type'] = back_entity
                out_data[val]['uid'] = val
                out_data[val][back_attr] = attr_dict['uid']

        return out_data

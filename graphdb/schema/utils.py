import json


def add_templates_to_dict(target_dict, template_dict, *template_names):
    if type(target_dict) is not dict:
        print("target_dict should be a dict, please supply a dict")
        raise(ValueError)

    for name in template_names:
        for key, value in template_dict[name].items():
            target_dict[key] = {'to': value}


def generate_full_schema(partial_schema):
    ''' Takes a partial schema (without backlinks and attribute entries, and
        generates a full explicit schema from it.
    '''
    literals = partial_schema['literals']
    template_dict = partial_schema['templates']
    new_entities = {}

    for entity, attr_dict in partial_schema['entities'].items():
        if entity not in new_entities:
            new_entities[entity] = {}

        for attr, val_type in attr_dict.items():
            if attr == "_templates":   # add the template attributes
                add_templates_to_dict(new_entities[entity], template_dict,
                                      *val_type)
                continue

            if type(val_type) is str:  # only one value - literal type
                if val_type not in literals:
                    print("The literal type " + val_type + " is not defined"
                          "in 'literals'")
                    raise(ValueError)

                # Add the normal keys to new_dict
                new_entities[entity][attr] = {'to': val_type}

            else:  # multiple values - create a backlink
                # Add the normal keys to new_dict
                new_entities[entity][attr] = {'to': val_type[0]}

                new_entity = val_type[0]
                # create the entity key if not already present
                if new_entity not in new_entities:
                    new_entities[new_entity] = {}
                if len(val_type) > 1:
                    new_entities[new_entity][val_type[1]] = {'to': entity,
                                                             'reverse': attr}
                    new_entities[entity][attr]['reverse'] = val_type[1]

    full_schema = {'schema-name': partial_schema['schema-name'],
                   'literals': literals,
                   'entities': new_entities
                   }
    return full_schema

if __name__ == '__main__':
    path_to_schema = 'tests/schema/schema.json'
    with open(path_to_schema) as infile:
        partial_schema = json.load(infile)

    # print(partial_schema)
    full_schema = generate_full_schema(partial_schema)
    with open('out.json', 'w') as f:
        json.dump(full_schema, f, indent=4, separators=(',', ': '),
                  sort_keys=True)

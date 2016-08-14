from graphdb.schema.backlinks import BacklinksHelper


path_to_schema = 'tests/schema/full_schema.json'


class TestSchemaBacklinksHelper():
    def setUp(self):
        self.backhelper = BacklinksHelper(path_to_schema)

    def tearDown(self):
        pass

    def test_schema_validate_data_invalid_entity(self):
        bh = self.backhelper
        is_valid = bh.validate_attributes('invalid_entity',
                                          {
                                           'name': 'bar',
                                           'baz': 'foo'
                                          }
                                          )
        assert not is_valid

    def test_schema_validate_data_invalid_attr(self):
        bh = self.backhelper
        is_valid = bh.validate_attributes('person',
                                          {
                                           'name': 'bar',
                                           'invalid_attr': 'foo'
                                          }
                                          )
        assert not is_valid

    def test_schema_validate_data_valid(self):
        bh = self.backhelper
        is_valid = bh.validate_attributes('company',
                                          {
                                           'name': 'bar',
                                           'investors': 'foo'
                                          }
                                          )
        assert is_valid

    def test_schema_get_backlinks_single(self):
        bh = self.backhelper
        attr_dict = {
                     'name': 'foo oof',
                     'uid': 'foo',
                     'studied at': 'college-bar'
                     }
        out_dict = bh.get_backlinks(attr_dict)

        expected_dict = {
                         'college-bar': {
                            'uid': 'college-bar',
                            'alumni': 'foo'
                          }
                        }

        assert expected_dict == out_dict

    def test_schema_get_backlinks_multiple(self):
        bh = self.backhelper
        attr_dict = {
                     'name': 'foo oof',
                     'uid': 'foo',
                     'type': 'company',
                     'founders': 'person1',
                     'current employees': ['person1', 'person2']
                     }
        out_dict = bh.get_backlinks(attr_dict)

        expected_dict = {
                         'person1': {
                            'uid': 'person1',
                            'work at': 'foo',
                            'type': 'person',
                            'founded': 'foo'
                          },
                         'person2': {
                            'uid': 'person2',
                            'work at': 'foo',
                            'type': 'person'
                          }
                        }

        print(out_dict)
        print(expected_dict)
        assert expected_dict == out_dict

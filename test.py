import unittest
from main import SchemaGenerator


class TestSchemaGenerator(unittest.TestCase):
    """
    This class handle testing schema generator class
    """

    def test_valid_schema(self):
        expected_schema = {}
        schema = SchemaGenerator('valid_schema.json')
        resp = schema.run()
        assert resp.get('status') is True
        assert expected_schema == resp.get('schema')

    def test_invalid_data_without_message_key(self):
        schema = SchemaGenerator('invalid_schema_without_message_key.json')
        resp = schema.run()
        assert resp.get('status') is False
        assert resp.get('message') == 'message key missing from json file'

    def test_schema_generator(self):
        file_list = ['data_1.json', 'data_2.json']
        for file in file_list:
            schema = SchemaGenerator(file)
            resp = schema.run()
            assert resp.get('status') is True


if __name__ == '__main__':
    unittest.main()

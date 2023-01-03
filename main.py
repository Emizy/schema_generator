import json
import os
import random

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseSchema:
    """
    This class indicate the base class which entails method that handle generating schema based on data-types

    """

    def __init__(self):
        pass

    @staticmethod
    def generate_int(key):
        """
        handle generating of integer type schema
        :param key:
        :return:
        """
        payload = {
            key: {
                "type": "integer",
                "tag": "",
                "description": "",
                "required": False
            }
        }
        return payload

    @staticmethod
    def generate_string(key):
        """
        handle generating of string type schema
        :param key:
        :return:
        """
        payload = {
            key: {
                "type": "string",
                "tag": "",
                "description": "",
                "required": False
            }
        }
        return payload

    @staticmethod
    def generate_enum(key):
        """
        handle generating of enum type schema
        :param key:
        :return:
        """
        payload = {
            key: {
                "type": "ENUM",
                "tag": "",
                "description": "",
                "required": False
            }
        }
        return payload

    @staticmethod
    def generate_array(key):
        """
        handle generating of array type schema
        :param key:
        :return:
        """
        payload = {
            key: {
                "type": "ARRAY",
                "tag": "",
                "description": "",
                "required": False
            }
        }
        return payload


class SchemaGenerator(BaseSchema):
    """
    this class handle generating schema based on the file name supplied as parameter
    """

    def __init__(self, file_name):
        """
        :param file_name:
        """
        super().__init__()
        self.file_name = file_name

    def generate(self, key, value):
        if isinstance(value, list):
            # check if array is either an enum or normal
            enum_exist = [True for k in value if type(k) is str]
            if len(enum_exist) == len(value):
                # array is not enum
                return self.generate_enum(key)
            else:
                return self.generate_array(key)
        elif isinstance(value, str):
            return self.generate_string(key)
        elif isinstance(value, int):
            return self.generate_int(key)
        return {}

    def process_(self, key, value):
        """
        the method handle the actual generating of the schema based on the data being passed as parameter and also handle generating
        of nested schema for a schema that is nested inside an object
        :param key:
        :param value:
        :return:
        """
        if isinstance(value, dict):
            data = {
                "type": "object",
                "tag": "",
                "description": "",
                "required": False,
            }
            if len(value.keys()) > 0:
                data.update({"properties": {}})
                for k, v in value.items():
                    if isinstance(v, dict):
                        res = self.process_(k, v)
                        data['properties'].update(res)
                    else:
                        data['properties'].update(self.generate(k, v))
            else:
                return data
        else:
            return self.generate(key, value)
        return {key: data}

    def run(self):
        """
        This indicate the method to be called after initializing the schema generator class
        it handles validating of the file if it exist inside the data directory and also call the
        process_ method to generate a schema for each data entry
        :return:
        """
        file_path = os.path.join(PROJECT_DIR, f'data/{self.file_name}')
        save_dir = os.path.join(PROJECT_DIR, f'schema')
        if os.path.isfile(file_path) is False:
            return {'status': False, 'message': 'File does not exist'}

        with open(file_path, 'r') as file:
            data = json.load(file)
        if isinstance(data, dict) is False:
            return {'status': False, 'message': 'Invalid json file, after loading the data is not an instance of dict'}
        if 'message' not in data:
            return {'status': False, 'message': 'message key missing from json file'}
        message = data.get('message')
        schema = {}
        for key, value in message.items():
            schema.update(self.process_(key, value))
        with open(f"{save_dir}/schema_{random.randint(0, 100)}.json", "w") as outfile:
            json.dump(schema, outfile)
        return {'schema': schema, 'status': True}

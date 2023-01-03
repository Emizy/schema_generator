### SCHEMA GENERATOR

The objective of the project is to:

- Reads a JSON file that is located inside (./data/)
- Sniffs the schema of the JSON file
- Dumps the output in (./schema/)

### How to run

- Import schema generator class from ``main.py``
- Place the json file containing the data inside the ``./data/`` directory
- Initialize the schema generator instance by passing the json file name as parameter to the class
- After the schema generator class as be instantiated, call ``.run()`` method which return a dictionary containing the
  following
    1. status: is a boolean object which indicate the state of the response (True/False)
    2. schema: This is the equivalent schema generated for the json file and its will only be return
       if ``status is True``
    3. message: This contains information regarding the current state of the system and its only return
       if ``status is False``

### How to run test

This following are needed to be made provision for in order to run the test

- json file with name valid_schema.json needs to be created inside ``/data/`` directory and its corresponding schema
  data should be added to the test case named: ``test_valid_schema``
- json file with name ``invalid_schema_without_message_key.json`` needs to be created inside ``/data`` directory which
  contain a json data without  ``message attribute``

Inside your terminal run the command below

```
python test.py
```
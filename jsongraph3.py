#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""JSON Graph Python Library

Parameters
----------
None

Returns
-------
None

Long Description
"""

import json
import os.path
from jsonschema import Draft4Validator
import sys
import urllib.request, urllib.parse, urllib.error


def load_json_string(jsonstring):
    '''Check if string is JSON and if so return python dictionary'''

    try:
        json_object = json.loads(jsonstring)
    except ValueError as e:
        return False
    return json_object


def get_github_masterschema():
    '''Read JSON Graph Schema file from Github Master branch'''
    link = 'https://raw.githubusercontent.com/jsongraph/json-graph-specification/master/json-graph-schema.json'
    f = urllib.request.urlopen(link)
    js = json.load(f)
    f.close

    return js


def get_json(jsongraph):
    '''Check if parameter is a file object, filepath or JSON string

        Return:  dictionary object OR False for failure
    '''
    if type(jsongraph) is dict:
        return jsongraph
    elif type(jsongraph) is file:
        return json.load(jsongraph)
    elif os.path.isfile(jsongraph):
        with open(jsongraph, 'rb') as f:
            return json.load(f)

    jg = load_json_string(jsongraph)
    if jg:
        return jg
    else:
        return False


def validate_schema(schema='', verbose=False):
    '''Validate schema file'''

    if not schema:
        schema = get_github_masterschema()
    else:
        schema = get_json(schema)

    results = Draft4Validator.check_schema(schema)

    if verbose and results:
        print("    Schema doesn't validate!")
        print(results)
    elif verbose:
        print("    Schema Validates!")

    if results:
        return (False, results)

    return (True, '')


def validate_jsongraph(jsongraph, schema='', verbose=False):
    '''Validate JSON Graph against given jsongraph object and schema object'''

    jg = get_json(jsongraph)

    if not schema:
        schema = get_github_masterschema()
    else:
        schema = get_json(schema)

    if not jg:
        sys.exit('JSON Graph parameter does not appear to be a file object, filepath or JSON string.')
    if not schema:
        sys.exit('JSON Graph Schema parameter does not appear to be a file object, filepath or JSON string.')

    schema = Draft4Validator(schema)  # transform schema in a Schema validation object

    errors = [error for error in schema.iter_errors(jg)]
    if verbose and errors:
        print('Problem with JSON Graph')
        for error in errors:
            print(error)

        quit()

    elif verbose:
        print("    Validated!")

    if errors:
        return errors

    return (True, '')


def load_graphs(jsongraphs, validate=False, schema='', verbose=False):
    '''Loads one or more graphs from jsongraphs JSON as a generator'''

    jgs = get_json(jsongraphs)

    if validate:
        (status, results) = validate_jsongraph(jsongraphs, schema, verbose)
        sys.exit('JSON Graph does not validate')

    if 'graph' in jgs:
        yield jgs['graph']

    if 'graphs' in jgs:
        for graph in jgs['graphs']:
            yield graph


def test_example_graphs():
    '''Test and usage example'''
    single_graph_link = 'https://raw.githubusercontent.com/jsongraph/json-graph-specification/master/examples/usual_suspects.json'
    multiple_graph_link = 'https://raw.githubusercontent.com/jsongraph/json-graph-specification/master/examples/car_graphs.json'

    f = urllib.request.urlopen(single_graph_link)
    sg = json.load(f)
    f.close

    f = urllib.request.urlopen(multiple_graph_link)
    mg = json.load(f)
    f.close

    print("Does JSON Graph Schema validate?")
    validate_schema(schema='', verbose=True)

    print("\nDoes Single Graph example validate?")
    validate_jsongraph(sg, schema='', verbose=True)

    print("\nShow Label of Single Graph")
    graphs = load_graphs(sg, validate=False, schema='', verbose=False)
    print("    Label: ", next(graphs)['label'])

    print("\nShow Label's of Multiple Graphs")
    graphs = load_graphs(mg, validate=False, schema='', verbose=False)
    for graph in graphs:
        print("    Label: ", graph['label'])


def main():
    test_example_graphs()


if __name__ == '__main__':
    main()

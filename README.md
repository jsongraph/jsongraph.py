jsongraph.py
============

Python library for jsongraph

You can run the jsongraph.py from the command line to see how to use the library.  The three key functions to use are:

    load_graphs(jsongraphs, validate=False, schema='', verbose=False)

    validate_jsongraph(jsongraph, schema='', verbose=False)

    validate_schema(schema='', verbose=False)

The default json schema file is the Github Master branch JSON Graph Specification file.  The *jsongraph(s)* and *schema* parameters can be python dict's, file objects, filenames, or JSON strings and the library will detect the type in that order or return False if none of those attempts to read in the JSON or JSON Schema works.


Example usage:

    import jsongraph
    import urllib
    import json

    '''Test and usage example'''
    single_graph_link = 'https://raw.githubusercontent.com/jsongraph/json-graph-specification/master/examples/usual_suspects.json'
    multiple_graph_link = 'https://raw.githubusercontent.com/jsongraph/json-graph-specification/master/examples/car_graphs.json'

    f = urllib.urlopen(single_graph_link)
    sg = json.load(f)
    f.close

    f = urllib.urlopen(multiple_graph_link)
    mg = json.load(f)
    f.close

    # Uses Github Master branch JSON Graph Specification file by default
    print "Does JSON Graph Schema validate?"
    jsongraph.validate_schema(schema='', verbose=True)

    print "\nDoes Single Graph example validate?"
    jsongraph.validate_jsongraph(sg, schema='', verbose=True)

    print "\nShow Label of Single Graph"
    graphs = jsongraph.load_graphs(sg, validate=False, schema='', verbose=False)
    print "    Label: ", next(graphs)['label']

    print "\nShow Label's of Multiple Graphs"
    graphs = jsongraph.load_graphs(mg, validate=False, schema='', verbose=False)
    for graph in graphs:
        print "    Label: ", graph['label']

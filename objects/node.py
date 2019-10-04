import json
import unittest

class Node:

    ID = 'id'
    LABEL = 'label'
    METADATA = "metadata"

    def __init__(self, id, label=None, metadata=None):
        self.set_id(id)
        self._label = None
        if label != None:
            self.set_label(label)
        self._metadata = None
        if metadata != None:
            self.set_metadata(metadata)

    def _isJsonSerializable(self, dictionay):
        try:
            json.dumps(dictionay)
            return True
        except Exception:
            return False

    def set_id(self, id):
        if id == None:
            raise ValueError('Id of Node can not be None')
        if isinstance(id, str):
            self._id = id
        else:
            try:
                stringId = str(id)
                self._id = stringId
            except Exception as excecption:
                raise TypeError("Type of id in Node needs to be a string (or string castable): " + str(exception))
            
    def set_label(self, label):
        if label == None:
            self._label = None
            return
        if isinstance(label, str):
            self._label = label
        else:
            try:
                stringLabel = str(label)
                self._label = stringLabel
            except Exception as excecption:
                raise TypeError("Type of label in Node object needs to be a string (or string castable): " + str(exception))

    def set_metadata(self, metadata):
        if metadata == None:
            self._metadata = None
        if isinstance(metadata, dict) and self._isJsonSerializable(metadata):
            self._metadata = metadata
        else:
            raise TypeError("metadata in Node object needs to be json serializable")

    def get_id(self):
        return self._id

    def get_label(self):
        return self._label

    def get_metadata(self):
        return self._metadata

    def to_JSON(self):
        json = {Node.ID: self._id}
        if self._label != None:
            json[Node.LABEL] = self._label
        if self._metadata != None:
            json[Node.METADATA] = self._metadata


class TestNodeClass(unittest.TestCase):

    def test_base(self):
        node = Node('nodeId', 'nodeLabel', {'metaNumber': 11, 'metaString': 'hello world'})

        self.assertEqual(node.get_id(), 'nodeId')
        self.assertEqual(node.get_label(), 'nodeLabel')
        self.assertEqual(node.get_metadata()['metaNumber'], 11)
        self.assertEqual(node.get_metadata()['metaString'], 'hello world')

    def test_setters(self):
        node = Node('nodeId', 'nodeLabel', {'metaNumber': 11, 'metaString': 'hello world'})
        node.set_id('new_nodeId')
        node.set_label('new_nodeLabel')
        node.set_metadata({'new_metaNumber': 13, 'new_metaString': 'world hello'})

        self.assertEqual(node.get_id(), 'new_nodeId')
        self.assertEqual(node.get_label(), 'new_nodeLabel')
        self.assertEqual(node.get_metadata()['new_metaNumber'], 13)
        self.assertEqual(node.get_metadata()['new_metaString'], 'world hello')
        #TODO unittest error handling

    def test_to_JSON(self):
        self.assertEqual("TODO", "TODO")
        #TODO unittest json result

if __name__ == '__main__':
    unittest.main()

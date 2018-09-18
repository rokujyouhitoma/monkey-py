import unittest

from monkey import object


class TestObject(unittest.TestCase):
    def test_string_hash_key(self):
        hello1 = object.String(Value='Hello World')
        hello2 = object.String(Value='Hello World')
        diff1 = object.String(Value='My name is johnny')
        diff2 = object.String(Value='My name is johnny')

        if object.GetHashKey(hello1) != object.GetHashKey(hello2):
            self.fail('strings with same content have different hash keys')

        if object.GetHashKey(diff1) != object.GetHashKey(diff2):
            self.fail('strings with same content have different hash keys')

        if object.GetHashKey(hello1) == object.GetHashKey(diff1):
            self.fail('strings with different content have same hash keys')

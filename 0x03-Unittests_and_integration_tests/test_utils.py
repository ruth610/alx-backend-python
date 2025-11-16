#!/usr/bin/env python3
import unittest

from parameterized import parameterized

from utils import access_nested_maps

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a":1}, ("a",),1),
        ({"a":{"b":2}},("a","b"),1),
        ({"a":{"b":2}},("a",),{"b":2})
    ])

    def test_access_nested_map(self,nested_map,path,expected_value):
        self.assertEqual(access_nested_maps(nested_map,path),expected_value)


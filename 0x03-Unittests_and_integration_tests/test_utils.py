#!/usr/bin/env python3
"""
This module contains unit tests for the following functions in utils.py:

- access_nested_map
- get_json
- memoize

Tests include normal cases, exceptions, and memoization behavior.
"""
import unittest
from unittest.mock import Mock, patch

from parameterized import parameterized

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test the function for correct behavior and exceptions."""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}},
             ("a", "b"),
             2),
            ({"a": {"b": 2}},
             ("a",),
             {"b": 2}),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected_value):
        """Test access_nested_map returns the correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected_value)

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(str(error.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Test the `get_json` function using mocked HTTP responses."""

    @parameterized.expand(
        [
            ("http://example.com",
             {"payload": True}),
            ("http://holberton.io",
             {"payload": False}),
        ]
    )
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns expected payload and calls get once."""
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)
            mock_get.assert_called_once_with(
                test_url
            )
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test the `memoize` decorator to ensure it caches results correctly."""

    def test_memoize(self):
        """Test that memoized property caches result & calls method once."""

        class TestClass:
            def a_method(self):
                """A simple method returning 42."""
                return 42

            @memoize
            def a_property(self):
                """A memoized property calling a_method once."""
                return self.a_method()

        obj = TestClass()

        with patch.object(
                TestClass,
                "a_method",
                return_value=42
        ) as mock_method:
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()

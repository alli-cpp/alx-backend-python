#!/usr/bin/env python3

""" Parametizing a unit test """
import unittest
from unittest import mock
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a", ), 1),
        ({"a": {"b": 2}}, ("a", ), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: any):
        """test the access_nested_map method of utils"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a", )),
        ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence):
        self.assertRaises(KeyError, access_nested_map, nested_map, path)


class TestClass:

    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()


class TestMemoize(unittest.TestCase):

    @patch.object(TestClass, 'a_method', return_value=42)
    def test_memoize(self, mock_a_method):
        # create an instance of TestClass
        test_obj = TestClass()
        # call a_property twice
        result1 = test_obj.a_property
        result2 = test_obj.a_property
        # assert that the correct result is returned
        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)
        # assert that a_method is only called once
        mock_a_method.assert_called_once()


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        # create a mock response object with a json method that returns test_payload
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = test_payload
        # set the return value of requests.get to mock_response
        mock_get.return_value = mock_response
        # call get_json with test_url
        result = get_json(test_url)
        # assert that requests.get is called once with test_url as argument
        mock_get.assert_called_once_with(test_url)
        # assert that result is equal to test_payload
        self.assertEqual(result, test_payload)

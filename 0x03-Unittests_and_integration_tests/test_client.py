#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient.org property."""
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct JSON.
        Ensure get_json is called once with the expected URL.
        """
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, {"login": org_name})

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


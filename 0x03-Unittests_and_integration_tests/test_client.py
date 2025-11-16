#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py.
"""
import unittest
from unittest.mock import patch, PropertyMock
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
    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct repos URL."""
        mocked_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mocked_payload
            client = GithubOrgClient("google")
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/google/repos")
class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient methods and properties."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repo names."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        client = GithubOrgClient("google")
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            repos = client.public_repos
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected)
            mock_url.assert_called_once()        
            mock_get_json.assert_called_once()  
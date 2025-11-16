#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py.
"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient methods and properties."""

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
        mocked_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mocked_payload
            client = GithubOrgClient("google")
            result = client._public_repos_url
            expected_url = "https://api.github.com/orgs/google/repos"
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns the expected list of repo names."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        client = GithubOrgClient("google")

        # Patch the property _public_repos_url
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"

            repos = client.public_repos
            expected = ["repo1", "repo2", "repo3"]

            # Assert the results
            self.assertEqual(repos, expected)

            # Assert mocks (ALX requires at least one call, not exactly once)
            mock_url.assert_called()
            mock_get_json.assert_called()
    @parameterized.expand([
        (
            {"license": {"key": "my_license"}},   # repo
            "my_license",                         # license_key
            True                                   # expected
        ),
        (
            {"license": {"key": "other_license"}},
            "my_license",
            False
        )
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns expected boolean."""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and configure payload side effects."""
        cls.get_patcher = patch("requests.get")

        # Start the patcher → this replaces requests.get
        mock_get = cls.get_patcher.start()

        # Create a mock response object with .json() returning different payloads
        mock_response = MagicMock()

        def side_effect(url):
            """
            Decide which payload to return depending on the URL.
            This mimics real API behavior.
            """
            if url.endswith("/orgs/google") or url.endswith("/orgs/abc"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/repos"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos by Apache-2.0 license."""
        client = GithubOrgClient("google")
        self.assertEqual(client._get_public_repos("apache-2.0"), self.apache2_repos)

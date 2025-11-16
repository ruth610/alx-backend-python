#!/usr/bin/env python3
"""
Unit and integration tests for the GithubOrgClient class in client.py.
"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient

# --- FIX: INLINED FIXTURES to resolve ImportError ---
org_payload = {
    "login": "google",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {
        "id": 1,
        "name": "repo1",
        "license": {"key": "apache-2.0"}
    },
    {
        "id": 2,
        "name": "repo2",
        "license": {"key": "mit"}
    },
    {
        "id": 3,
        "name": "repo3",
        "license": {"key": "apache-2.0"}
    }
]

expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]
# --- END FIXTURES ---

# REMOVE: from fixtures import org_payload, repos_payload
# expected_repos, apache2_repos


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
        Ensures get_json is called once with the correct URL.
        """
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the correct repos URL.
        Mocks the self.org property.
        """
        mocked_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        mock_org.return_value = mocked_payload

        client = GithubOrgClient("google")
        result = client._public_repos_url

        self.assertEqual(result, mocked_payload["repos_url"])
        mock_org.assert_called_once()  # Added explicit assertion for mock_org

    @patch("client.get_json")
    @patch.object(
        GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
    )
    def test_public_repos(self, mock_url, mock_get_json):
        """
        Test public_repos returns the expected list of repo names.
        Uses decorators for cleaner mocking of the property and get_json.
        """
        # Set up the mock for get_json (fetches repo list)
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        # Set up the mock for the _public_repos_url property
        mock_url.return_value = "https://api.github.com/orgs/google/repos"

        client = GithubOrgClient("google")

        repos = client.public_repos
        expected = ["repo1", "repo2", "repo3"]

        self.assertEqual(repos, expected)
        # Use assert_called_once() for stricter verification in unit tests
        mock_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns expected boolean."""
        # This method is a static method, so the client instance is irrelevant.
        # Calling the static method directly on the class is cleaner.
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patching get_json and configure payload side effects."""
        cls.get_patcher = patch("client.get_json")
        cls.mock_get_json = cls.get_patcher.start()

        # Side effect function to return correct payloads
        def side_effect(url):
            # FIX E501 (Line 119) and Logical Error: Use
            # the correct class variables
            # FIX E501: Breaking long string
            org_url = f"https://api.github.com/orgs/{cls.org_payload['login']}"

            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            if url == org_url:
                return cls.org_payload
            return {}

        cls.mock_get_json.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching get_json."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all repo names."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos by Apache-2.0 license."""
        client = GithubOrgClient(self.org_payload["login"])
        # The license filtering is done by calling the helper method
        self.assertEqual(
            client._public_repos(license="apache-2.0"), self.apache2_repos
        )

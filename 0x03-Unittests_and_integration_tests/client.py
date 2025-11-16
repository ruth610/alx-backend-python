#!/usr/bin/env python3
"""
This module contains the GithubOrgClient class that interacts
with the GitHub API.
"""
from utils import get_json


class GithubOrgClient:
    """Github organization client."""

    def __init__(self, org_name):
        """Initialize with the organization name."""
        self.org_name = org_name

    @property
    def org(self):
        """
        Returns the organization information as a dictionary.

        Uses get_json to fetch data from:
        https://api.github.com/orgs/<org_name>
        """
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

    @property
    def _public_repos_url(self):
        """Return the URL of the organization’s public repositories."""
        return self.org["repos_url"]

    @property
    def public_repos(self, license=None):
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo["name"] for repo in repos]
        return [repo["name"] for repo in repos if self.has_license(repo, license)]
    @staticmethod
    def has_license(repo, license_key):
        return repo.get("license", {}).get("key") == license_key

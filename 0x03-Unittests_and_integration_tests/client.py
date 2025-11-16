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
        """Return organization information as a dictionary."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

    @property
    def _public_repos_url(self):
        """Return the URL of the organization’s public repositories."""
        return self.org["repos_url"]

    # Renamed from _public_repos to clarify its helper role
    def _get_public_repos(self, license=None):
        """Return list of public repo names, optionally filtered by license."""
        repos = get_json(self._public_repos_url)

        if license is None:
            return [repo["name"] for repo in repos]

        return [
            repo["name"]
            for repo in repos
            if self.has_license(repo, license)
        ]

    # RENAMED from all_public_repos to public_repos (Fixes the AttributeError)
    @property
    def public_repos(self):
        """Property to return list of public repo names."""
        # Now calls the helper method without arguments
        return self._get_public_repos()

    @staticmethod
    def has_license(repo, license_key):
        """Check if repo has the requested license."""
        return repo.get("license", {}).get("key") == license_key
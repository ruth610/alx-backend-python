#!/usr/bin/env python3
"""
This module contains the GithubOrgClient class that interacts
with the GitHub API.
"""
from utils import get_json


class GithubOrgClient:
    """Github organization client."""

    def __init__(self, org_name: str):
        """Initialize with the organization name."""
        self.org_name = org_name

    @property
    def org(self) -> dict:
        """Return organization information as a dictionary."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

    @property
    def _public_repos_url(self) -> str:
        """Return the URL of the organization’s public repositories."""
        return self.org["repos_url"]

    def _public_repos(self, license: str = None) -> list:
        """Return list of public repo names, optionally filtered by license."""
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo["name"] for repo in repos]
        return [
            repo["name"]
            for repo in repos
            if self.has_license(repo, license)
        ]

    @property
    def public_repos(self) -> list:
        """Return all public repo names (unfiltered)."""
        return self._public_repos()

    @staticmethod
    def has_license(repo: dict, license_key: str) -> bool:
        """Check if repo has the requested license."""
        return repo.get("license", {}).get("key") == license_key

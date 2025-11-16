#!/usr/bin/env python3
from utils import get_json

class GithubOrgClient:
    """Github organization client."""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

    @property
    def _public_repos_url(self):
        return self.org["repos_url"]

    def has_license(self, repo, license_key):
        return repo.get("license", {}).get("key") == license_key

    @property
    def public_repos(self):
        """Return list of repo names."""
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

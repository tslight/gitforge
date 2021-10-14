import logging
import json
from .git import Git
from .utils import paginated_requests as get


class GitHub(Git):
    def __init__(self, token, destination, protocol, affiliation):
        super().__init__(destination)
        self.url = "https://api.github.com"
        self.params = {"per_page": "100", "affiliation": ",".join(affiliation)}
        self.headers = {"Authorization": f"token {token}"}
        self.protocol = protocol

    def transform_repo(self, repo):
        transformed = {}

        for key, value in repo.items():
            if key == "id":
                transformed["id"] = value
            elif key == "name":
                transformed["name"] = value
            elif key == "full_name":
                transformed["path"] = value
            elif key == "ssh_url" and self.protocol == "ssh":
                transformed["url"] = value
            elif key == "clone_url" and self.protocol == "http":
                transformed["url"] = value

        return transformed

    def get_all_repos(self):
        try:
            logging.info(f"Retrieving repos from {self.url}/user/repos... ")
            repos = get(self.url + "/user/repos", self.headers, self.params, results=[])
            logging.debug(json.dumps(repos, indent=2))
            repos = [self.transform_repo(r) for r in repos]
            return repos
        except Exception as exc:
            logging.debug(exc)
            raise exc

    def get_repos(self, requested_repos):
        repos = []

        for r in self.get_all_repos():
            for name in requested_repos:
                if (
                    r["name"] == name
                    or r["path"] == name
                    or r["path"].endswith(name)
                    or r["path"].startswith(name)
                ):
                    repos.append(r)

        return repos

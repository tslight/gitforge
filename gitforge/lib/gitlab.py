import json
import logging
from .git import Git
from .utils import paginated_requests as get


class GitLab(Git):
    def __init__(self, token, destination, protocol):
        super().__init__(destination)
        self.url = "https://gitlab.com/api/v4"
        self.params = {
            "per_page": "100",
            "membership": "true",
        }
        self.headers = {"PRIVATE-TOKEN": token}
        self.protocol = protocol

    def transform_repo(self, repo):
        transformed = {}

        for key, value in repo.items():
            if key == "id":
                transformed["id"] = value
            elif key == "name":
                transformed["name"] = value
            elif key == "path_with_namespace":
                transformed["path"] = value
            elif key == "ssh_url_to_repo" and self.protocol == "ssh":
                transformed["url"] = value
            elif key == "http_url_to_repo" and self.protocol == "http":
                transformed["url"] = value

        return transformed

    def get_all_repos(self):
        try:
            logging.info(f"Retrieving repos from {self.url}/projects... ")
            repos = get(self.url + "/projects", self.headers, self.params, results=[])
            logging.debug(json.dumps(repos, indent=2))
            repos = [self.transform_repo(r) for r in repos]
            return repos
        except Exception as exc:
            logging.debug(exc)
            raise exc

    def get_all_groups(self):
        try:
            logging.info(f"Retrieving groups from {self.url}/groups... ")
            groups = get(self.url + "/groups", self.headers, self.params, results=[])
            logging.debug(json.dumps(groups, indent=2))
            return groups
        except Exception as exc:
            logging.debug(exc)
            raise exc

    def get_subgroups(self, requested_groups):
        groups = []

        for grp in self.get_all_groups():
            for group in requested_groups:
                path_elements = grp["full_path"].split("/")
                explicit_subgroup = grp["full_path"].startswith(group)
                implicit_subgroup = group in path_elements and path_elements.index(
                    group
                ) < path_elements.index(grp["name"])
                is_group = grp["name"] == group
                if is_group or explicit_subgroup or implicit_subgroup:
                    groups.append(grp)

        return groups

    def get_group_repos(self, groups):
        groups = self.get_subgroups(groups)
        all_repos = []
        for group in groups:
            try:
                logging.info(
                    f"Retrieving repos from {self.url}/{group['id']}/projects... "
                )
                repos = get(
                    f"{self.url}/groups/{group['id']}/projects",
                    self.headers,
                    self.params,
                    results=[],
                )
                logging.debug(json.dumps(repos, indent=2))
                repos = [self.transform_repo(r) for r in repos]
                all_repos.extend(repos)
            except Exception as exc:
                logging.debug(exc)
                raise exc

        return all_repos

    def get_repos(self, requested_repos):
        repos = []

        for repo in self.get_all_repos():
            for name in requested_repos:
                if (
                    repo["name"] == name
                    or repo["path"] == name
                    or repo["path"].endswith(name)
                ):
                    repos.append(repo)

        return repos

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

    def transform_project(self, project):
        transformed = {}

        for key, value in project.items():
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

    def get_all_projects(self):
        try:
            logging.info(f"Retrieving projects from {self.url}/projects... ")
            projects = get(
                self.url + "/projects", self.headers, self.params, results=[]
            )
            logging.debug(json.dumps(projects, indent=2))
            projects = [self.transform_project(p) for p in projects]
            return projects
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

    def get_group_projects(self, groups):
        groups = self.get_subgroups(groups)
        all_projects = []
        for group in groups:
            try:
                logging.info(
                    f"Retrieving projects from {self.url}/{group['id']}/projects... "
                )
                projects = get(
                    f"{self.url}/groups/{group['id']}/projects",
                    self.headers,
                    self.params,
                    results=[],
                )
                logging.debug(json.dumps(projects, indent=2))
                projects = [self.transform_project(p) for p in projects]
                all_projects.extend(projects)
            except Exception as exc:
                logging.debug(exc)
                raise exc

        return all_projects

    def get_projects(self, requested_projects):
        projects = []

        for p in self.get_all_projects():
            for name in requested_projects:
                if p["name"] == name or p["path"] == name or p["path"].endswith(name):
                    projects.append(p)

        return projects

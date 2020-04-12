import json
import logging
import os
from .git import Git
from .utils import paginated_requests as get

if os.name == "posix":
    from .color import ansi_color as color
else:
    from .color import win_color as color


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

    def get_last_failed_job(self, repo):
        url = f"{self.url}/projects/{repo['id']}/jobs"

        logging.info(f"Retrieving jobs for {repo['name']} from {url}...")
        jobs = get(url, self.headers, self.params, results=[],)

        failed_jobs = [job for job in jobs if job["status"] == "failed"]
        failed_jobs = sorted(failed_jobs, reverse=True, key=lambda k: k["created_at"])

        logging.debug(json.dumps(failed_jobs, indent=2))
        logging.info(
            f"Retrieving logs for {failed_jobs[0]['id']} "
            + f"in {repo['name']} from {failed_jobs[0]['created_at']}."
        )

        last_failed_job = get(
            f"{url}/{failed_jobs[0]['id']}/trace",
            self.headers,
            self.params,
            results=[],
        )

        last_failed_job.insert(
            0,
            f"{color.fg.yellow}JOB {color.fg.cyan}{failed_jobs[0]['id']} "
            + f"{color.fg.yellow}IN {color.fg.cyan}{repo['name'].upper()} "
            + f"{color.fg.yellow}FROM {color.fg.cyan}{failed_jobs[0]['created_at']}"
            + f"{color.reset}\n",
        )

        return last_failed_job

    def get_last_failed_jobs(self, repos):
        output = []

        for repo in repos:
            last_failed_job = self.get_last_failed_job(repo)
            output.extend(last_failed_job)

        return output

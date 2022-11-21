import os
import logging
import re
from pathlib import Path
from .utils import is_git_repo, run_cmd
from concurrent.futures import ThreadPoolExecutor, as_completed

if os.name == "posix":
    from .color import ansi_color as color
else:
    from .color import win_color as color


class Git:
    def __init__(self, destination):
        self.destination = destination

    def status(self, repo):
        path = Path(self.destination + "/" + repo["name"])
        if path.exists():
            path = str(path)
            cmd = ["git", "-C", path, "status", "-s"]
            retcode, stdout, stderr = run_cmd(cmd)
            if retcode == 0 and stdout:
                return f"{color.fg.yellow}MODIFIED{color.fg.cyan} {path}...{color.reset}\n{stdout}"
            elif stderr:
                logging.error(f"{path}: SOMETHING WENT AWRY...\n{stderr}")
            elif logging.INFO:
                logging.info(f"{path}: Nothing to commit.")
        else:
            logging.warn(f"{path}: Doesn't exist.")

    def pull(self, path):
        path = str(Path(path))
        cmd = ["git", "-C", path, "pull"]
        retcode, stdout, stderr = run_cmd(cmd)

        if retcode != 0:
            logging.error(f"{color.fg.red}PULLING {path}...{color.reset}\n{stderr}")
        else:
            if re.search("up.to.date", stdout, re.IGNORECASE) or stdout.endswith(
                "Fetching origin"
            ):
                logging.info(f"{path}: Up to date")
            elif "no such ref was fetched" in stderr:
                logging.info(f"{path}: Empty repo")
            elif "Updating" in stdout:
                return f"{color.fg.yellow}UPDATING {color.fg.cyan}{path}...{color.reset}\n{stdout}"
            else:
                return f"{color.fg.yellow}FETCHING {color.fg.cyan}{path}...{color.reset}\n{stdout}"

    def clone(self, path, url):
        path = str(Path(path))
        os.makedirs(path, exist_ok=True)
        logging.info(f"Cloning {url} to {path}...")

        cmd = ["git", "clone", url, path]
        retcode, stdout, stderr = run_cmd(cmd)

        if retcode != 0:
            logging.error(
                f"{color.fg.red}Cloning {url} to {path}...{color.reset}\n{stderr}"
            )
        else:
            return f"{color.fg.yellow}CLONED {color.fg.cyan}{path}{color.reset}"

    def clone_or_pull(self, repo):
        path = str(Path(repo["name"]))
        url = repo["url"]

        fullpath = self.destination + "/" + path

        if is_git_repo(fullpath):
            return self.pull(fullpath)

        return self.clone(fullpath, url)

    def batch_run(self, method, repos):
        output = []

        if repos:
            with ThreadPoolExecutor(max_workers=len(repos)) as executor:
                future_job = {executor.submit(method, repo): repo for repo in repos}
                for future in as_completed(future_job):
                    try:
                        result = future.result()
                    except ValueError as error:
                        logging.error(error)
                    else:
                        if result:
                            output.append(result)

        return output

import os
import logging
import requests
import subprocess
import sys
from configparser import ConfigParser, ParsingError

if os.name == "posix":
    from .color import ansi_color as color
else:
    from .color import win_color as color


def chkfile(path):
    if os.path.isfile(os.path.expanduser(path)):
        return os.path.abspath(os.path.expanduser(path))

    raise FileNotFoundError(f"{path} is not a file.")


def chkdir(path):
    if os.path.isdir(os.path.expanduser(path)):
        return os.path.abspath(os.path.expanduser(path))

    raise FileNotFoundError(f"{path} is not a directory.")


def mklog(verbosity):
    if verbosity > 1:
        loglevel = logging.DEBUG
        logformat = "%(asctime)s %(threadName)s %(levelname)s %(message)s"
    elif verbosity == 1:
        loglevel = logging.INFO
        logformat = f"{color.fg.yellow}%(levelname)s {color.reset}%(message)s"
    else:
        loglevel = logging.WARNING
        logformat = f"{color.fg.yellow}%(levelname)s {color.reset}%(message)s"

    logging.basicConfig(
        # filename='',
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
        level=loglevel,
        stream=sys.stdout,
    )


def get_config(path, forge):
    try:
        config = ConfigParser()
        config.read(path)
        forge = config[forge]
    except Exception as error:
        logging.error(error)
        raise ParsingError(f"Failed to retrieve configuration from {path}.")

    forge["destination"] = chkdir(forge["destination"])

    if forge["token"]:
        logging.info(f"Found configuration at {path}.")
        return forge

    raise ParsingError(f"Failed to retrieve configuration from {path}.")


def is_git_repo(path):
    git_subpaths = ["info", "objects", "refs", "HEAD"]

    for subpath in git_subpaths:
        if os.path.exists(f"{path}/.git/{subpath}"):
            continue
        return False

    return True


def run_cmd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = proc.communicate()

    return (
        proc.returncode,
        stdout.decode("utf-8").rstrip(),
        stderr.decode("utf-8").rstrip(),
    )


def paginated_requests(url, headers, params, results=[]):
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.ok:
            results.extend(response.json())
            if "next" in response.links:
                url = response.links["next"]["url"]
                return paginated_requests(url, headers, params={}, results=results)
            return results
        raise AssertionError(response.reason)
    except Exception as exc:
        logging.debug(exc)
        raise exc

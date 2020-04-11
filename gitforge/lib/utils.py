import os
import logging
import requests
import subprocess
import sys
from configparser import ConfigParser, ParsingError
from chopt import chopt
from subprocess import call

if os.name == "posix":
    from .color import ansi_color as color
else:
    from .color import win_color as color


def chkdir(path):
    try:
        path = os.path.expanduser(path)
        os.makedirs(path, exist_ok=True)
        return path
    except Exception as exc:
        raise exc


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


def args_vs_config(args, config):
    if args.destination:
        destination = args.destination
    else:
        destination = config["destination"]

    if args.token:
        token = args.token
    else:
        token = config["token"]

    logging.debug(f"TOKEN: {token}, DESTINATION: {destination}")

    return token, destination


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


def choose_repo(repos):
    paths = [p["path"] for p in repos]
    chosen = chopt(sorted(paths))
    call("clear" if os.name == "posix" else "cls")
    return [p for p in repos if chosen and p["path"] in chosen]


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

import json
import logging
import os
import re
import readline
import requests
import subprocess
import sys

if os.name == "posix":
    from cpager import pager
    from cpick import pick

from configparser import ConfigParser, ParsingError
from pathlib import Path
from shutil import copyfile
from subprocess import call

if os.name == "posix":
    from .color import ansi_color as color
else:
    from .color import win_color as color


def chkdir(path):
    try:
        logging.debug(f"Checking if {path} exists...")
        path = os.path.normpath(os.path.expanduser(os.path.expandvars(path)))
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

    destination = chkdir(destination)

    if args.token:
        token = args.token
    else:
        token = config["token"]

    logging.debug(f"TOKEN: {token}, DESTINATION: {destination}")

    return token, destination


def get_config(forge):
    og = f"{Path(__file__).parent.parent.parent}/example.cfg"
    path = f"{os.path.expanduser('~/.gitforge.cfg')}"

    if not os.path.exists(path):
        if not os.path.exists(og):
            raise FileNotFoundError(og)
        logging.debug(f"Copying {og} to {path}...")
        copyfile(og, path)

    logging.debug(f"Looking for configuration at {path}...")

    try:
        config = ConfigParser()
        config.read(path)
    except Exception as error:
        logging.error(error)
        raise ParsingError(f"Failed to retrieve configuration from {path}.")

    logging.info(f"Found default configuration at {path}.")

    # https://stackoverflow.com/a/56119373/11133327
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")

    if config[forge]["destination"] == "/path/to/directory/to/store/repos":
        config[forge]["destination"] = input(
            f"{color.fg.yellow}{forge}{color.fg.cyan} Destination Directory:{color.reset} "
        )
        config[forge]["destination"] = chkdir(config[forge]["destination"])
        with open(path, "w") as configfile:
            config.write(configfile)

    if config[forge]["token"] == f"{forge.upper()}-PERSONAL-ACCESS-TOKEN":
        readline.parse_and_bind("tab: complete")
        config[forge]["token"] = input(
            f"{color.fg.yellow}{forge}{color.fg.cyan} Personal Access Token:{color.reset} "
        )
        with open(path, "w") as configfile:
            config.write(configfile)

    return config[forge]


def choose_repo(repos):
    paths = [p["path"] for p in repos]
    chosen = pick(items=sorted(paths))
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
    except json.decoder.JSONDecodeError:
        results.append(response.content.decode("utf-8"))
        return results
    except Exception as exc:
        logging.debug(exc)
        raise exc


def print_output(output):
    if output and type(output) is list:
        if re.match(".*JOB.*IN.*FROM", output[0]):
            pager(output)
        else:
            print("\n".join(output))
    elif output and type(output) is str:
        print(output)
    else:
        print("Nothing to see here!")

import os
import logging

from argparse import ArgumentParser
from subprocess import call
from chopt import chopt

from .lib.gitlab import GitLab
from .lib.utils import chkdir, chkfile, get_config, mklog


def get_args():
    parser = ArgumentParser(description="Clone or pull repos")
    parser.add_argument(
        "-C",
        "--config",
        type=chkfile,
        metavar=("PATH"),
        default=f"{os.path.expanduser('~/.config/gitforge/config')}",
        help="path to azure configuration file",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p", "--projects", metavar=("PROJECT"), nargs="+", help="gitlab project names",
    )
    group.add_argument(
        "-g", "--groups", metavar=("GROUP"), nargs="+", help="gitlab group names",
    )
    parser.add_argument(
        "-d", "--destination", type=chkdir, required=False, help="destination path",
    )
    parser.add_argument(
        "-t", "--token", required=False, help="gitlab personal access token",
    )
    parser.add_argument(
        "-P",
        "--protocol",
        metavar=("SSH/HTTP"),
        default="ssh",
        help="protocol to use - ssh or http",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="choose projects interactively"
    )
    parser.add_argument(
        "-r",
        "--run",
        metavar=("GIT COMMAND"),
        default="sync",
        help="git command to run",
    )
    parser.add_argument("-v", action="count", default=0, help="increase verbosity")
    return parser.parse_args()


def main():
    args = get_args()
    mklog(args.v)
    config = get_config(args.config, "gitlab")

    if args.destination:
        destination = args.destination
    else:
        destination = config["destination"]

    if args.token:
        token = args.token
    else:
        token = config["token"]

    if args.protocol not in ["ssh", "http"]:
        raise ValueError("Invalid protocol specified: {args.protocol}")

    logging.debug(
        f"\nTOKEN: {token}\nDESTINATION: {destination}\nPROTOCOL: {args.protocol}"
    )

    gitlab = GitLab(token, destination, args.protocol)

    if args.projects:
        projects = gitlab.get_projects(args.projects)
    elif args.groups:
        projects = gitlab.get_group_projects(args.groups)
    else:
        projects = gitlab.get_all_projects()

    if projects:
        if args.interactive:
            paths = [p["path"] for p in projects]
            chosen = chopt(paths)
            projects = [p for p in projects if p["path"] in chosen]
            call("clear" if os.name == "posix" else "cls")

        if args.run == "sync":
            output = gitlab.batch_run(gitlab.clone_or_pull, projects)
        elif args.run == "status":
            output = gitlab.batch_run(gitlab.status, projects)
        else:
            output = [f"Invalid command: {args.command}"]

        if output:
            print("\n".join(output))
    else:
        print("Nothing to see here.")


if __name__ == "__main__":
    main()

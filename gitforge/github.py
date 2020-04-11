import os
import logging

from argparse import ArgumentParser
from subprocess import call
from chopt import chopt

from .lib.github import GitHub
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
        "-r", "--repos", metavar=("REPO"), nargs="+", help="github repo names",
    )
    parser.add_argument(
        "-d", "--destination", type=chkdir, required=False, help="destination path",
    )
    parser.add_argument(
        "-t", "--token", required=False, help="github personal access token",
    )
    parser.add_argument(
        "-P",
        "--protocol",
        metavar=("SSH/HTTP"),
        default="ssh",
        help="protocol to use - ssh or http",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="choose repos interactively"
    )
    parser.add_argument(
        "-c",
        "--command",
        metavar=("GIT COMMAND"),
        default="sync",
        help="git command to run",
    )
    parser.add_argument("-v", action="count", default=0, help="increase verbosity")
    return parser.parse_args()


def main():
    args = get_args()
    mklog(args.v)
    config = get_config(args.config, "github")

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

    github = GitHub(token, destination, args.protocol)

    if args.repos:
        repos = github.get_repos(args.repos)
    else:
        repos = github.get_all_repos()

    if repos:
        if args.interactive:
            paths = [r["path"] for r in repos]
            chosen = chopt(paths)
            repos = [r for r in repos if r["path"] in chosen]
            call("clear" if os.name == "posix" else "cls")

        if args.command == "sync":
            output = github.batch_run(github.clone_or_pull, repos)
        elif args.command == "status":
            output = github.batch_run(github.status, repos)
        else:
            output = [f"Invalid command: {args.command}"]

        if output:
            print("\n".join(output))
    else:
        print("Nothing to see here.")


if __name__ == "__main__":
    main()

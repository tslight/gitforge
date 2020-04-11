import os
import logging

from subprocess import call
from chopt import chopt

from .lib.github import GitHub
from .lib.utils import get_config, mklog
from .lib.args import get_args


def main():
    args = get_args("GitHub").parse_args()
    mklog(args.verbosity)
    config = get_config(f"{os.path.expanduser('~/.config/gitforge/config')}", "github")

    if args.destination:
        destination = args.destination
    else:
        destination = config["destination"]

    if args.token:
        token = args.token
    else:
        token = config["token"]

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
            chosen = chopt(sorted(paths))
            if chosen:
                repos = [r for r in repos if r["path"] in chosen]
            else:
                return
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

import os
import logging

from subprocess import call
from chopt import chopt

from .lib.gitlab import GitLab
from .lib.utils import args_vs_config, get_config, mklog
from .lib.args import get_args


def main():
    args = get_args("GitLab")
    args.add_argument(
        "-g", "--groups", metavar=("GROUP"), nargs="+", help="gitlab group names",
    )
    args = args.parse_args()
    mklog(args.verbosity)
    config = get_config(os.path.expanduser("~/.config/gitforge/config"), "gitlab")
    repos = []
    token, destination = args_vs_config(args, config)
    gitlab = GitLab(token, destination, args.protocol)

    if not args.repos and not args.groups:
        repos.extend(gitlab.get_all_repos())
    else:
        if args.repos:
            repos.extend(gitlab.get_repos(args.repos))
        if args.groups:
            repos.extend(gitlab.get_group_repos(args.groups))

    if repos:
        if args.interactive:
            paths = [p["path"] for p in repos]
            chosen = chopt(sorted(paths))
            if chosen:
                repos = [p for p in repos if p["path"] in chosen]
            else:
                return
            call("clear" if os.name == "posix" else "cls")

        if args.command == "sync":
            output = gitlab.batch_run(gitlab.clone_or_pull, repos)
        elif args.command == "status":
            output = gitlab.batch_run(gitlab.status, repos)
        else:
            output = [f"Invalid command: {args.command}"]

        if output:
            print("\n".join(output))
    else:
        print("Nothing to see here.")


if __name__ == "__main__":
    main()

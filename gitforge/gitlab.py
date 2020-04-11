import os
import logging


from .lib.gitlab import GitLab
from .lib.utils import args_vs_config, choose_repo, get_config, mklog
from .lib.args import get_args


def main():
    args = get_args("GitLab")
    args.add_argument(
        "-g", "--groups", metavar=("GROUP"), nargs="+", help="gitlab group names",
    )
    args = args.parse_args()
    mklog(args.verbosity)
    config = get_config(os.path.expanduser("~/.config/gitforge/config"), "gitlab")
    token, destination = args_vs_config(args, config)
    gitlab = GitLab(token, destination, args.protocol)
    repos = []

    if not args.repos and not args.groups:
        repos.extend(gitlab.get_all_repos())
    else:
        if args.repos:
            repos.extend(gitlab.get_repos(args.repos))
        if args.groups:
            repos.extend(gitlab.get_group_repos(args.groups))

    if args.interactive:
        repos = choose_repo(repos)

    if repos:
        if args.command == "sync":
            output = gitlab.batch_run(gitlab.clone_or_pull, repos)
        elif args.command == "status":
            output = gitlab.batch_run(gitlab.status, repos)

        if output:
            print("\n".join(output))


if __name__ == "__main__":
    main()

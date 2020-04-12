from .lib.gitlab import GitLab
from .lib.utils import args_vs_config, choose_repo, get_config, mklog
from .lib.args import get_args


def get_repos(args, gitlab):
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

    return repos


def main():
    args = get_args("GitLab")
    args.add_argument("-g", "--groups", nargs="+", help="gitlab group names")
    args = args.parse_args()
    mklog(args.verbosity)
    config = get_config("GitLab")
    token, destination = args_vs_config(args, config)
    gitlab = GitLab(token, destination, args.protocol)

    if args.command == "sync":
        output = gitlab.batch_run(gitlab.clone_or_pull, get_repos(args, gitlab))
    elif args.command == "status":
        output = gitlab.batch_run(gitlab.status, get_repos(args, gitlab))
    elif args.command == "jobs":
        output = gitlab.get_last_failed_jobs(get_repos(args, gitlab))
    elif args.command == "schedules":
        output = gitlab.get_pipeline_schedules(get_repos(args, gitlab))
    elif args.command == "members":
        if args.groups:
            groups = gitlab.get_groups(args.groups)
            output = gitlab.get_members(groups, "groups")
        else:
            output = gitlab.get_members(get_repos(args, gitlab))

    if type(output) is list:
        print("\n".join(output))
    else:
        print(output)


if __name__ == "__main__":
    main()

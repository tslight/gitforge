from .lib.gitlab import GitLab
from .lib.utils import args_vs_config, choose_repo, get_config, mklog, print_output
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


def get_members(args, gitlab):
    if args.groups:
        groups = gitlab.get_groups(args.groups)
        return gitlab.get_members(groups, "groups")

    return gitlab.get_members(get_repos(args, gitlab))


def main():
    args = get_args("GitLab")
    args.add_argument("-g", "--groups", nargs="+", help="gitlab group names")
    args = args.parse_args()
    mklog(args.verbosity)
    config = get_config("GitLab")
    token, destination = args_vs_config(args, config)
    gitlab = GitLab(token, destination, args.protocol)

    command_actions = {
        "sync": lambda: gitlab.batch_run(gitlab.clone_or_pull, get_repos(args, gitlab)),
        "status": lambda: gitlab.batch_run(gitlab.status, get_repos(args, gitlab)),
        "jobs": lambda: gitlab.get_last_failed_jobs(get_repos(args, gitlab)),
        "schedules": lambda: gitlab.get_pipeline_schedules(get_repos(args, gitlab)),
        "members": lambda: get_members(args, gitlab),
    }

    output = command_actions[args.command]()

    print_output(output)


if __name__ == "__main__":
    main()

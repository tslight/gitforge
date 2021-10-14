from .lib.github import GitHub
from .lib.utils import choose_repo, args_vs_config, get_config, mklog, print_output
from .lib.args import get_args


def main():
    args = get_args("GitHub").parse_args()
    mklog(args.verbosity)
    config = get_config("GitHub")
    token, destination = args_vs_config(args, config)
    github = GitHub(token, destination, args.protocol, args.affiliation)
    output = []

    if args.repos:
        repos = github.get_repos(args.repos)
    else:
        repos = github.get_all_repos()

    if args.interactive:
        repos = choose_repo(repos)

    if repos:
        if args.command == "sync":
            output = github.batch_run(github.clone_or_pull, repos)
        elif args.command == "status":
            output = github.batch_run(github.status, repos)

    print_output(output)


if __name__ == "__main__":
    main()

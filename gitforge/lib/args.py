from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from operator import attrgetter
from .utils import chkdir


class SortingHelpFormatter(ArgumentDefaultsHelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)


def get_args(forge):
    parser = ArgumentParser(
        description=f"CLI {forge} API Client", formatter_class=SortingHelpFormatter,
    )

    if forge == "GitHub":
        parser.add_argument(
            "command",
            choices=["sync", "status"],
            nargs="?",
            default="sync",
            help="command to run",
        )
        parser.add_argument(
            "-a",
            "--affiliation",
            choices=["owner","collaborator","organization_member"],
            default=["owner"],
            nargs="+",
            help="repository access level",
        )
    elif forge == "GitLab":
        parser.add_argument(
            "command",
            choices=["sync", "status", "jobs", "schedules", "members"],
            nargs="?",
            default="sync",
            help="command to run",
        )

    parser.add_argument(
        "-d", "--destination", type=chkdir, required=False, help="destination path",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="choose repos interactively"
    )
    parser.add_argument(
        "-p",
        "--protocol",
        choices=["ssh", "http"],
        default="ssh",
        help="protocol to use",
    )
    parser.add_argument(
        "-r", "--repos", nargs="+", help=f"{forge} repo names",
    )
    parser.add_argument(
        "-t", "--token", required=False, help=f"{forge} personal access token",
    )
    parser.add_argument(
        "-v", "--verbosity", action="count", default=0, help="increase verbosity",
    )

    return parser

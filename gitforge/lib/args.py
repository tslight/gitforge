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
    parser.add_argument(
        "-r", "--repos", metavar=("REPO"), nargs="+", help=f"{forge} repo names",
    )
    parser.add_argument(
        "-d", "--destination", type=chkdir, required=False, help="destination path",
    )
    parser.add_argument(
        "-t", "--token", required=False, help=f"{forge} personal access token",
    )
    parser.add_argument(
        "-p",
        "--protocol",
        choices=["ssh", "http"],
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
        choices=["sync", "status"],
        metavar=("COMMAND"),
        default="sync",
        help="command to run - sync or status",
    )
    parser.add_argument(
        "-v", "--verbosity", action="count", default=0, help="increase verbosity",
    )
    return parser

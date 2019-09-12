from nota import __version__
import argparse
import os
import sys


from appdirs import AppDirs
from enum import EnumMeta, IntEnum

_homeDirectory = AppDirs("nota", "nota").user_config_dir

__author__ = "Robert Taylor"
__copyright__ = "Robert Taylor"
__license__ = "MIT"


class NoteType(IntEnum):
    Defect = 1
    Bug = 2
    Story = 3
    Feature = 4


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="A scaffolding program for developer notes")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="nota {ver}".format(ver=__version__))
    parser.add_argument(
        dest="name",
        help="name of new note",
        metavar="<name>")
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        help="configuration file location",
        default=os.path.join(_homeDirectory, "config.json"))
    parser.add_argument(
        "-t",
        "--template",
        dest="template",
        help="custom template file location")
    parser.add_argument(
        "-i",
        "--identifier",
        dest="id",
        help="custom note identifier")
    parser.add_argument(
        "--directories",
        dest="dirs",
        help="additional directories to create",
        action="append",
        nargs="+")
    parser.add_argument(
        "--filename",
        dest="file",
        help="custom note filename")
    parser.add_argument(
        "-l",
        "--list",
        dest="list",
        help="lists all notes available",
        action="store_true")
    parser.add_argument(
        "-r",
        "--root",
        dest="root",
        help="root directory for all notes")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-d",
        "--defect",
        dest="type",
        help="create a defect note",
        action="store_const",
        const=NoteType.Defect)
    group.add_argument(
        "-b",
        "--bug",
        dest="type",
        help="create a bug note",
        action="store_const",
        const=NoteType.Bug)
    group.add_argument(
        "-s",
        "--story",
        dest="type",
        help="create a story note",
        action="store_const",
        const=NoteType.Story)
    group.add_argument(
        "-f",
        "--feature",
        dest="type",
        help="create a feature note",
        action="store_const",
        const=NoteType.Feature)
    group.add_argument(
        "-o",
        "--option",
        dest="custom",
        help="create a custom note")
    return parser.parse_args(args)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    print(args)
    print(__file__)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

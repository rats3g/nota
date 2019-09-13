from nota import __version__
import argparse
import collections
import json
import os
import sys


from appdirs import AppDirs
from enum import Enum
from os import path
from shutil import copyfile

_homeDirectory = AppDirs("nota", "nota").user_config_dir

__author__ = "Robert Taylor"
__copyright__ = "Robert Taylor"
__license__ = "MIT"


class NoteType(Enum):
    Defect = "defect"
    Bug = "bug"
    Story = "story"
    Feature = "feature"


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
        help="configuration file location")
    parser.add_argument(
        "-t",
        "--template",
        dest="template",
        help="custom template file location")
    parser.add_argument(
        "-i",
        "--identifier",
        dest="identifier",
        help="custom note identifier")
    parser.add_argument(
        "--directories",
        dest="dirs",
        help="additional directories to create",
        action="append",
        nargs="+")
    parser.add_argument(
        "--filename",
        dest="filename",
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
        dest="note_type",
        help="create a defect note",
        action="store_const",
        const=NoteType.Defect)
    group.add_argument(
        "-b",
        "--bug",
        dest="note_type",
        help="create a bug note",
        action="store_const",
        const=NoteType.Bug)
    group.add_argument(
        "-s",
        "--story",
        dest="note_type",
        help="create a story note",
        action="store_const",
        const=NoteType.Story)
    group.add_argument(
        "-f",
        "--feature",
        dest="note_type",
        help="create a feature note",
        action="store_const",
        const=NoteType.Feature)
    group.add_argument(
        "-o",
        "--option",
        dest="custom",
        help="create a custom note")
    return parser.parse_args(args)


def config_check(config):
    if (config is None):
        # Use default config location
        config = path.join(_homeDirectory, "config.json")
        if (not path.exists(config)):
            # Copy template if config doesn't exist
            print(
                f"Configuration file not found! Copying templates to: {_homeDirectory}")

            os.makedirs(_homeDirectory, exist_ok=True)

            template_directory = path.join(path.dirname(__file__), "templates")
            for file in os.listdir(template_directory):
                if (path.isfile(path.join(template_directory, file))):
                    copyfile(path.join(template_directory, file),
                             path.join(_homeDirectory, file))

            data = {
                "defect": {
                    "template": f"{_homeDirectory}/defect.md",
                    "directories": [
                        "logs"
                    ],
                    "filename": "defect_$id.md"
                }
            }

            with open(config, "w+") as config_file:
                json.dump(data, config_file, indent=4)

    else:
        # Config parameter set
        if (not path.exists(config)):
            print(f"Configuration file not found: {config}")
            exit(-1)

    return config


def option_check(option, note_type):
    if (option is None and note_type is not None):
        option = note_type.value

    return option


def template_check(config, option, template):
    if (template is not None):
        return template

    if (option in config and "template" in config[option]):
        return config[option]["template"]

    if ("default" in config and "template" in config["default"]):
        return config["default"]["template"]

    return path.join(_homeDirectory, f"{option}.md")


def directories_check(config, option, directories):
    if (directories is not None):
        return directories

    if (option in config and "directories" in config[option]):
        return config[option]["directories"]

    if ("default" in config and "template" in config["default"]):
        return config["default"]["directories"]

    return []


def filename_check(config, option, filename):
    if (filename is not None):
        return filename

    if (option in config and "filename" in config[option]):
        return config[option]["filename"]

    if ("default" in config and "filename" in config["default"]):
        return config["default"]["filename"]

    return "$option_$id"


def root_check(config, root):
    if (root is not None):
        return root

    if ("root" in config):
        return config["root"]

    return os.getcwd()


def id_check(identifier, name):
    if (identifier is None):
        return name

    return identifier


def inject(name, identifier, option, value):
    value = value.replace("$name", name)
    value = value.replace("$id", identifier)
    value = value.replace("$option", option)

    value = path.expanduser(value)
    value = path.expandvars(value)

    return value


def flatten(l):
    for el in l:
        if isinstance(el, collections.Sequence) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)

    config_path = config_check(args.config)
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

        option = option_check(args.custom, args.note_type)
        template = template_check(config, option, args.template)
        directories = flatten(directories_check(config, option, args.dirs))
        filename = filename_check(config, option, args.filename)
        root = root_check(config, args.root)
        identifier = id_check(args.identifier, args.name)

        template = inject(args.name, identifier, option, template)
        filename = inject(args.name, identifier, option, filename)
        directories = [inject(args.name, identifier, option, item)
                       for item in directories]

        if (not path.exists(template)):
            print(f"Template file not found: {template}")
            exit(-1)

        if (not path.isfile(template)):
            print(f"Template must be a file: {template}")
            exit(-1)

        if (not path.exists(root)):
            print(f"Root directory not found: {root}")
            exit(-1)

        if (not path.isdir(root)):
            print(f"Root must be a directory: {root}")
            exit(-1)

        os.makedirs(path.join(root, option, identifier), exist_ok=True)
        for directory in directories:
            os.makedirs(path.join(root, option, identifier,
                                  directory), exist_ok=True)

        with open(template, "r") as template_file:
            with open(path.join(root, option, identifier, filename), "w+") as new_file:
                contents = template_file.read()
                contents = inject(args.name, identifier, option, contents)
                new_file.write(contents)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

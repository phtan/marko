#! -*- coding: utf-8 -*-
"""
Command line interfaces
"""
from __future__ import print_function
import sys
import importlib
import marko
import codecs
from argparse import ArgumentParser


def import_class(import_string):
    try:
        module, classname = import_string.rsplit(".", 1)
        cls = getattr(importlib.import_module(module), classname)
    except ValueError:
        sys.exit("Please supply module.classname.")
    except ImportError:
        sys.exit("Cannot import module %s" % module)
    except AttributeError:
        sys.exit("Cannot find class {} in module {}".format(classname, module))
    else:
        return cls


def parse(args):
    parser = ArgumentParser(prog="marko")

    parser.add_argument("-v", "--version", action="version", version=marko.__version__)
    parser.add_argument(
        "-p",
        "--parser",
        type=import_class,
        default="marko.Parser",
        help="Specify another parser class",
    )
    parser.add_argument(
        "-r",
        "--renderer",
        type=import_class,
        default="marko.HTMLRenderer",
        help="Specify another renderer class",
    )
    parser.add_argument(
        "-e",
        "--extension",
        action="append",
        default=[],
        metavar="EXTENSTION",
        help="Specify the import name of extension, can be given multiple times"
    )
    parser.add_argument("-o", "--output", help="Ouput to a file")
    parser.add_argument(
        "document",
        nargs="?",
        help="The document to convert, will use stdin if not given.",
    )
    return parser.parse_args(args)


def main():
    namespace = parse(sys.argv[1:])
    if namespace.document:
        with codecs.open(namespace.document, encoding="utf-8") as f:
            content = f.read()
    else:
        keystroke = "Ctrl+Z" if sys.platform.startswith("win") else "Ctrl+D"
        print(
            "Type in the markdown content to be converted. End with {}".format(
                keystroke
            ),
            file=sys.stderr
        )
        content = sys.stdin.read()
    markdown = marko.Markdown(
        namespace.parser,
        namespace.renderer,
        extensions=namespace.extension
    )
    result = markdown(content)
    if namespace.output:
        with codecs.open(namespace.output, "w", encoding="utf-8") as f:
            f.write(result)
    else:
        print(result)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import argparse
import sys
import logging
import logging.config
from yaml4parms import read


log = logging.getLogger(__name__)


def get_arg_parser():
    """ Defines the arguments to this script by using Python's [argparse](https://docs.python.org/3/library/argparse.html)
    """
    parser = argparse.ArgumentParser(description='exposes yaml structured parameters information',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-l', '--logconf',
        type=str,
        action='store',
        help='location of the logging config (yml) to use',
    )

    parser.add_argument(
        '-p', '--prefix',
        type=str,
        metavar='PREFIX',
        action='store',
        help='The comment-prefix to recognise yml structure',
        required=False,
        default='#= ',
    )

    parser.add_argument(
        'format',
        nargs='?',
        type=str,
        metavar='FORMAT',
        action='store',
        help='The format in which to produce the parameters-description',
        default='yml',
    )

    parser.add_argument(
        'input',
        type=str,
        nargs='?',
        metavar='FILE',
        action='store',
        help='The input file to parse',
        default='parameters.tsv',
    )
    return parser


def enable_logging(args: argparse.Namespace):
    if args.logconf is None:
        return
    import yaml   # conditional dependency -- we only need this (for now) when logconf needs to be read
    with open(args.logconf, 'r') as yml_logconf:
        logging.config.dictConfig(yaml.load(yml_logconf, Loader=yaml.SafeLoader))
    log.info(f"Logging enabled according to config in {args.logconf}")


def main():
    """ The main entry point to this module.
    """
    args = get_arg_parser().parse_args()
    enable_logging(args)

    log.info("The args passed to %s are: %s." % (sys.argv[0], args))
    log.debug("Some Logging")

    pd = read(args.input, args.prefix)
    print(pd.format(args.format))


if __name__ == '__main__':
    main()

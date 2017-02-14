#!/usr/bin/env python3

import argparse
import logging

from .automaton import Automaton
from .version import __version__

def main():
    description = ('Generate images for the single 1 histories of Stephen Wolfram\'s '
                   'elementary cellular automata.')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('image',
                        help='path to the output image (PNG format)')
    parser.add_argument('-n', '--rows', type=int, default=256,
                        help='number of rows to generate; default is 256')
    parser.add_argument('-r', '--rule', nargs='?', type=int, default=30,
                        help='Wolfram code of the rule (between 0 and 255); default is 30')
    parser.add_argument('-s', '--block-size', type=int, default=1,
                        help='the size in pixels for each cell; default is 1')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--debug', action='store_true',
                        help='enable debug messages')
    args = parser.parse_args()
    path = args.image
    rows = args.rows
    rule = args.rule
    block_size = args.block_size
    debug = args.debug

    logging.basicConfig(format='[%(levelname)s] %(name)s: %(message)s')
    logger = logging.getLogger('rule30')

    try:
        automaton = Automaton(rows=rows, rule=rule)
        image = automaton.image(block_size=block_size)
        image.save(path, format='png')
    except Exception as e:
        logger.error('%s: %s', type(e).__name__, e)
        if debug:
            raise

if __name__ == '__main__':
    main()

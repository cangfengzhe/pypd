#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
query
"""

# ---------
# Change Logs:
#
# ---------

__author__ = 'Li Pidong'
__email__ = 'lipidong@126.com'
__version__ = '0.0.1'
__status__ = 'Dev'

import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import argparse
import logging
import pandas as pd

from dfply import *
import ipdb

def log(file_name, logger_name='lipidong', quite=False):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s",
                                 datefmt="%Y-%m-%d %H:%M:%S")
    handler = logging.FileHandler(file_name)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    if not quite:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger


class Query(object):

    """query """

    def __init__(self, args):
        """TODO: to be defined1.

        :file_path: TODO
        :query: TODO
        :pipe: TODO
        :output: TODO
        :noheader: TODO

        """
        self._file_path = args.file_path
        self._query = args.query
        self._pipe = args.pipe
        self_output = args.output
        self._pr = args.pr
        self._input_args = eval(args.input_args)

        self.run()

    def run(self):
        """TODO: Docstring for run.
        :returns: TODO

        """

        df = pd.read_table(self._file_path, **self._input_args)
        df = df.query(self._query)

        if self._pipe:
            pipe_str = "df >> " + self._pipe
            # ipdb.set_trace()
            # print(pipe_str)
            # exec(pipe_str)
            df = eval(pipe_str)
            # print(df)
        if self._pr:
            print(df.head())
        else:
            df.to_csv(self._output, index=False, sep='\t')

def get_args():
    parser = argparse.ArgumentParser(prog='query')
    parser.add_argument('--file_path', type=str,
                        help='输入文件名，文件必须有列名')
    parser.add_argument('--query', help='')
    parser.add_argument('--pipe', help='')
    parser.add_argument('--output', help='')
    parser.add_argument('--pr', help='', action="store_true")
    parser.add_argument('--input_args', help='')
    parser.add_argument('--log', help='log file, default=.log', default='.log')
    parser.add_argument("--quite", help="increase output verbosity",
                         action="store_true")
    if len(sys.argv) == 1:
        parser.print_help()
        exit()
    return parser.parse_args()

def main():
    args = get_args()
    Query(args)

if __name__ == '__main__':
    main()

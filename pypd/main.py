#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
desc
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
from join import Join

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


def proc_join(args):
    file_list = args.file_list
    how = args.how
    on = args.on
    show = args.show
    suffixes = args.suffixes
    output = args.output
    Join(file_list, how, on, show, suffixes, output)

def get_args():

    parser = argparse.ArgumentParser(prog='desc')
    subparsers = parser.add_subparsers()
    parent_parser = argparse.ArgumentParser(add_help=False)

    parser_cmd = subparsers.add_parser('cmd', parents=[parent_parser], help="Detect trinucleotide repeats from a BAM file")
    parser_query = subparsers.add_parser('query', parents=[parent_parser], help="Detect trinucleotide repeats from a BAM file")

    parser_join = subparsers.add_parser('join', parents=[parent_parser], help="Detect trinucleotide repeats from a BAM file")
    parser_join.add_argument('--file_list', metavar='file list', type=str, nargs='+',
                      help='输入文件名，文件必须有列名')
    parser_join.add_argument('--how', help='how to join[left, right, inner, outer]', default='outer',
                   choices=['left', 'right', 'inner', 'outer'])
    parser_join.add_argument("--on", help="所有文件共有的列，根据该列信息合并表",
                   nargs='+')
    parser_join.add_argument("--show", help="需要显示的列",
                   nargs='+')
    parser_join.add_argument("--suffixes", help="相同的列名添加后缀",
                   nargs='+')
    parser_join.add_argument("--output", help="输出结果")
    parser_join.set_defaults(func=proc_join)

    parser_sql = subparsers.add_parser('sql', parents=[parent_parser], help="Detect trinucleotide repeats from a BAM file")
    parser.add_argument('--log', help='log file, default=.log', default='.log')
    parser.add_argument("--quite", help="increase output verbosity",
                         action="store_true")
    if len(sys.argv) == 1:
        parser.print_help()
        exit()

    return parser.parse_args()


def main():
    args = get_args()
    # global logger
    # logger = log(log_file, quite=quite)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
根据列信息，连接多个表
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
from functools import reduce
import re
import os
import pdb

import pandas as pd


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


class Join(object):

    """Join Class,方便传值"""

    def __init__(self, file_list, how, on, show, suffixes, output):
        """初始化

        :file_list: TODO
        :how: TODO
        :on: TODO
        :show: TODO
        :basename: TODO

        """
        self._file_list = file_list
        self._how = how
        self._on = on
        self._show = show
        self._index = 0
        self._suffixes = suffixes
        self._output = output

        self.run()

    def read_table(self, file_path):
        """TODO: Docstring for read_table.

        :file_path: TODO
        :returns: TODO

        """
        pass


    def run(self):
        """run
        :returns: TODO

        """
        df_list = map(lambda x: pd.read_table(x), self._file_list)
        out_df = reduce(self.join, df_list)
        out_df.to_csv(self._output, sep='\t', index=False)

    def get_suffixes(self):
        """获取不同文件的suffix, 当不同文件有相同列名时采用suffix加以区分
        :returns: TODO

        """
        # if self._show:
            # colnames = [xx for xx in  df.columns if xx in self._show]
        if self._suffixes:
            return self._suffixes
        else:
            base_names = list(map(lambda x: re.split('[^0-9a-zA-Z]', os.path.basename(x))[0], self._file_list))
            if len(base_names) == len(set(base_names)):
                return base_names
            else:
                return list(range(1, len(self._file_list) + 1))

    def join(self, df1, df2):
        # df1 = pd.read_table(file1)
        # df2 = pd.read_table(file2)
        # name_list = map(lambda x: '_%s' % re.split('[^0-9a-zA-Z]', os.path.basename(x))[0], [file1, file2])
        # if name_list[0] == name_list[1]:
            # name_list[0] = '_%d' % self.index
            # self.index += 1
            # name_list[1] = '_%d' % self.index
        # df1.columns = ['%s_%s' % (xx, self._suffixes[self._index]) for xx in df1.columns if xx not in self._on ]
        # df2.columns = ['%s_%s' % (xx, self._suffixes[self._index]) for xx in df2.columns if xx not in self._on ]
        suffixes = self.get_suffixes()
        df = df1.merge(df2, how=self._how, on=self._on, suffixes=('_%s' % suffixes[self._index], '_%s' % suffixes[self._index+1]))

        if self._show:
            show_names = '_'.join(self._show)
            columns = [xx for xx in  df.columns if xx in show_names]
            columns = self._on + columns
            df = df[columns]

        self._index += 1
        return df


def get_args():
    parser = argparse.ArgumentParser(prog='根据列信息，连接多个表')
    parser.add_argument('--file_list', metavar='file list', type=str, nargs='+',
                                            help='输入文件名，文件必须有列名')
    parser.add_argument('--how', help='how to join[left, right, inner, outer]', default='outer',
                        choices=['left', 'right', 'inner', 'outer'])
    parser.add_argument("--on", help="所有文件共有的列，根据该列信息合并表",
                        nargs='+')
    parser.add_argument("--show", help="需要显示的列",
                         nargs='+')
    parser.add_argument("--suffixes", help="相同的列名添加后缀",
                         nargs='+')
    parser.add_argument("--output", help="输出结果")

    if len(sys.argv) == 1:
        parser.print_help()
        exit()
    return parser.parse_args()


def main():

    args = get_args()
    file_list = args.file_list
    how = args.how
    on = args.on
    show = args.show
    suffixes = args.suffixes
    output = args.output
    Join(file_list, how, on, show, suffixes, output)


if __name__ == '__main__':
    main()

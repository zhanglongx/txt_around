# python
# -*- coding: utf-8 -*-

import os, argparse
import re

class Search():
    def __init__(self, filename, around=10, max=3):

        self._filename = filename
        self._around   = around
        self._max      = max

        self._to_skip  = ['一']

        self._load_txt()

    def _load_txt(self):

        with open(self._filename, encoding='utf-8', mode='r') as f:
            self._txt = f.read()

    def _skip_common(self, str):
        if len(str) == 1 and str[0] in self._to_skip:
            return True

        return False

    def search(self, str, mode='two'):

        if len(str) == 1:
            reg = r'.{,%d}%s.{,%d}' % (self._around, str[0], self._around)
        elif len(str) == 2:
            reg = r'.{,%d}%s.{,%d}%s.{,%d}' % \
                  (self._around, str[0], self._max, str[1], self._around)
        else:
            raise ValueError('str must be less than 2')

        if self._skip_common(str) is True:
            return []

        try:
            return re.findall(reg, self._txt, flags=re.S)
        except:
            return []

def main(args):

    s = Search(filename=args.filename)

    with open('data/names.txt', encoding='utf-8', mode='r') as f:
        lines = f.readlines()

    for name in [l for l in lines if len(l) == 4 and len(l) > 2]:
        # skip first char
        res = s.search(name.strip('\n')[1:])

        if len(res) == 0:
            continue  # Non-result

        print(name + ''.join(res) + '\n')

    del s

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='search text and provide around context')
    parser.add_argument('filename', type=str, help='text to search')
    parser.add_argument('-a', '--around', default=10, type=int, nargs=1, help='display <around> chars text')
    parser.add_argument('-m', '--max',    default=3,  type=int, nargs=1, help='max chars gap in two-char mode')

    main(parser.parse_args())

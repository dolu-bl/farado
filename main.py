#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from farado.stem import Stem

def main() -> int:
    argv = sys.argv
    # TODO: use argv
    stem = Stem()
    result = stem.run()
    return result

if __name__ == '__main__':
    sys.exit(main())


#!/usr/bin/env python

from jnius import autoclass

TestIO = autoclass('hdfsio.TestIO')
TestIO.writeHDFS()
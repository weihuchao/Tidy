#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opencc import OpenCC

cc = OpenCC('t2s')
with open('/Users/weihc/卡卡西精通五遁，野原琳幸福坏了.txt', 'r', encoding='gbk') as fin, open('/Users/weihc/output.txt', 'w', encoding='utf-8') as fout:
    for line in fin:
        fout.write(cc.convert(line))

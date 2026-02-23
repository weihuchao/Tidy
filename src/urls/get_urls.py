#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


def run():
    with open("./input/base.html") as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    for li in soup.find_all("img"):
        print(li.attrs.get("src", ""))


if __name__ == '__main__':
    run()

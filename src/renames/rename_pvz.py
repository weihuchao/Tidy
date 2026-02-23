#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

folder = "/Volumes/MSData/音乐/01-专辑/PVZ"

for filename in os.listdir(folder):
    # 匹配以数字.开头的文件名
    match = re.match(r"^\d+\.(.+)", filename)
    if match:
        new_name = f"Plants vs. Zombies OST - {match.group(1)}"
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")
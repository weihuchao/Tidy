#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from mutagen import File

folder = "/Volumes/MSData/Music/01-无损源文件"

for filename in sorted(os.listdir(folder)):
    # 跳过隐藏文件
    if filename.startswith('.'):
        continue
    # 只处理常见音频文件
    if not filename.lower().endswith(('.flac', '.mp3', '.m4a', '.ogg', '.wav')):
        continue
    filepath = os.path.join(folder, filename)
    try:
        audio = File(filepath)
    except:
        print(filename)
        continue
    artist = None
    if audio:
        # 尝试多种常见标签
        for key in ['artist', 'ARTIST', 'Author', 'a']:
            value = audio.get(key)
            if value:
                artist = value[0] if isinstance(value, list) else value
                break
    if not artist:
        print(filename)

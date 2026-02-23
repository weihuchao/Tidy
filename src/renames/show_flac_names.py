#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from mutagen.flac import FLAC
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1


def get_mp3_metadata(path, name):
    try:
        audio = MP3(path)
        tags = audio.tags
        artist = tags.get('TPE1')
        title = tags.get('TIT2')
        artist_name = artist.text[0] if artist else None
        title_name = title.text[0] if title else None

        if '澤野弘之' in path and 'SawanoHiroyuki[nZk]' not in artist_name:
            artist_name = f'SawanoHiroyuki[nZk];{artist_name}'
        if artist_name == '澤野弘之':
            artist_name = 'SawanoHiroyuki[nZk]'

        return f"{artist_name} - {title_name}.mp3" if artist_name and title_name else filename
    except Exception:
        print(path, name)
        return ''


def get_flac_metadata(path, name):
    audio = FLAC(path)
    artist_name = audio.get("artist", ["Unknown Artist"])[0]
    if artist_name == "Unknown Artist":
        print(path, name)
        return ''
    title = audio.get("title", ["Unknown Title"])[0]
    if title == "Unknown Title":
        print(path, name)
        return ''
    if artist_name == '澤野弘之':
        artist_name = 'SawanoHiroyuki[nZk]'
    if '澤野弘之' in path and 'SawanoHiroyuki[nZk]' not in artist_name:
        artist_name = f'SawanoHiroyuki[nZk];{artist_name}'
    return f"{artist_name} - {title}.flac"


def run():
    name = '澤野弘之 - 機動戦士ガンダムUC　オリジナルサウンドトラック3'
    folder = f"/Volumes/MSData/音乐/02-待处理/{name}"

    for filename in sorted(os.listdir(folder)):
        if filename.startswith('.'):
            continue
        if not filename.lower().endswith(('.flac', '.mp3', '.m4a', '.ogg', '.wav')):
            continue
        path = os.path.join(folder, filename)
        new_name = ''
        if filename.lower().endswith('.mp3'):
            new_name = get_mp3_metadata(path, filename)
        if filename.lower().endswith('.flac'):
            new_name = get_flac_metadata(path, filename)
        if not new_name:
            continue
        new_name = new_name.replace("/", "-").replace(':', ';')
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        print(f"Renamed: {filename} -> {new_name}")
        os.rename(old_path, new_path)

    print()
    print(f"7z a -mx0 '{name}.7z' ./'{name}'/*")


if __name__ == '__main__':
    run()

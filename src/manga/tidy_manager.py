#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path


# 在函数执行前输出间隔符号的装饰器
def print_separator(func):
    def wrapper(*args, **kwargs):
        print('=' * 120)
        return func(*args, **kwargs)

    return wrapper


@print_separator
def move_mikan_download_files():
    target_path = os.path.join(MANGA_HOME, MANGA_NAME)
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    need_file_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm', '.ass'}

    print(f"FROM {DOWNLOAD_HOME}")
    print(f"TO   {target_path}")
    print("-" * 60)

    for root, dirs, files in os.walk(DOWNLOAD_HOME):
        if root == target_path:
            continue
        for file in sorted(files):
            if os.path.splitext(file)[1].lower() not in need_file_extensions:
                continue
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_path, file)

            if os.path.exists(target_file):
                continue
                # base, ext = os.path.splitext(file)
                # counter = 1
                # while os.path.exists(target_file):
                #     target_file = os.path.join(target_path, f"{base}_{counter}{ext}")
                #     counter += 1

            print(f"{source_file.replace(DOWNLOAD_HOME, '')}")
            print(f"-> {target_file.replace(MANGA_HOME, '')}")

            if not DRY_RUN:
                shutil.move(source_file, target_file)

            if not DRY_RUN and len([p for p in os.listdir(root) if not p.startswith('.')]) == 0:
                print(f'deleted: {root.replace(DOWNLOAD_HOME, "")}')
                shutil.rmtree(root)

    print("-" * 60)


@print_separator
def rename_download_files():
    suffixes = [
        '.mkv',
        '.mp4',
        '.ass',
        '.rmvb',
    ]
    path_list = []
    for fname in os.listdir(MANGA_PATH):
        if fname.startswith('.'):
            continue
        if not any(fname.endswith(suffix) for suffix in suffixes):
            continue
        path_list.append(MANGA_PATH / fname)

    idx = 0
    for path in sorted(path_list):
        idx += 1
        while idx in MISSING_INDEXES:
            idx += 1
        suffix = path.suffix
        new_path = MANGA_PATH / f'{idx:02d}{suffix}'
        if new_path.exists():
            continue
        old_name = str(path).replace(str(MANGA_PATH), "").strip("/")
        print(f'{old_name}')
        new_name = str(new_path).replace(str(MANGA_PATH), "").strip("/")
        print(f'{new_name}'.center(len(old_name) + len(new_name) + 4, ' '))
        print('-' * (len(old_name) + len(new_name) + 4))

        if not DRY_RUN:
            shutil.move(path, new_path)


@print_separator
def clean_cht_ass():
    ass_list = []
    for fname in os.listdir(MANGA_PATH):
        if fname.startswith('.'):
            continue
        if not fname.endswith('.ass'):
            continue
        ass_list.append(fname)

    need_clean = []
    for fname in ass_list:
        # remove *.CHT.ass and check has same name *.CHS.ass file
        if not fname.endswith('.CHT.ass'):
            continue
        chs_fname = fname.replace('.CHT.ass', '.CHS.ass')
        if chs_fname in ass_list:
            need_clean.append(fname)

    for fname in sorted(need_clean):
        print(fname)
        if not DRY_RUN:
            # remove file
            os.remove(MANGA_PATH / fname)


if __name__ == '__main__':
    DOWNLOAD_HOME = '/Users/weihc/番剧/1'

    MANGA_HOME = '/Users/weihc/番剧'
    # MANGA_HOME = '/Volumes/MSData/番剧/1 已完结'

    MANGA_NAME = 'Re：从零开始的异世界生活 第3季A'

    MANGA_PATH = Path(MANGA_HOME) / MANGA_NAME

    DRY_RUN = True
    DRY_RUN = False

    move_mikan_download_files()

    MISSING_INDEXES = [6]
    MISSING_INDEXES = []

    clean_cht_ass()
    rename_download_files()

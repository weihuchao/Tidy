#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil


def move_mikan_download_files(source_path: str, target_name: str):
    target_path = os.path.join(source_path, target_name)
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    need_file_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm', '.ass'}

    for root, dirs, files in os.walk(source_path):
        if root == target_path:
            continue
        for file in files:
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

            shutil.move(source_file, target_file)
            print(f"{source_file}")
            print(f'-> {target_file}')

            if len([p for p in os.listdir(root) if not p.startswith('.')]) == 0:
                print(f'deleted: {root}')
                shutil.rmtree(root)

    print("done.")


if __name__ == '__main__':
    move_mikan_download_files('/Users/weihc/Downloads/Mikan', '不幸职业【鉴定士】实则最强')

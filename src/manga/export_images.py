#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def run():
    # [i.id for i in book.get_items() if i.media_type == 'image/jpeg']
    epub_dir_path = '/Volumes/MSData/漫画/全职猎人（东立）'
    for file_name in sorted(os.listdir(epub_dir_path)):
        if file_name.startswith('.'):
            continue
        if not file_name.endswith('.epub'):
            continue
        print('--------')
        print(file_name)
        epub_path = os.path.join(epub_dir_path, file_name)
        output_img_dir = f'/Volumes/MSData/漫画/Export/{file_name.replace(".epub", "")}'
        os.makedirs(output_img_dir, exist_ok=True)
        book = epub.read_epub(epub_path)

        # type check: {'image/jpeg', 'application/xhtml+xml', 'application/x-dtbncx+xml', 'image/png', 'text/css'}
        # media_types = set()
        # for item in book.get_items():
        #     media_types.add(item.media_type)
        # print(file_name, '--->', media_types)

        # 还是乱序
        # img_idx = 1
        # for item in book.get_items():
        #     if not item.media_type.startswith('image/'):
        #         continue
        #     # print(item.id)
        #     ext = os.path.splitext(item.file_name)[1]
        #     new_name = f"img_{img_idx:03d}{ext}"
        #     print(new_name)
        #     with open(os.path.join(output_img_dir, new_name), 'wb') as f:
        #         f.write(item.get_content())
        #     img_idx += 1

        img_map = {}
        for item in book.items:
            # if item.get_type() != ebooklib.ITEM_IMAGE:
            if not item.media_type.startswith('image/'):
                continue
            name = item.file_name.rsplit('/')[-1]
            if name in img_map:
                # print(item)
                raise Exception('Duplicate image name')
            img_map[name] = item.get_content()

        img_idx = 1
        for spine_id, _ in book.spine:
            item = book.get_item_with_id(spine_id)
            assert item and item.get_type() == ebooklib.ITEM_DOCUMENT

            soup = BeautifulSoup(item.get_content(), 'html.parser')
            for img_tag in soup.find_all('img'):
                img_src = img_tag.get('src')
                if not img_src:
                    continue

                name = img_src.rsplit('/')[-1]
                if name not in img_map:
                    print(img_src)
                    raise Exception('Image name not found.')

                ext = os.path.splitext(name)[1]
                new_name = f"img_{img_idx:03d}{ext}"
                with open(os.path.join(output_img_dir, new_name), 'wb') as f:
                    f.write(img_map[name])
                img_idx += 1


if __name__ == '__main__':
    run()

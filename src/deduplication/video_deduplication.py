#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
在 Python 脚本中，直接指定一个文件夹，查找里面所有的视频文件（包括子文件夹内、子文件夹的子文件夹内...），按照文件名进行排序，将重名的按照顺序文件输出
发现重复文件，输出时，附带各个文件的大小
'''
from pathlib import Path
import sys
import re
from collections import defaultdict

DEFAULT_FOLDER = "/Volumes/MSData/TMP/1/3"

# 支持的视频扩展（小写）
VIDEO_EXTS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
    ".m4v", ".ts", ".m2ts", ".mpg", ".mpeg", ".3gp", ".vob", ".rmvb"
}

_def_re = re.compile(r'(\d+)|(\D+)')


def natural_key(s: str):
    """用于自然排序的 key：把数字部分作为整数比较，其它作为小写字符串比较。"""
    parts = []
    for m in _def_re.finditer(s):
        num, text = m.groups()
        if num is not None:
            parts.append((0, int(num)))
        else:
            parts.append((1, text.lower()))
    return parts


def find_videos(root: Path):
    grouped = defaultdict(list)  # basename -> list of Path
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in VIDEO_EXTS:
            base = p.stem  # 不含扩展名的文件名
            grouped[base].append(p)
    return grouped


def human_size(n: int) -> str:
    n = float(n)
    for unit in ('B', 'K', 'M', 'G', 'T', 'P'):
        if n < 1024.0 or unit == 'P':
            if unit == 'B':
                return f"{int(n)}{unit}"
            return f"{n:.1f}{unit}"
        n /= 1024.0


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_FOLDER)
    if not folder.exists() or not folder.is_dir():
        sys.exit(2)

    grouped = find_videos(folder)

    for base in sorted(grouped.keys(), key=natural_key):
        files = grouped[base]
        files_sorted = sorted(files, key=lambda p: natural_key(p.name))
        if len(files_sorted) == 1:
            continue

        print(f"\n== {base}  (共 {len(files_sorted)} 个) ==")
        for i, fp in enumerate(files_sorted, 1):
            try:
                size = fp.stat().st_size
                size_str = human_size(size)
            except Exception:
                size_str = "N/A"
            print(f"  {i:02d}. {fp} ({size_str})")


if __name__ == "__main__":
    main()

from typing import List

import re


def extract_stamps(src: str) -> List[str]:
    """
    メッセージ文字列(src)からスタンプのみを抽出する
    ex. "@BOT_stamProlog :technologist: :heart::computer:\n:ton:"
    -> ":technologist: :heart: :computer: :ton:".split()
    """
    list_stamp = []
    list_string = src.split(":")
    check = False
    for i in range(1, len(list_string) - 1):
        if check:
            check = False
            continue
        now_string = list_string[i]
        m = re.fullmatch(r"@?[0-9a-zA-Z_-]+(\.[a-zA-Z_-]){0,6}", now_string)
        if m is None:
            continue
        else:
            list_stamp.append(":" + list_string[i] + ":")
            check = True
    return list_stamp


def split_sentences(src: List[str]) -> List[List[str]]:
    """
    TODO
    スタンプ列を分ごとに分割する
    ex. ":technologist: :heart: :computer: :ton: :heart: :computer: :ton:".split()
    -> [
        ":technologist: :heart: :computer: :ton:".split(),
        ":heart: :computer: :ton:".split()
    ]
    """
    raise NotImplementedError

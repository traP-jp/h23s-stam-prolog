import re
from typing import Union


def extract_stamps(src: str) -> list[str]:
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


def split_statements(src: list[str]) -> Union[list[list[str]], str]:
    """
    スタンプ列を文ごとに分割する
    ex. ":technologist: :heart: :computer: :ton: :heart: :computer: :ton:".split()
    -> [
        ":technologist: :heart: :computer: :ton:".split(),
        ":heart: :computer: :ton:".split()
    ]
    """
    l: list[list[str]] = [[]]
    i = 0
    for s in src:
        l[i].append(s)
        if s == ":ton:" or s == ":hatena:":
            i += 1
            l.append([])
    last = l.pop()
    if last == []:
        return l
    else:
        return "構文エラー: :ton:または:hatena:で文が終わっていません"

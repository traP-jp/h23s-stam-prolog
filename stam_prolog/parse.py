from typing import List
from typing import Union


def extract_stamps(src: str) -> List[str]:
    """
    TODO
    メッセージ文字列(src)からスタンプのみを抽出する
    ex. "@BOT_stamProlog :technologist: :heart::computer:\n:ton:"
    -> ":technologist: :heart: :computer: :ton:".split()
    """
    raise NotImplementedError


def split_sentences(src: List[str]) -> Union[List[List[str]], str]:
    """
    TODO
    スタンプ列を分ごとに分割する ←文ごと?
    ex. ":technologist: :heart: :computer: :ton: :heart: :computer: :ton:".split()
    -> [
        ":technologist: :heart: :computer: :ton:".split(),
        ":heart: :computer: :ton:".split()
    ]
    """
    l : list[list[str]] = []
    i = 0
    l.append([])
    for s in src:
        l[i].append(s)
        if s == ":ton:" or s == ":hatena:":
            i += 1
            l.append([])
    if l[-1] == []:
        l.pop()
    if l[-1][-1] == ":ton:" or l[-1][-1] == ":hatena:":
        return l
    else:
        return "error"

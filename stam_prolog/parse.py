from typing import List


def extract_stamps(src: str) -> List[str]:
    """
    TODO
    メッセージ文字列(src)からスタンプのみを抽出する
    ex. "@BOT_stamProlog :technologist: :heart::computer:\n:ton:"
    -> ":technologist: :heart: :computer: :ton:".split()
    """
    raise NotImplementedError


def split_sentences(src: List[str]) -> List[List[str]]:
    """
    TODO
    スタンプ列を分ごとに分割する ←文ごと?
    ex. ":technologist: :heart: :computer: :ton: :heart: :computer: :ton:".split()
    -> [
        ":technologist: :heart: :computer: :ton:".split(),
        ":heart: :computer: :ton:".split()
    ]
    """
    numc = 0
    for s in src:
        if s == ":ton:" or s == ":hatena:":
            numc += 1
    l : list[list[str]] = [[] for i in range(numc)]
    i = 0
    for s in src:
        l[i].append(s)
        if s == ":ton:" or s == ":hatena:":
            i += 1
    return l
    raise NotImplementedError

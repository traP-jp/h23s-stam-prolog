from typing import Union


def extract_stamps(src: str) -> list[str]:
    """
    TODO
    メッセージ文字列(src)からスタンプのみを抽出する
    ex. "@BOT_stamProlog :technologist: :heart::computer:\n:ton:"
    -> ":technologist: :heart: :computer: :ton:".split()
    """
    raise NotImplementedError


def split_sentences(src: list[str]) -> Union[list[list[str]], str]:
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

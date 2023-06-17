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
    スタンプ列を分ごとに分割する
    ex. ":technologist: :heart: :computer: :ton: :heart: :computer: :ton:".split()
    -> [
        ":technologist: :heart: :computer: :ton:".split(),
        ":heart: :computer: :ton:".split()
    ]
    """
    raise NotImplementedError

from typing import List


def extract_stamps(src: str) -> List[str]:
    """
    TODO
    メッセージ文字列(src)からスタンプのみを抽出する
    ex. "@BOT_stamProlog :technologist: :heart::computer:\n:ton:"
    -> ":technologist: :heart: :computer: :ton:".split()
    """
    src_size = len(src)
    is_in_stamp = False
    list_stamp = []
    now_stamp = ""
    
    for i in range(src_size):
        if src[i] == ":":
            if is_in_stamp:
                is_in_stamp = False
                list_stamp.append(now_stamp)
                now_stamp = ""
            else:
                is_in_stamp = True
        elif not is_in_stamp:
            continue
        elif ("0" <= src[i] and src[i] <= "9") or ("a" <= src[i] and src[i] <= "z") or ("A" <= src[i] and src[i] <= "Z") or src[i] == "_" or src[i] == "-" or src[i] == ".":
            now_stamp += src[i]
        else:
            is_in_stamp = False
            now_stamp = ""
    
    return list_stamp
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

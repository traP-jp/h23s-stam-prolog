from ast import *
from curses import tparm
from typing import Optional


def extract_stamps(src: str) -> list[str]:
    """
    TODO
    メッセージ文字列(src)からスタンプのみを抽出する
    ex. "@BOT_stamProlog :technologist: :heart::computer:\n:ton:"
    -> ":technologist: :heart: :computer: :ton:".split()
    """
    raise NotImplementedError


def split_sentences(src: list[str]) -> List[List[str]]:
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

class TreeNode:
    def __init__(self):
        self.valueType = None
        self.value = None
        self.parent = None
        self.left = None
        self.right = None
    @classmethod
    def new(self, valueType : str, value: Optional[int | str]) -> None:
        self.valueType = valueType
        self.value = value


#class BinaryTree:
#    def __init__(self) -> None:
#        self.root = None
#    @classmethod
#    def new(cls, type : str, value: Optional[int | str]) -> None:
#        cls.root = TreeNode(type, value)

class parser:
    def statement_parser(src: list[str]) -> TreeNode:
        _tree = TreeNode()
        if ":hatena:" in src:
            _tree = TreeNode.new("queryop", "?")
            _tree.left = stamps_parser()
            _tree.right = None
            return _tree
        elif ":ton:" in src:
            _tree.root = TreeNode.new("declop", ".")
            _tree.right = None
            return _tree
        else:
            return self.stamps_parser(src)
    def statement_parser(src: list[str]) -> TreeNode:
        _tree = TreeNode()
        if ":arrow_right:" in src:
            _tree = TreeNode.new("operand", "->")
            _tree.left = stamps_parser()
            _tree.right = stamps_parser()
            return _tree
        elif ":and:" in src:
            _tree.root = TreeNode.new("boolop", "and")
        else:
            return self.stamps_parser(src)

    def stamps_parser(src: list[str]) -> TreeNode:
        if ":arrow_right:" in src:

        elif ":and:" in src:
            _Tree.root =
        else:
    def_

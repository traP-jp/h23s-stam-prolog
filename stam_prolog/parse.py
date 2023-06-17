from platform import architecture
import re
from typing import Union

from stam_prolog.ast import *


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


def split_sentences(src: list[str]) -> Union[list[list[str]], str]:
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


class TreeNode:
    def __init__(self):
        self.value = None
        self.parent = None
        self.left = None
        self.right = None

    @classmethod
    def new(self, value) -> None:
        self.value = value


class Parser:
    @classmethod
    def statement_parser(cls, src: list[str]) -> TreeNode:
        if ":hatena:" in src:
            return cls.query_statement_parser(src)
        if ":ton" in src:
            return cls.decl_statement_parser(src)

    @classmethod
    def decl_statement_parser(cls, sentence: DeclStatement):
        _tree = TreeNode()
        _tree = TreeNode.new(sentence)
        sentence = sentence[:-1]
        if ":right_arrow:" in sentence:
            splited_sentence = sentence.split(":right_arrow:", 1)
            if splited_sentence[0] == "0" or splited_sentence[1] == "":
                raise SyntaxError("矢印の前後の文法が不適切です")
            _tree.left = cls.var_single_statement_parser(splited_sentence[0])
            _tree.right = cls.var_single_statement_parser(splited_sentence[1])
        else:
            _tree.left = cls.var_single_statement_parser(sentence)
        return _tree

    @classmethod
    def decl_statement_parser(cls, sentence: QueryStatement):
        _tree = TreeNode()
        _tree = TreeNode.new(sentence)
        sentence = sentence[:-1]
        if ":right_arrow:" in sentence:
            splited_sentence = sentence.split(":right_arrow:", 1)
            if splited_sentence[0] == "0" or splited_sentence[1] == "":
                raise SyntaxError("矢印の前後の文法が不適切です")
            _tree.left = cls.var_single_statement_parser(splited_sentence[0])
            _tree.right = cls.var_single_statement_parser(splited_sentence[1])
            return _tree
        else:
            _tree.left = cls.var_single_statement_parser(sentence)
        return _tree

    @classmethod
    def var_single_statement_parser(cls, sentence: VarSingleStatement):
        _tree = TreeNode()
        _tree = TreeNode.new(sentence)
        if ":right_arrow:" in sentence:
            raise SyntaxError("矢印の前後の文法が不適切です")
        if ":and:" in sentence:
            splited_sentence = sentence.split(":and:", 1)
            if splited_sentence[0] == "0" or splited_sentence[1] == "":
                raise SyntaxError(":and:の前後の文法が不適切です")
            _tree.left = cls.var_stamps_parser(splited_sentence[0])
            _tree.right = cls.var_single_statement_parser(splited_sentence[1])
            return _tree
        else:
            _tree.left = cls.var_stamps_parser(sentence)
            return _tree

    def var_stamps_parser(sentence: VarStamps) -> TreeNode:
        __math_stamp_list = {
            "zero": "0",
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }
        _tree = TreeNode()
        _tree = TreeNode.new(sentence)
        num_sentence_match = None
        for keys in __math_stamp_list.keys():
            if keys in VarStamps:
                num_sentence_match = __math_stamp_list[keys]
        # TODO: 数字と普通のスタンプがあったときの例外
        var_sentence_match = re.match(":[a-z]:")
        if num_sentence_match:
            from stam_prolog.parse_math import *
            #expr_parser
            #TODO: mathのparse
        elif not(var_sentence_match):
            _tree.left = cls.stamps_parser(sentence)
        return _tree

    def stamps_parser(sentence: Stamps) -> TreeNode:
        _tree = TreeNode()
        _tree = TreeNode.new(sentence)










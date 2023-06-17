import re
from platform import architecture
from typing import Union

from stam_prolog.ast import (
    DeclStatement,
    QueryStatement,
    Atom,
    Variable,
    Stamps,
    VarStamps,
    VarSingleStatement,
    ConditionalStatement,
)
from stam_prolog.ast.statement import SingleStatement


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


class Parser:
    @classmethod
    def statement_parser(cls, src: list[str]) -> Union[DeclStatement, QueryStatement]:
        if ":hatena:" in src:
            return cls.query_statement_parser(src)
        elif ":ton:" in src:
            return cls.decl_statement_parser(src)
        else:
            raise SyntaxError("構文エラー: 不明なエラー")

    @classmethod
    def decl_statement_parser(cls, sentence: list[str]) -> DeclStatement:
        sentence = sentence[:-1]
        if ":right_arrow:" in sentence:
            return cls.conditional_statement_parser(sentence)
        else:
            return cls.single_statement_parser(sentence)

    @classmethod
    def query_statement_parser(cls, sentence: list[str]) -> QueryStatement:
        sentence = sentence[:-1]
        if ":right_arrow:" in sentence:
            return cls.conditional_statement_parser(sentence)
        else:
            return cls.var_single_statement_parser(sentence)

    @classmethod
    def conditional_statement_parser(cls, sentence: list[str]) -> ConditionalStatement:
        if sentence.count(":right_arrow:") >= 2:
            raise SyntaxError("構文エラー: 一つの文に矢印が二つ以上あります")
        _condition, _then = [], []
        _tmp: list[str] = []
        for value in sentence:
            if value == ":right_arrow:":
                _condition = _tmp
                _tmp = []
            else:
                _tmp.append(value)
        _then = _tmp
        if _condition == [] or _then == []:
            raise SyntaxError("構文エラー: 矢印の位置が不適切です")
        _statement = ConditionalStatement(
            condition=cls.var_single_statement_parser(_condition),
            then=cls.var_single_statement_parser(_then),
        )
        return _statement


# TODO exprの扱いを実装
"""
    @classmethod
    def single_statement_parser(cls, sentence: list[str]) -> SingleStatement:
        _stamps_list = []
        _tmp: Stamps = []
        for value in sentence:
            if value == ":and:":
                _stamps_list.append(_tmp)
                _tmp = []
            else:
                _tmp.append(cls.atom_parser(value))
        if _tmp != []:
            _stamps_list.append(_tmp)
        return _stamps_list


    @classmethod
    def var_single_statement_parser(cls, sentence: list[str]) -> SingleStatement:
        _var_stamps_list = []
        _tmp: VarStamps = []
        for value in sentence:
            if value == ":and:":
                _stamps_list.append(_tmp)
                _tmp = []
            else:
                _tmp.append(cls.atom_parser(value))
        if _tmp != []:
            _stamps_list.append(_tmp)
        return _stamps_list

    @classmethod atom_parser(cls, sentence: list[str]) -> Atom:

    @classmethod
    def var_stamps_parser(sentence: list[str]) -> TreeNode:
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
        _tree.set(sentence)
        num_sentence_match = None
        for keys in __math_stamp_list.keys():
            if keys in VarStamps:
                num_sentence_match = __math_stamp_list[keys]
        # TODO: 数字と普通のスタンプがあったときの例外
        var_sentence_match = re.match(":[a-z]:")
        # if num_sentence_match:
        # from stam_prolog.parse_math import *

        # expr_parser
        # TODO: mathのparse
        ##elif not (var_sentence_match):
        #   _tree.left = cls.stamps_parser(sentence)
"""

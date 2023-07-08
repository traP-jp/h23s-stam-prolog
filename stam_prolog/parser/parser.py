from typing import Union

from .. import ast
from ..parse import extract_stamps, split_statements
from .statement_parser import StatementParser


class Parser:
    def parse(
        self, src: str
    ) -> Union[list[tuple[bool, Union[ast.DeclStatement, ast.QueryStatement]]], str]:
        stamps = extract_stamps(src)
        statements = split_statements(stamps)
        if isinstance(statements, str):
            return statements
        res = []
        for s in statements:
            sp = StatementParser()
            res.append(sp.parse(s))
        return res

from typing import Union

from .. import ast


class Parser:
    def parse(self, src: str) -> list[Union[ast.DeclStatement, ast.QueryStatement]]:
        # TODO
        raise NotImplementedError

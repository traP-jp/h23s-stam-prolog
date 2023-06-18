from typing import Union

from ...ast import math
from ..stamp_kind import StampKind


def split_tokens(src: list[tuple[StampKind, str]]) -> list[Union[math.Literal, str]]:
    res: list[Union[math.Literal, str]] = []
    literal_stack: list[str] = []
    for k, s in src:
        if k & StampKind.MathOperator:
            literal = math.Literal.from_stamps(literal_stack)
            literal_stack.clear()
            res.append(literal)
            res.append(s)
            continue
        literal_stack.append(s)
    return res

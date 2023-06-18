from ast import Expression
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


def parse_math(src: list[tuple[StampKind, str]]) -> Expression:
    tokens = split_tokens(src)
    output: list[math.Expression] = []
    operator_stack: list[str] = []

    def push_operator(op: str) -> None:
        if op == ":heavy_plus_sign:":
            output.append(math.AddExpression(output.pop(), output.pop()))
        elif op == ":heavy_minus_sign:":
            output.append(math.SubExpression(output.pop(), output.pop()))
        elif op == ":heavy_multiplication_x:":
            output.append(math.MulTerm(output.pop(), output.pop()))
        elif op == ":heavy_division_sign:":
            output.append(math.DivTerm(output.pop(), output.pop()))
        else:
            raise NotImplementedError

    for token in tokens:
        if isinstance(token, math.Literal):
            output.append(token)
            continue
        if not operator_stack:
            operator_stack.append(token)
            continue
        if token in [":heavy_plus_sign:", ":heavy_minus_sign:"]:
            while operator_stack:
                push_operator(operator_stack.pop())
            operator_stack.append(token)
            continue
        if token in [":heavy_multiplication_x:", ":heavy_division_sign:"]:
            while operator_stack and operator_stack[-1] in [
                ":heavy_multiplication_x:",
                ":heavy_division_sign:",
            ]:
                push_operator(operator_stack.pop())
            operator_stack.append(token)
            continue
    raise NotImplementedError

from dataclasses import dataclass
from typing import Union

from frozenlist import FrozenList

from .math import Expression


@dataclass(frozen=True)
class Stamp:
    name: str


@dataclass(frozen=True)
class Variable:
    name: str


Atom = Union[Stamp, Expression]
Stamps = FrozenList[Atom]
VarStamps = FrozenList[Union[Atom, Variable]]


def _num2str(n: int) -> str:
    if n < 0:
        return f":heavy_minus_sign:{_num2str(-n)}"
    if n < 10:
        s = "zero one two three four five six seven eight nine".split()[n]
        return f":{s}:"
    return f"{_num2str(n // 10)}:{_num2str(n % 10)}"


def to_str(statement: Union[Atom, Variable]) -> str:
    if isinstance(statement, Variable):
        return f"{statement.name}"
    elif isinstance(statement, Stamp):
        return f"{statement.name}"
    else:
        return _num2str(statement.eval())

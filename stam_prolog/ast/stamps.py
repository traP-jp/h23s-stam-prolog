from dataclasses import dataclass
from typing import Union

from .math import Expression


@dataclass(frozen=True)
class Stamp:
    name: str


@dataclass(frozen=True)
class Variable:
    name: str


# immutableにしたいが厳しいかも
Atom = Union[Stamp, Expression]
Stamps = list[Atom]
VarStamps = list[Union[Atom, Variable]]

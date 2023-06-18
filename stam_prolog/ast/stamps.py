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

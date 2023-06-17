from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Stamp:
    name: str


@dataclass(frozen=True)
class Variable:
    name: str


# TODO: math.Expressionを追加する
# immutableにしたいが厳しいかも
Stamps = list[Stamp]
VarStamps = list[Union[Stamp, Variable]]

from dataclasses import dataclass
from typing import Self, Union

from . import Expression

_CVT_TABLE = {
    ":heavy_plus_sign:": "+",
    ":heavy_minus_sign:": "-",
    ":zero:": "0",
    ":one:": "1",
    ":two:": "2",
    ":three:": "3",
    ":four:": "4",
    ":five:": "5",
    ":six:": "6",
    ":seven:": "7",
    ":eight:": "8",
    ":nine:": "9",
}


@dataclass(frozen=True)
class Literal(Expression):
    value: int

    def eval(self) -> int:
        return self.value

    @classmethod
    def from_stamps(cls, stamps: list[str]) -> Self:
        s = "".join(_CVT_TABLE[stamp] for stamp in stamps)
        return cls(int(s))


Factor = Union[Literal, Expression]

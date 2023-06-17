from dataclasses import dataclass
from typing import Union

from . import Expression


@dataclass(frozen=True)
class Literal(Expression):
    value: int

    def eval(self) -> int:
        return self.value


Factor = Union[Literal, Expression]

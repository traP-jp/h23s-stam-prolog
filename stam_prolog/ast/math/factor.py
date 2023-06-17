from typing import Union

from . import Expression

Literal = int
Factor = Union[Literal, Expression]

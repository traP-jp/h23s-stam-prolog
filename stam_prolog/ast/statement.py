from dataclasses import dataclass
from typing import Self, Union

from frozenlist import FrozenList

from .stamps import Stamps as _Stamps
from .stamps import VarStamps as _VarStamps

# andで繋がっている
SingleStatement = FrozenList[_Stamps]
VarSingleStatement = FrozenList[_VarStamps]


@dataclass(frozen=True)
class ConditionalStatement:
    condition: VarSingleStatement
    then: VarSingleStatement

    # freezeを確実に行うため
    @classmethod
    def new(cls, condition: VarSingleStatement, then: VarSingleStatement) -> Self:
        condition.freeze()
        then.freeze()
        return cls(condition, then)


QueryStatement = Union[VarSingleStatement, ConditionalStatement]
DeclStatement = Union[SingleStatement, ConditionalStatement]

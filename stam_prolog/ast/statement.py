from dataclasses import dataclass
from typing import Self, Union

from frozenlist import FrozenList

from .stamps import Stamps as _Stamps
from .stamps import VarStamps as _VarStamps
from .stamps import to_str as _atom_to_str

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


def to_str(statement: Union[DeclStatement, QueryStatement]) -> str:
    if isinstance(statement, ConditionalStatement):
        return f"{to_str(statement.condition)}:arrow_right:{to_str(statement.then)}"
    return ":and:".join("".join(_atom_to_str(s) for s in ss) for ss in statement)

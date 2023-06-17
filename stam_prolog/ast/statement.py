from dataclasses import dataclass
from typing import Union

from frozenlist import FrozenList
from stamps import Stamps as _Stamps
from stamps import VarStamps as _VarStamps

# andで繋がっている
SingleStatement = FrozenList[_Stamps]
VarSingleStatement = FrozenList[_VarStamps]


@dataclass(frozen=True)
class ConditionalStatement:
    condition: VarSingleStatement
    then: VarSingleStatement


QueryStatement = Union[VarSingleStatement, ConditionalStatement]
DeclStatement = Union[SingleStatement, ConditionalStatement]

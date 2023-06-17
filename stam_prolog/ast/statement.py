from dataclasses import dataclass
from typing import Union

from stamps import Stamps as _Stamps
from stamps import VarStamps as _VarStamps

# andで繋がっている
SingleStatement = list[_Stamps]
VarSingleStatement = list[_VarStamps]


@dataclass(frozen=True)
class ConditionalStatement:
    condition: VarSingleStatement
    then: VarSingleStatement


QueryStatement = Union[VarSingleStatement, ConditionalStatement]
DeclStatement = Union[SingleStatement, ConditionalStatement]

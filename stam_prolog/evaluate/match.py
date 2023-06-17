from typing import Optional

from ..ast import Stamps, Variable, VarStamps


def match_stamps(
    stamps: Stamps, var_stamps: VarStamps
) -> Optional[dict[Variable, Stamps]]:
    """
    TODO
    スタンプがマッチするかどうかを判定する
    ex:
    stamps = [Stamp("technologist"), Stamp("heart"), Stamp("girl"), Stamp("computer")]
    var_stamps = [Stamp("technologist"), Variable("x"), Stamp("computer")]
    ---
    返り値はどのVariableがどのようなスタンプ列に置き換えられるかを示す
    そもそもマッチしなかったらNoneを返す
    """
    raise NotImplementedError

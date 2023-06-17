from typing import Optional

from ..ast import Stamps, Variable, VarSingleStatement, VarStamps


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


def papply_match(match: dict[Variable, Stamps], var_stamps: VarStamps) -> VarStamps:
    """
    TODO
    マッチしたVariableを置き換える
    置換できなかったvariableはそのまま
    """
    raise NotImplementedError


def apply_match(
    match: dict[Variable, Stamps], var_stamps: VarStamps
) -> Optional[Stamps]:
    """
    TODO
    マッチしたVariableを置き換える
    var_stampsに置換できなかったvariableがあったらNoneを返す
    """
    raise NotImplementedError


def contextful_match(
    pre_match: dict[Variable, Stamps],
    condition: VarSingleStatement,
    declarations: set[Stamps],
) -> list[dict[Variable, Stamps]]:
    """
    TODO
    既にvariableのマッチpre_matchが定まっている中で、declarationsに対してconditionがマッチするパターン全てを列挙する
    """
    raise NotImplementedError

from typing import Optional

from frozenlist import FrozenList

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
    マッチしたVariableを置き換える
    置換できなかったvariableはそのまま
    """
    res: VarStamps = FrozenList()
    for v in var_stamps:
        if isinstance(v, Variable):
            res += match.get(v, [v])
        else:
            res.append(v)
    res.freeze()
    return res


def apply_match(
    match: dict[Variable, Stamps], var_stamps: VarStamps
) -> Optional[Stamps]:
    """
    マッチしたVariableを置き換える
    var_stampsに置換できなかったvariableがあったらNoneを返す
    """
    res = papply_match(match, var_stamps)
    if any(isinstance(v, Variable) for v in res):
        return None
    return res  # type: ignore


def contextful_match(
    pre_match: dict[Variable, Stamps],
    condition: VarSingleStatement,
    declarations: set[Stamps],
) -> list[dict[Variable, Stamps]]:
    """
    既にvariableのマッチpre_matchが定まっている中で、declarationsに対してconditionがマッチするパターン全てを列挙する
    """
    if not condition:
        return [pre_match]
    res = []
    cond = papply_match(pre_match, condition[0])
    for decl in declarations:
        m = match_stamps(decl, cond)
        if isinstance(m, dict):
            m.update(pre_match)
            res += contextful_match(m, condition[1:], declarations)
    return res

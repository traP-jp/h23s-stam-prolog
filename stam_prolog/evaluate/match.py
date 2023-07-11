from typing import Optional

from frozenlist import FrozenList

from ..ast import Stamps, Variable, VarSingleStatement, VarStamps


def match_stamps_search(stamps: Stamps, var_stamps: VarStamps) -> list[list[int]]:
    length_stamps = len(stamps)
    length_var_stamps = len(var_stamps)
    is_in_var = False
    var = []
    var_begin = 0
    var_cnt = sum(isinstance(stamp, Variable) for stamp in var_stamps)
    var_seen = i = j = 0
    while i < length_stamps:
        if isinstance(var_stamps[j], Variable):
            var_seen += 1
            if var_seen == var_cnt:
                var.append([j, i, length_stamps - length_var_stamps + j])
                i = length_stamps - (length_var_stamps - j - 1)
            elif j == length_var_stamps - 1:
                var.append([j, i, length_stamps - 1])
            elif isinstance(var_stamps[j + 1], Variable):
                var.append([j, i, i])
            else:
                var_begin = i
                is_in_var = True
        elif is_in_var and stamps[i] == var_stamps[j]:
            var.append([j - 1, var_begin, i - 1])
            is_in_var = False
        elif stamps[i] != var_stamps[j]:
            break
        j += 1
        if j == length_var_stamps:
            break
        i += 1
    return var


def match_stamps(
    stamps: Stamps, var_stamps: VarStamps
) -> Optional[dict[Variable, Stamps]]:
    """
    スタンプがマッチするかどうかを判定する
    ex:
    stamps = [Stamp("technologist"), Stamp("heart"), Stamp("girl"), Stamp("computer")]
    var_stamps = [Stamp("technologist"), Variable("x"), Stamp("computer")]
    ---
    返り値はどのVariableがどのようなスタンプ列に置き換えられるかを示す
    そもそもマッチしなかったらNoneを返す
    """
    var = match_stamps_search(stamps, var_stamps)
    matched_dict: dict[Variable, Stamps] = {}
    for x in var:
        for i in range(x[1], x[2] + 1):
            v = var_stamps[x[0]]
            if isinstance(v, Variable):
                if v not in matched_dict:
                    matched_dict[v] = FrozenList()
                matched_dict[v].append(stamps[i])
    if len(matched_dict):
        for k in matched_dict:
            matched_dict[k].freeze()
        return matched_dict
    else:
        return None


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

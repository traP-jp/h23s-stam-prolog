from typing import Optional

from frozenlist import FrozenList

from ..ast import Stamps, Variable, VarSingleStatement, VarStamps


def match_stamps_search(
    stamps: Stamps, var_stamps: VarStamps
) -> list[tuple[int, int, int]]:
    length_stamps = len(stamps)
    length_var_stamps = len(var_stamps)
    var = []
    var_cnt = sum(isinstance(stamp, Variable) for stamp in var_stamps)
    var_seen = i = j = 0
    check = True
    while (not var_seen == var_cnt) or (not check):
        if (i == length_stamps) or (j == length_var_stamps):
            break
        if not isinstance(var_stamps[j], Variable):
            if stamps[i] == var_stamps[j]:
                i += 1
                j += 1
            else:
                check = False
                continue
        var_seen += 1
        if j == length_var_stamps - 1:
            # 最後まで適用
            var.append([j, i, length_stamps - 1])
            i = length_stamps
            j += 1
        elif var_seen == var_cnt:
            if i > length_stamps - length_var_stamps + j:
                check = False
                continue
            var.append([j, i, length_stamps - length_var_stamps + j])
            i = length_stamps - (length_var_stamps - j - 1)
            j += 1
            while i != length_stamps:
                if stamps[i] != var_stamps[j]:
                    check = False
                i += 1
                j += 1
        elif isinstance(var_stamps[j + 1], Variable):
            # 変数連続の際
            var.append([j, i, i])
            i += 1
            j += 1
        else:
            var_begin = i
            i += 1
            while stamps[i] != var_stamps[j + 1]:
                i += 1
                if i >= length_stamps:
                    check = False
                    break
            # stamps[i] == var_stamps[j]
            var.append([j, var_begin, i - 1])
            j += 1
    # チェック
    if i != length_stamps or j != length_var_stamps:
        check = False
    if check:
        return var
    else:
        return


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

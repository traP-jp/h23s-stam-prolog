from ..ast import Stamps, Variable, VarStamps


def match_stamps(stamps: Stamps, var_stamps: VarStamps) -> bool:
    """
    スタンプがマッチするかどうかを判定する
    ex:
    stamps = [Stamp("technologist"), Stamp("heart"), Stamp("girl"), Stamp("computer")]
    var_stamps = [Stamp("technologist"), Variable("x"), Stamp("computer")]
    ---
    variableは1つ以上のスタンプにマッチする
    →xにStamp("heart"),Stamp("girl")を代入したらマッチする
    """
    former = []
    latter = []
    verpass = False
    if len(stamps) < len(var_stamps):
        return False
    for ver in var_stamps:
        if not verpass:
            if ver != Variable:
                former.append(ver)
            else:
                verpass = True
        else:
            latter.append(ver)
    for i in range(len(former)):
        if former[i] != stamps[i]:
            return False
    for j in range(len(latter)):
        if latter[j] != stamps[len(var_stamps) - len(latter) + j]:
            return False
    return True

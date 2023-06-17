from ..ast import Stamps, VarStamps


def match_stamps(stamps: Stamps, var_stamps: VarStamps) -> bool:
    """
    TODO
    スタンプがマッチするかどうかを判定する
    ex:
    stamps = [Stamp("technologist"), Stamp("heart"), Stamp("girl"), Stamp("computer")]
    var_stamps = [Stamp("technologist"), Variable("x"), Variable("computer")]
    ---
    variableは1つ以上のスタンプにマッチする
    """
    raise NotImplementedError

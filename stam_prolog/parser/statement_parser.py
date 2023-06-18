from typing import Optional

from .. import ast
from .stamp_kind import StampKind
from .statement_kind import StatementKind


class StatementParser:
    def __init__(self) -> None:
        # 今処理している文の種類
        self.s_kind: StatementKind = StatementKind.NormalDeclaration
        self.reading_math: bool = False
        # 次に受け入れられるスタンプの種類
        self.next_stamp_kind: StampKind = StampKind.All ^ StampKind.ArrowRight

    def judge_stamp_kinds(self, stamps: list[str]) -> list[StampKind]:
        ks = [(StampKind.judge(stamp), stamp) for stamp in stamps]
        res: list[StampKind] = []
        for i, e in enumerate(ks):
            k, _ = e
            if k & StampKind.Variable:
                res.append(StampKind.Variable)
                continue
            if k & StampKind.ArrowRight:
                res.append(StampKind.ArrowRight)
                continue
            if k & StampKind.MathNumber:
                res.append(StampKind.MathNumber)
                continue
            if not k & StampKind.MathOperator:
                res.append(StampKind.Normal)
                continue
            # 残りは演算子
            if i == len(stamps) - 1:
                res.append(StampKind.Normal)
                continue
            if i == 0:
                if not k & StampKind.MathSign:
                    res.append(StampKind.Normal)
                    continue
                res.append(StampKind.Normal)
                continue
            if ks[i - 1][0] & StampKind.MathNumber:
                if ks[i + 1][0] & StampKind.MathNumber:
                    res.append(StampKind.MathOperator)
                    continue
                res.append(StampKind.Normal)
                continue
            if ks[i + 1][0] & StampKind.MathNumber:
                if k & StampKind.MathSign:
                    res.append(StampKind.MathSign)
                    continue
            res.append(StampKind.Normal)
        return res

    def parse(
        self, stamps: list[str]
    ) -> Optional[ast.DeclStatement | ast.QueryStatement]:
        self.s_kind = StatementKind.judge(stamps)
        if self.s_kind == StatementKind.NormalDeclaration:
            self.next_stamp_kind ^= StampKind.Variable
        # kinds = self.judge_stamp_kinds(stamps[:-1])
        raise NotImplementedError

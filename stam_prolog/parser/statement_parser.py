from typing import Union

from frozenlist import FrozenList

from stam_prolog.ast.stamps import VarStamps

from .. import ast
from .math.math_parser import parse_math
from .stamp_kind import StampKind
from .statement_kind import StatementKind


class StatementParser:
    def __init__(self) -> None:
        # 今処理している文の種類
        self.s_kind: StatementKind = StatementKind.NormalDeclaration

    def judge_stamp_kinds(self, stamps: list[str]) -> list[StampKind]:
        ks = [(StampKind.judge(stamp), stamp) for stamp in stamps]
        res: list[StampKind] = []
        for i, e in enumerate(ks):
            k, _ = e
            if k & (
                StampKind.Variable
                | StampKind.ArrowRight
                | StampKind.MathNumber
                | StampKind.And
            ):
                res.append(k)
                continue
            if not k & StampKind.MathOperator:
                res.append(StampKind.Normal)
                continue
            # 残りは演算子
            if i == len(stamps) - 1:
                res.append(StampKind.Normal)
                continue
            if i == 0 and not k & StampKind.MathSign:
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

    def parse_single_statement(
        self, stamps: list[str]
    ) -> Union[ast.SingleStatement, ast.VarSingleStatement]:
        res: FrozenList[VarStamps] = FrozenList()
        kinds = self.judge_stamp_kinds(stamps)
        math_stack: list[tuple[StampKind, str]] = []
        ss_stack: FrozenList[ast.Atom | ast.Variable] = FrozenList()
        for k, s in zip(kinds, stamps):
            if k & (StampKind.MathNumber | StampKind.MathSign | StampKind.MathOperator):
                math_stack.append((k, s))
                continue
            if math_stack:
                ss_stack.append(parse_math(math_stack))
                math_stack.clear()
            if k & StampKind.Variable:
                ss_stack.append(ast.Variable(s))
                continue
            if k & StampKind.And:
                ss_stack.freeze()
                res.append(ss_stack)
                ss_stack = FrozenList()
                continue
            ss_stack.append(ast.Stamp(s))
        if ss_stack:
            ss_stack.freeze()
            res.append(ss_stack)
        res.freeze()
        return res

    def parse_cond_statement(self, stamps: list[str]) -> ast.ConditionalStatement:
        res_l: FrozenList[VarStamps] = FrozenList()
        res_r: FrozenList[VarStamps] = FrozenList()
        kinds = self.judge_stamp_kinds(stamps)
        math_stack: list[tuple[StampKind, str]] = []
        ss_stack: FrozenList[ast.Atom | ast.Variable] = FrozenList()
        read_arrow = False
        for k, s in zip(kinds, stamps):
            if k & (StampKind.MathNumber | StampKind.MathSign | StampKind.MathOperator):
                math_stack.append((k, s))
                continue
            if math_stack:
                ss_stack.append(parse_math(math_stack))
                math_stack.clear()
            if k & StampKind.Variable:
                ss_stack.append(ast.Variable(s))
                continue
            if k & StampKind.And:
                ss_stack.freeze()
                if read_arrow:
                    res_r.append(ss_stack)
                else:
                    res_l.append(ss_stack)
                ss_stack = FrozenList()
                continue
            ss_stack.append(ast.Stamp(s))
        if ss_stack:
            ss_stack.freeze()
            res_r.append(ss_stack)
        return ast.ConditionalStatement.new(res_l, res_r)

    def parse(
        self, stamps: list[str]
    ) -> tuple[bool, ast.DeclStatement | ast.QueryStatement]:
        kind = StatementKind.judge(stamps)
        if kind == StatementKind.NormalDeclaration:
            return (False, self.parse_single_statement(stamps[:-1]))
        if kind == StatementKind.ConditionalDeclaration:
            return (False, self.parse_cond_statement(stamps[:-1]))
        if kind == StatementKind.NormalQuery:
            return (True, self.parse_single_statement(stamps[:-1]))
        if kind == StatementKind.ConditionalQuery:
            return (True, self.parse_cond_statement(stamps[:-1]))
        raise NotImplementedError

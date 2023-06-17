from typing import Optional

from ..ast import (
    ConditionalStatement,
    QueryStatement,
    SingleStatement,
    Stamps,
    Variable,
    VarSingleStatement,
)
from .match import apply_match, match_stamps


class Evaluator:
    __slots__ = ("__declarations", "__cond_declarations", "__errored")

    def __init__(self) -> None:
        self.__declarations: set[Stamps] = set()
        self.__cond_declarations: set[ConditionalStatement] = set()
        self.__errored = False

    def _add_statement(self, statement: Stamps) -> None:
        """
        declarationsにstatementを追加する
        cond_declarationsを見て、条件に合致するものがあれば、そのthenを追加する
        """
        if self.__errored:
            return
        # これ冪等なので何回もやってる
        statement.freeze()
        if statement in self.__declarations:
            return
        self.__declarations.add(statement)
        for c_decl in self.__cond_declarations:
            replace = self._match_condition(c_decl.condition)
            if replace is None:
                continue
            # replaceを適用してthenを追加する
            replaced = list(apply_match(replace, t) for t in c_decl.then)
            if any(r is None for r in replaced):
                self.__errored = True
                return
            for r in replaced:
                # 上のanyで確認したのでここではassertで良い
                assert r is not None
                self._add_statement(r)

    def _match_condition(
        self, condition: VarSingleStatement
    ) -> Optional[dict[Variable, Stamps]]:
        """
        現在のdeclarationsに対して、conditionがマッチするかどうかを判定する
        返り値は.match.match_stampsと同じ
        """
        if self.__errored:
            return None
        # condition内のvarstamps全てがdeclarationsにマッチするように置き換えを構成する
        result: dict[Variable, Stamps] = {}
        for c in condition:
            m: Optional[dict[Variable, Stamps]] = None
            for d in self.__declarations:
                m = match_stamps(d, c)
                if not isinstance(m, dict):
                    # マッチしなかったら次のdeclarationsを見る
                    continue
                # 既存の置き換えと矛盾しないか確認する
                proper_match = True
                for k, v in m.items():
                    if k in result and result[k] != v:
                        proper_match = False
                        break
                if proper_match:
                    break
            if not isinstance(m, dict):
                return None
            result.update(m)
        return result

    def eval_single_statement(self, statement: SingleStatement) -> None:
        if self.__errored:
            return
        for s in statement:
            self._add_statement(s)

    def eval_conditional_statement(self, statement: ConditionalStatement) -> None:
        if self.__errored:
            return
        self.__cond_declarations.add(statement)

    def eval_query_statement(self, statement: QueryStatement) -> None:
        ...

    def get_output(self) -> str:
        return ""

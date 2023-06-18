from ..ast import ConditionalStatement, QueryStatement, SingleStatement, Stamps
from .match import apply_match, contextful_match


class Evaluator:
    __slots__ = ("__declarations", "__cond_declarations", "__errored")

    def __init__(self) -> None:
        self.__declarations: set[Stamps] = set()
        self.__cond_declarations: set[ConditionalStatement] = set()
        self.__errored = False

    def _add_statement(self, statement: Stamps) -> None:
        """
        declarationsにstatementを追加する
        既存conditionと全てマッチ確認→マッチしたものを適用してdecl追加
        """
        if self.__errored:
            return
        # これ冪等なので何回もやってる
        statement.freeze()
        if statement in self.__declarations:
            return
        self.__declarations.add(statement)
        ss = {statement}
        for c in self.__cond_declarations:
            if not contextful_match({}, c.condition, ss):
                continue
            m_all = contextful_match({}, c.condition, self.__declarations)
            for replace in m_all:
                replaced = list(apply_match(replace, t) for t in c.then)
                if any(r is None for r in replaced):
                    self.__errored = True
                    return
                for r in replaced:
                    # 上のanyで確認したのでここではassertで良い
                    assert r is not None
                    self._add_statement(r)

    def _add_cond_statement(self, statement: ConditionalStatement) -> None:
        """
        cond_declarationsにstatementを追加する
        マッチを全て列挙→マッチ適用後を全てdeclに追加
        """
        if self.__errored:
            return
        if statement in self.__cond_declarations:
            return
        self.__cond_declarations.add(statement)
        m_all = contextful_match({}, statement.condition, self.__declarations)
        for replace in m_all:
            replaced = list(apply_match(replace, t) for t in statement.then)
            if any(r is None for r in replaced):
                self.__errored = True
                return
            for r in replaced:
                # 上のanyで確認したのでここではassertで良い
                assert r is not None
                self._add_statement(r)

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

from ..ast import (
    ConditionalStatement,
    DeclStatement,
    QueryStatement,
    SingleStatement,
    Stamps,
    Variable,
    VarSingleStatement,
)
from ..ast.stamps import to_str
from .match import apply_match, contextful_match


class Ok(str):
    pass


class Err(str):
    pass


class Evaluator:
    __slots__ = ("__declarations", "__cond_declarations", "__output", "__errored")

    def __init__(self) -> None:
        self.__declarations: set[Stamps] = set()
        self.__cond_declarations: set[ConditionalStatement] = set()
        self.__output: str = ""
        self.__errored = False

    def is_err(self) -> bool:
        return self.__errored

    def _add_statement(self, statement: Stamps) -> None:
        """
        declarationsにstatementを追加する
        既存conditionと全てマッチ確認→マッチしたものを適用してdecl追加
        """
        if self.is_err() or len(statement) > 50:
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
                    # TODO: エラーかどうか確かめる
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
        if self.is_err():
            return
        if statement in self.__cond_declarations:
            return
        self.__cond_declarations.add(statement)
        m_all = contextful_match({}, statement.condition, self.__declarations)
        for replace in m_all:
            replaced = list(apply_match(replace, t) for t in statement.then)
            if any(r is None for r in replaced):
                # TODO: エラーかどうか確かめる
                return
            for r in replaced:
                # 上のanyで確認したのでここではassertで良い
                assert r is not None
                self._add_statement(r)

    def eval_single_statement(self, statement: SingleStatement) -> None:
        if self.is_err():
            return
        for s in statement:
            self._add_statement(s)

    def eval_conditional_statement(self, statement: ConditionalStatement) -> None:
        if self.is_err():
            return
        self._add_cond_statement(statement)

    def eval_decl_statement(self, statement: DeclStatement) -> None:
        if self.is_err():
            return
        if isinstance(statement, ConditionalStatement):
            self.eval_conditional_statement(statement)
        else:
            self.eval_single_statement(statement)

    def _eval_query_cnd_statement(self, statement: ConditionalStatement) -> None:
        if self.is_err():
            return
        m_all = contextful_match({}, statement.condition, self.__declarations)
        for replace in m_all:
            replaced = list(apply_match(replace, t) for t in statement.then)
            if any(r is None for r in replaced):
                # TODO: エラーかどうか確かめる
                return
            for r in replaced:
                # 上のanyで確認したのでここではassertで良い
                assert r is not None
                # ここstr(s)ではない
                self.__output += "".join(to_str(s) for s in r) + "\n"

    def _eval_query_var_statement(self, statement: VarSingleStatement) -> None:
        if self.is_err():
            return
        if not any(isinstance(s, Variable) for ss in statement for s in ss):
            # statementは変数を含まない
            res = all(ss in self.__declarations for ss in statement)
            self.__output += ":true:\n" if res else ":false:\n"
            return
        m_all = contextful_match({}, statement, self.__declarations)
        for replace in m_all:
            replaced = list(apply_match(replace, t) for t in statement)
            if any(r is None for r in replaced):
                # TODO: エラーかどうか確かめる
                return
            for r in replaced:
                # 上のanyで確認したのでここではassertで良い
                assert r is not None
                # ここstr(s)ではない
                self.__output += "".join(to_str(s) for s in r) + "\n"

    def eval_query_statement(self, statement: QueryStatement) -> None:
        if self.is_err():
            return
        if isinstance(statement, ConditionalStatement):
            self._eval_query_cnd_statement(statement)
        else:
            self._eval_query_var_statement(statement)

    def get_output(self) -> str:
        return self.__output

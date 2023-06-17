from ..ast import ConditionalStatement, QueryStatement, SingleStatement, Stamps


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
        # これ冪等なので何回もやってる
        statement.freeze()
        if statement in self.__declarations:
            return
        self.__declarations.add(statement)
        # TODO

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

from ..ast import ConditionalStatement, DeclStatement, QueryStatement


class Evaluator:
    __slots__ = ("__declarations", "__cond_declarations", "__errored")

    def __init__(self) -> None:
        self.__declarations: set[DeclStatement] = set()
        self.__cond_declarations: set[ConditionalStatement] = set()
        self.__errored = False

    def eval_single_statement(self, statement: SingleStatement) -> None:
        if self.__errored:
            return
        self.__declarations.add(statement)

    def eval_conditional_statement(self, statement: ConditionalStatement) -> None:
        if self.__errored:
            return
        self.__cond_declarations.add(statement)

    def eval_query_statement(self, statement: QueryStatement) -> None:
        ...

    def get_output(self) -> str:
        return ""

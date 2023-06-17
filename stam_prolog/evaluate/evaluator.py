from ..ast import ConditionalStatement, DeclStatement, QueryStatement


class Evaluator:
    __slots__ = ("__declarations", "__cond_declarations")

    def __init__(self) -> None:
        self.__declarations: set[DeclStatement] = set()
        self.__cond_declarations: set[ConditionalStatement] = set()

    def eval_decl_statement(self, statement: DeclStatement) -> None:
        self.__declarations.add(statement)

    def eval_conditional_statement(self, statement: ConditionalStatement) -> None:
        self.__cond_declarations.add(statement)

    def eval_query_statement(self, statement: QueryStatement) -> None:
        ...

    def get_output(self) -> str:
        return ""

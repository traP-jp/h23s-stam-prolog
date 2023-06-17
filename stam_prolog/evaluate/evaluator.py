from ..ast import ConditionalStatement, DeclStatement, QueryStatement


class Evaluator:
    __slots__ = ("__declarations", "__cond_declarations")

    def __init__(self) -> None:
        self.__declarations: set[DeclStatement] = set()
        self.__cond_declarations: set[ConditionalStatement] = set()

    def eval_decl_statement(self, sentence: DeclStatement) -> None:
        ...

    def eval_conditional_statement(self, sentence: ConditionalStatement) -> None:
        ...

    def eval_query_statement(self, sentence: QueryStatement) -> None:
        ...

    def get_output(self) -> str:
        return ""

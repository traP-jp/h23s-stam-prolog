from .evaluate import Evaluator
from .parser import Parser


def run(src: str) -> str:
    parser = Parser()
    evaluator = Evaluator()
    parsed = parser.parse(src)
    if isinstance(parsed, str):
        return parsed
    for b, p in parsed:
        if b:
            evaluator.eval_query_statement(p)  # type: ignore
        else:
            evaluator.eval_decl_statement(p)  # type: ignore
    return evaluator.get_output()

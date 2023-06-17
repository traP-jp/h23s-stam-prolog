from dataclasses import dataclass

from . import Expression


class Term(Expression):
    pass


@dataclass(frozen=True)
class MulTerm(Term):
    left: Term
    right: Term

    def eval(self) -> int:
        return self.left.eval() * self.right.eval()


@dataclass(frozen=True)
class DivTerm(Term):
    left: Term
    right: Term

    def eval(self) -> int:
        return self.left.eval() // self.right.eval()

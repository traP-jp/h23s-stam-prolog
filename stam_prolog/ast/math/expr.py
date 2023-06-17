from abc import ABC, abstractmethod
from dataclasses import dataclass


class Expression(ABC):
    @abstractmethod
    def eval(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True)
class AddExpression(Expression):
    left: Expression
    right: Expression

    def eval(self) -> int:
        return self.left.eval() + self.right.eval()


@dataclass(frozen=True)
class SubExpression(Expression):
    left: Expression
    right: Expression

    def eval(self) -> int:
        return self.left.eval() - self.right.eval()

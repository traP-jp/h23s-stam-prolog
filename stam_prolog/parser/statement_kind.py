import enum


class StatementKind(enum.Enum):
    NormalDeclaration = enum.auto()
    ConditionalDeclaration = enum.auto()
    NormalQuery = enum.auto()
    ConditionalQuery = enum.auto()

    @classmethod
    def judge(cls, statement: list[str]) -> "StatementKind":
        last = statement[-1]
        include_arrow = ":arrow_right:" in statement
        if last == ":ton:":
            if include_arrow:
                return cls.ConditionalDeclaration
            return cls.NormalDeclaration
        if include_arrow:
            return cls.ConditionalQuery
        return cls.NormalQuery

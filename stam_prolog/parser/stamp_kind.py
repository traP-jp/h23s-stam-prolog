import enum

_NUMBERS = (
    ":one: :two: :three: :four: :five: :six: :seven: :eight: :nine: :zero:".split()
)
_SIGNS = ":heavy_plus_sign: :heavy_minus_sign:".split()
_OPERATORS = [
    ":heavy_plus_sign:",
    ":heavy_minus_sign:",
    ":heavy_multiplication_x:",
    ":heavy_division_sign:",
]


class StampKind(enum.Flag):
    Normal = enum.auto()
    Variable = enum.auto()
    MathNumber = enum.auto()
    MathSign = enum.auto()
    MathOperator = enum.auto()
    ArrowRight = enum.auto()
    And = enum.auto()
    All = Normal | Variable | MathNumber | MathSign | MathOperator | ArrowRight | And

    # スタンプの種類を判定する
    # スタンプ例: ":heart:"
    @classmethod
    def judge(cls, stamp: str) -> "StampKind":
        if len(stamp) == 3:
            # 1文字スタンプ→変数
            return cls.Variable
        if stamp == ":arrow_right:":
            return cls.ArrowRight
        if stamp == ":and:":
            return cls.And
        if stamp in _NUMBERS:
            return cls.MathNumber
        if stamp in _SIGNS:
            return cls.MathSign | cls.MathOperator | cls.Normal
        if stamp in _OPERATORS:
            return cls.MathOperator | cls.Normal
        return cls.Normal

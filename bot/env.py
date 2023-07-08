# 環境変数読み込む系
from dataclasses import dataclass
from os import environ
from typing import Self

from dotenv import dotenv_values


def filter_dict(d: dict, keys: list[str]) -> dict:
    return {k: v for k, v in d.items() if k in keys}


@dataclass(frozen=True)
class Env:
    bot_id: str
    bot_user_id: str
    verification_token: str
    bot_access_token: str

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return cls(
            bot_id=d.get("BOT_ID", "") or d.get("bot_id", ""),
            bot_user_id=d.get("BOT_USER_ID", "") or d.get("bot_user_id", ""),
            verification_token=d.get("VERIFICATION_TOKEN", "")
            or d.get("verification_token", ""),
            bot_access_token=d.get("BOT_ACCESS_TOKEN", "")
            or d.get("bot_access_token", ""),
        )

    @classmethod
    def load(cls) -> Self:
        keys = ["BOT_ID", "BOT_USER_ID", "VERIFICATION_TOKEN", "BOT_ACCESS_TOKEN"]
        # .env.devはデフォルト値
        env_d = {
            **filter_dict(dotenv_values(".env.dev"), keys),
            **filter_dict(dotenv_values(".env"), keys),
            **filter_dict(dict(environ), keys),
        }
        return cls.from_dict(env_d)


if __name__ == "__main__":
    print(Env.load())

from traq_bot import TraqBot

from . import Env, Handler


def main() -> None:
    env = Env.from_env()
    bot = TraqBot(env.verification_token)
    handler = Handler(env.bot_access_token)
    bot.message_created(handler.on_message_created)
    bot.run(8080)


if __name__ == "__main__":
    main()

import json
from typing import Any, Optional

from traq import ApiClient, Configuration
from traq.api.message_api import MessageApi
from traq.model.post_message_request import PostMessageRequest


class Handler:
    __slots__ = ("__client",)

    def __init__(self, access_token: str):
        self.__client = ApiClient(Configuration(access_token))

    def send_message(self, channel_id: str, message: str) -> Any:
        message_api = MessageApi(self.__client)
        req = PostMessageRequest(message)
        res = message_api.post_message(channel_id, post_message_request=req)
        return res

    def on_message_created(self, payload: Optional[dict]) -> None:
        if not payload:
            print("[on_message_created] payload is None")
            return
        print(json.dumps(payload, indent=2))
        message = payload.get("message", None)
        if not isinstance(message, dict):
            print("unexpected input")
            return
        # ここでメッセージを処理する
        res = message["plainText"]
        self.send_message(message["channelId"], res)

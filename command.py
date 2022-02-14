import json

import requests

from core import Message, Bot
from register import register, register_command
from mctools import RCONClient

blank_list = [

]


def not_admin_command(is_admin: bool, commands, text):
    for command in commands:
        if command in text and is_admin is False:
            return True


@register_command("测试")
def test(bot: Bot, message: Message):
    bot.sendGroupMessage(
        target=message.group.group_id,
        text="ces"
    )


@register_command("解除禁言")
def recommand_list_view(bot: Bot, message: Message):
    # command = "".join(message.text.split("禁言")).strip()

    if message.is_at:
        bot.unmute(
            message.group.group_id,
            member_id=message.at_member_id,
        )


@register_command("撤回")
def recommand_list_view(bot: Bot, message: Message):
    # command = "".join(message.text.split("禁言")).strip()

    if message.is_quote:
        bot.recall(message.quote_message_id)
        # bot.recall(message.message_id)


if __name__ == '__main__':
    pass
    # for key, value in register.items():
    #     print(key, value)

    # r = requests.get("https://api88.net/api/img/rand/", allow_redirects=False)
    # print(r.headers.get("Location"))

    # r = requests.get("http://gank.io/images/f12526b3e9654a47842db6ce21222874")
    # print(r.text)
    # bot = Bot(auth_key="12345678", qq=1398231927)
    # bot.sendGroupMessage(
    #     target=618155895,
    #     text="https://www.bilibili.com/video/BV1q64y1Q7eN"
    # )

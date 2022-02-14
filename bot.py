import json
import re
import time
import requests

from config import AUTH_QQ, AUTH_KEY
from core import Bot, Enum_Type
from command import register


bot = Bot(auth_key=AUTH_KEY, qq=int(AUTH_QQ))

while True:
    time.sleep(2)
    fetch = bot.reciveMessage()
    print(fetch.messageBody)

    if fetch.messageType == Enum_Type.GroupMessage:
        for item in fetch.messageBody.get("data"):
            message = bot.parseGroupMessage(item)

            # print(message.message_id)

            for key, value in register.items():
                if message is not None:
                    if message.is_xml:
                        pass

                    if message.text != "" and str(message.text.strip()).startswith(key):
                        register[key]['func'](bot, message)
                        break

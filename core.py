import json

import requests

from config import MIRAI_HTTP_API


class Sender:
    username = None
    qq = None
    permission = None

    def __init__(self, _sender):
        sender = _sender.get("sender")
        self.username = sender['memberName']
        self.qq = sender['id']
        self.permission = sender['permission']

    @property
    def is_owner(self):
        return self.permission == "OWNER"

    @property
    def is_admin(self):
        return self.permission == "ADMINISTRATOR"

    @property
    def is_member(self):
        return self.permission == "MEMBER"


class Gruop:
    group_id = None
    group_name = None
    group_permission = None

    def __init__(self, _group):
        group = _group['sender']['group']
        self.group_id = group['id']
        self.group_name = group['name']
        self.group_permission = group['permission']


class Message:
    is_at = False
    at_member_id = None
    sender = None
    group = None
    text = ""
    message_id = 0
    xml = ""

    is_quote = False
    is_xml = False
    quote_message_id = 0

    def __init__(self, message):
        self.messageChain = message['messageChain']
        self.__init_profile()
        self.sender = Sender(message)
        self.group = Gruop(message)

    def __init_profile(self):
        for item in self.messageChain:
            if item['type'].lower() == "at":
                self.is_at = True
                self.at_member_id = item['target']
            if item['type'].lower() == "plain":
                if item['text'].strip() != "":
                    self.text = item['text']

            if item['type'].lower() == "source":
                self.message_id = item['id']

            if item['type'].lower() == "quote":
                self.is_quote = True
                self.quote_message_id = item['id']

            if item['type'].lower() == "xml":
                self.is_xml = True
                self.xml = item['xml']


class Enum_Type:
    FriendMessage = "FriendMessage"
    GroupMessage = "GroupMessage"


class MessageType:
    messageType = None
    messageBody = None

    def __init__(self, body):
        self.messageBody = body
        data = body.get("data") if "data" in body else []

        if len(data) > 0:
            _type = data[0]['type']

            if _type == "FriendMessage":
                self.messageType = Enum_Type.FriendMessage
            elif _type == "GroupMessage":
                self.messageType = Enum_Type.GroupMessage


class Bot(object):

    def __init__(self, auth_key, qq):
        self.target = MIRAI_HTTP_API
        self.authKey = auth_key
        self.session = None
        self.loginqq = qq

        self.auth()

    def parseGroupMessage(self, body):
        if body['type'] == "GroupMessage":
            return Message(body)
        return None

    def __request(self, path, method, data):
        print(path, method, data)
        # print(path, data)
        if method.lower() == "get":
            r = requests.get(
                self.target + path,
            )
        elif method.lower() == "post":
            r = requests.post(
                self.target + path, json=data
            )
        else:
            r = None

        # print(r.text)
        return r.json()

    def auth(self):
        auth = self.__request(
            "/verify",
            method="POST",
            data={
                "verifyKey": self.authKey
            }
        )
        #
        session = self.__request(
            "/bind",
            method="POST",
            data={
                "sessionKey": auth.get("session"),
                "qq": self.loginqq
            }
        )
        self.session = auth.get("session")
        return session

    def __del__(self):
        r = self.__request(
            path="/release",
            method="POST",
            data={
                "sessionKey": self.session,
                "qq": self.loginqq
            }
        )
        print(r)

    def sendGroupMessage(self,
                         target, text,
                         at_members: list=[], quote=None):
        """
        发送群组消息
        :param target:
        :param message_chain:
        :return:
        """
        messages = []

        for member in at_members:
            messages.append({
                "type": "At",
                "target": member,
                "display": "@ "
            })
        if not isinstance(text, list):
            messages.append({"type": "Plain", "text": text})
        else:
            messages = text

        data = {
            "sessionKey": self.session,
            "target": target,
            "messageChain": messages
        }

        if quote:
            data['quote'] = quote

        send = self.__request(
            "/sendGroupMessage",
            method="POST",
            data=data
        )
        print(send)

    def reciveMessage(self):
        fetch = self.__request(
            path="/fetchMessage?sessionKey={}&count=10".format(self.session),
            method="GET",
            data={}
        )
        return MessageType(fetch)

        # print(fetch)

    def recallMessage(self, message_id):
        recall = self.__request(
            path="/recall",
            method="POST",
            data={
                "sessionKey": self.session,
                "target": message_id
            }
        )
        return

    def sendImageMessage(self, target, image_list):
        send = self.__request(
            path="/sendImageMessage",
            method="POST",
            data={
                "sessionKey": self.session,
                "target": target,
                "group": target,
                "urls": image_list
            }
        )

    def mute(self, group, member_id, time=60):
        mute = self.__request(
            path="/mute",
            method="POST",
            data={
                "sessionKey": self.session,
                "target": group,
                "memberId": member_id,
                "time": time
            }
        )

    def unmute(self, group, member_id):
        unmute = self.__request(
            path="/unmute",
            method="POST",
            data={
                "sessionKey": self.session,
                "target": group,
                "memberId": member_id,
            }
        )

    def recall(self, message_id):
        recall = self.__request(
            path="/recall",
            method="POST",
            data={
                "sessionKey": self.session,
                "target": message_id
            }
        )


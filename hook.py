import json
from email.message import EmailMessage
from email.parser import Parser
from email.policy import EmailPolicy
from os import environ as env
from sys import stdin
from typing import List
from urllib.request import Request, urlopen


def get_plaintext(msg: EmailMessage) -> str:
    texts: List[str] = list()

    part: EmailMessage
    for part in msg.walk():
        if "text/plain" == part.get_content_type():
            texts.append(part.get_content())

    return "\n".join(texts)


msg: EmailMessage = Parser(policy=EmailPolicy()).parse(stdin)

subject: str = msg.get("Subject", "NO SUBJECT")
payload: str = get_plaintext(msg)

#
# Discord API: POST /channels/{channel.id}/messages
#
chid: str = env["DISCORD_CHID"]
token: str = env["DISCORD_TOKEN"]


r: Request = Request(
    url=f"https://discord.com/api/channels/{chid}/messages",
    headers={
        "Authorization": f"Bot {token}",
        "User-Agent": "DiscordBot",
        "Content-Type": "application/json",
    },
    data=json.dumps({"content": f"**{subject}**\n```{payload}```"}).encode(),
)
urlopen(r)

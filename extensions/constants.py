import os
GUILDS = 873460501152165898
PREFIX ="?"


URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
SPOTCLIENT_ID = os.getenv("SPOTID")
SPOTCLIENT_SECRET = os.getenv("SPOTSECRET")
LAVALINK_HOST = "192.168.100.10"
LAVALINK_PORT = 2333
LAVALINK_PASSWORD = "CoolPass"

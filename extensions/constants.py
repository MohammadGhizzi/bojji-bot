import os
TOKEN = os.environ["DISCORD_BOT"]
GUILDS = 873460501152165898
PREFIX ="?"
RAPI = os.environ["RANDOM_API"]

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
SPOTCLIENT_ID = os.getenv("SPOTID")
SPOTCLIENT_SECRET = os.getenv("SPOTSECRET")
LAVALINK_PASSWORD = os.environ["LAVALINK_PASS"]

"""@bojji.listen()
async def hassan(event: hikari.GuildMessageCreateEvent) -> None:
    if event.author_id == 345984665456476163:
        #await event.message.delete()
        await event.message.respond("اسكت ياكولد")"""
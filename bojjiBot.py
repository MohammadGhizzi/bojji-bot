import os
from extensions.constants import GUILDS,PREFIX, LAVALINK_HOST, LAVALINK_PASSWORD, LAVALINK_PORT
import hikari
import lightbulb
import time
import logging
import miru
import random
from lightbulb import commands, context
from lightbulb.ext import tasks
#from utils import LOGCHANNELID
from speech import badword, memoji, re, text
from typing import Final
from extensions.users import hassan, rima, cold

bojji = lightbulb.BotApp(
    default_enabled_guilds=GUILDS,
    ignore_bots=True,
    prefix=lightbulb.when_mentioned_or(PREFIX),
)

bojji.load_extensions('extensions.music')


music_plugin = lightbulb.Plugin("music", "Music Related commands", include_datastore=True)
music_plugin.add_checks(lightbulb.checks.guild_only)



"""@bojji.listen(hikari.StartedEvent)
async def ready_listener(event: hikari.StartedEvent) -> None:
    await bojji.update_presence(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name=f"^________^",
            type=hikari.ActivityType.LISTENING
        )
    )"""


@bojji.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)


@bojji.listen(hikari.StartedEvent)
async def on_starting(event):
    print("bot has started")

@bojji.listen()
async def hassan(event: hikari.GuildMessageCreateEvent) -> None:
    if event.author_id == 605049087527747585:
        await event.message.add_reaction("😡")
    if event.author_id == 275654737695604736:
        await event.message.add_reaction("😡")

        
@bojji.listen()
async def hassan(event: hikari.GuildMessageCreateEvent) -> None:
    if event.author_id == 345984665456476163:
        await event.message.delete()
        await event.message.respond("اسكت ياكولد")
"""    if event.author_id == nawaf:
        await event.message.delete()
        await event.message.respond("اسكت يانواف")"""
        
@bojji.listen()
async def memo(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return
    if event.content.startswith(text):
        await event.message.respond(random.choice(memoji))
    


@bojji.listen()
async def reaction(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return
    if event.content.startswith(text):
        await event.message.add_reaction(random.choice(re))
    elif event.content.startswith(badword):
        await event.message.respond("عيب")
        await event.message.add_reaction("😡")


images = os.path.join(os.getcwd(), "gif")
def select_random_image_path():
    return os.path.join(images, random.choice(os.listdir(images)))

ctx = lightbulb.context
@bojji.command
@lightbulb.command('bojji', 'Random Bojji GIF')
@lightbulb.implements(lightbulb.SlashCommand)
async def image(ctx):
    f = hikari.File(select_random_image_path())
    await ctx.respond(f)
        
        
bojji.run(os.environ("DISCORD_BOT"))

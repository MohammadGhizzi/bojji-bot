import hikari
import logging
from typing import Optional

#from discord import channel

from extensions.constants import LAVALINK_PASSWORD, PREFIX, TOKEN
import lightbulb
import lavasnek_rs


class EventHandler:
    """Events from lavalink server """

    async def track_start(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
        logging.info("Track started on guild: %s", event.guild_id)

    async def track_finish(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
        logging.info("Track finished on guild: %s", event.guild_id)

    async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:
        logging.warning("Track exception event happened on guild: %d", event.guild_id)

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not node:
            return

        if skip and not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)


plugin = lightbulb.Plugin("Music")


def load(bojji):
    bojji.add_plugin(plugin)


async def _join(ctx: lightbulb.Context) -> Optional[hikari.Snowflake]:
    assert ctx.guild_id is not None

    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("ما أشوفك بالفويس تشانل")
        return None

    channel_id = voice_state.channel_id

    assert channel_id is not None

    await plugin.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True)
    connection_info = await plugin.bot.d.lavalink.wait_for_full_connection_info_insert(ctx.guild_id)

    await plugin.bot.d.lavalink.create_session(connection_info)

    return channel_id


@plugin.listener(hikari.ShardReadyEvent)
async def start_lavalink(event: hikari.ShardReadyEvent) -> None:
    """Event that triggers when the hikari gateway is ready."""
    builder = (  # TOKEN can be an empty string if you don't want to use lavasnek's discord gateway.
        lavasnek_rs.LavalinkBuilder(event.my_user.id, TOKEN)
            # This is the default value, so this is redundant, but it's here to show how to set a custom one.
            .set_host("127.0.0.1").set_password("CoolPass").set_port(2333)
    )
    builder.set_start_gateway(False)
    lava_client = await builder.build(EventHandler())
    plugin.bot.d.lavalink = lava_client


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("join", "Joins the user vc")
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def join(ctx: lightbulb.Context) -> None:
    channel_id = await _join(ctx)

    if channel_id:
        await ctx.respond(f"هاي <#{channel_id}>")


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("leave", "Leaves the vc")
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def leave(ctx: lightbulb.Context) -> None:
    await plugin.bot.d.lavalink.destroy(ctx.guild_id)

    await plugin.bot.update_voice_state(ctx.guild_id, None)
    await plugin.bot.d.lavalink.wait_for_connection_info_remove(ctx.guild_id)
    # line 100 freom the examples
    await ctx.respond("باي")


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("query", "query to search for", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("play", "رابط او اسم المقطع")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def play(ctx: lightbulb.Context) -> None:
    """Searches the query on youtube, or adds the URL to the queue."""

    query = ctx.options.query

    if not query:
        await ctx.respond("Please specify a query.")
        return None

    con = plugin.bot.d.lavalink.get_guild_gateway_connection_info(ctx.guild_id)
    # Join the user's voice channel if the bot is not in one.
    if not con:
        await _join(ctx)
    # Search the query, auto_search will get the track from a url if possible, otherwise,
    # it will search the query on youtube.
    query_information = await plugin.bot.d.lavalink.auto_search_tracks(query)

    if not query_information.tracks:  # if track is empty
        await ctx.respond("Could not find anything")
        return
    try:
        # `.requester()` To set who requested the track, so you can show it on now-playing or queue.
        # `.queue()` To add the track to the queue rather than starting to play the track now.
        await plugin.bot.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
    except lavasnek_rs.NoSessionPresent:
        await ctx.respond(f"Use '{PREFIX}join' first")
        return

    await ctx.respond(f"Added to queue: {query_information.tracks[0].info.title}")


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("stop", "يوقف الأغنية الحالية (استخدم سكيب عشان يكمل الاغنية اللي عقبها)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def stop(ctx: lightbulb.Context) -> None:
    """Stops the current song (skip to continue)."""

    await plugin.bot.d.lavalink.stop(ctx.guild_id)
    await ctx.respond("تم")


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("skip", "سكب للأغنية")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def skip(ctx: lightbulb.Context) -> None:
    """Skips the current song."""

    skip = await plugin.bot.d.lavalink.skip(ctx.guild_id)
    node = await plugin.bot.d.lavalink.get_guild_node(ctx.guild_id)

    if not skip:
        await ctx.respond("مافي شي يشتغل")
    else:
        # If the queue is empty, the next track won't start playing (because there isn't any),
        # so we stop the player.
        if not node.queue and not node.now_playing:
            await plugin.bot.d.lavalink.stop(ctx.guild_id)

        await ctx.respond(f"تم: {skip.track.info.title}")


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("pause", "يوقف مؤقتا.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def pause(ctx: lightbulb.Context) -> None:
    """Pauses the current song."""

    await plugin.bot.d.lavalink.pause(ctx.guild_id)
    await ctx.respond("Paused player")


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("resume", "Resumes playing the current song.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def resume(ctx: lightbulb.Context) -> None:
    """Resumes playing the current song."""

    await plugin.bot.d.lavalink.resume(ctx.guild_id)
    await ctx.respond("Resumed player")


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("nowplaying", "Gets the song that's currently playing.", aliases=["np"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def now_playing(ctx: lightbulb.Context) -> None:
    """Gets the song that's currently playing."""

    node = await plugin.bot.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        await ctx.respond("Nothing is playing at the moment.")
        return

    # for queue, iterate over `node.queue`, where index 0 is now_playing.
    await ctx.respond(f"Now Playing: {node.now_playing.track.info.title}")


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.owner_only)  # Optional
@lightbulb.option(
    "args", "The arguments to write to the node data.", required=False, modifier=lightbulb.OptionModifier.CONSUME_REST
)
@lightbulb.command("data", "Load or read data from the node.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def data(ctx: lightbulb.Context) -> None:
    """Load or read data from the node.
    If just `data` is ran, it will show the current data, but if `data <key> <value>` is ran, it
    will insert that data to the node and display it."""

    node = await plugin.bot.d.lavalink.get_guild_node(ctx.guild_id)

    if not node:
        await ctx.respond("No node found.")
        return None

    if args := ctx.options.args:
        args = args.split(" ")

        if len(args) == 1:
            node.set_data({args[0]: args[0]})
        else:
            node.set_data({args[0]: args[1]})
    await ctx.respond(node.get_data())


@plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    plugin.bot.d.lavalink.raw_handle_event_voice_state_update(
        event.state.guild_id,
        event.state.user_id,
        event.state.session_id,
        event.state.channel_id,
    )


@plugin.listener(hikari.VoiceServerUpdateEvent)
async def voice_server_update(event: hikari.VoiceServerUpdateEvent) -> None:
    await plugin.bot.d.lavalink.raw_handle_event_voice_server_update(event.guild_id, event.endpoint, event.token)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)

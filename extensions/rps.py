import hikari
import miru
import lightbulb


plugin = lightbulb.Plugin("Rps")



class MyView(miru.View):

    @miru.button(label="Rock", emoji=chr(129704), style=hikari.ButtonStyle.PRIMARY)
    async def rock_button(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.respond("Paper!")

    @miru.button(label="Paper", emoji=chr(128220), style=hikari.ButtonStyle.PRIMARY)
    async def paper_button(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.respond("Scissors!")

    @miru.button(label="Scissors", emoji=chr(9986), style=hikari.ButtonStyle.PRIMARY)
    async def scissors_button(self, button: miru.Button, ctx: miru.Context):
        await ctx.respond("Rock!")

    @miru.button(emoji=chr(9209), style=hikari.ButtonStyle.DANGER, row=2)
    async def stop_button(self, button: miru.Button, ctx: miru.Context):
        self.stop() # Stop listening for interactions


@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("rps", "play rps with bojji]")
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    if event.is_bot or not event.content:
        return

    if event.content.startswith("miru"):
        view = MyView(timeout=60)  # Create a new view
        message = await event.message.respond("Rock Paper Scissors!", components=view.build())
        view.start(message)  # Start listening for interactions
        await view.wait() # Wait until the view times out or gets stopped
        await event.message.respond("Thank you for playing!")


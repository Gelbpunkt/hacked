import discord
import traceback
import sys
import datetime
from discord.ext import commands
from checks import *


class Events:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.Forbidden):
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NotOwner):
            return await ctx.send("You're not the owner of this bot.")
        elif isinstance(error, NeedsAcc):
            return await ctx.send(f"You need an account to use this command.")
        elif isinstance(error, NoAcc):
            return await ctx.send("You need to have no account to use this command.")
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(
                f"Cooldown! Wait {str(datetime.timedelta(seconds=error.retry_after)).split('.')[0]} and try again."
            )
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )


def setup(bot):
    bot.add_cog(Events(bot))

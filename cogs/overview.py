import discord
from discord.ext import commands
from checks import *


class Overview:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tasks(self, ctx):
        """Lists all available tasks."""
        tasks = "\n".join(f"Task {i}: {j[0]}" for i, j in self.bot.data.tasks.items())
        await ctx.send(tasks)

    @acc()
    @commands.command()
    async def settask(self, ctx, task: int):
        """Change your current task."""
        if not task in self.bot.data.tasks:
            return await ctx.send(f"{task} is not a vaild task number.")
        await self.bot.pool.execute(
            'UPDATE hacked SET task=$1 WHERE "user"=$2;', task, ctx.author.id
        )
        await ctx.send(
            f"Your new task is now {task}. Use `{ctx.prefix}task` to view it."
        )


def setup(bot):
    bot.add_cog(Overview(bot))

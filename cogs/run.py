import discord
import textwrap
import aiofiles
from discord.ext import commands
from checks import *


class Run:
    def __init__(self, bot):
        self.bot = bot

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        content = content.lstrip("\n").rstrip("\n")
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(l for l in content.split("\n")[1:] if l != "\n").rstrip(
                "```"
            )

        # remove `foo`
        return content.strip("` \n")

    def check_sum(self, code):
        opening = tuple("({[")
        closing = tuple(")}]")
        mapping = dict(zip(opening, closing))
        queue = []

        for letter in code:
            if letter in opening:
                queue.append(mapping[letter])
            elif letter in closing:
                if not queue or letter != queue.pop():
                    return False
        return not queue

    def make_code(self, pre, code):
        code = textwrap.indent(code, "    ")
        code = f"function main(input) {{\n{code}\n    return output;\n}}\nsay(main({pre}));"
        return code

    @no_acc()
    @commands.command()
    async def start(self, ctx):
        await self.bot.pool.execute(
            'INSERT INTO hacked ("user", "task") VALUES ($1, $2);', ctx.author.id, 1
        )
        await ctx.send(self.bot.data.msg)

    @acc()
    @commands.command()
    async def task(self, ctx):
        val = await self.bot.pool.fetchval(
            'SELECT task FROM hacked WHERE "user"=$1;', ctx.author.id
        )
        try:
            await ctx.send(self.bot.data.levels[val][0])
        except KeyError:
            await ctx.send("You finished all levels.")

    @acc()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command()
    async def solve(self, ctx, *, code: str):
        code = self.cleanup_code(code)
        if not self.check_sum(code):
            return await ctx.send("You have left-open brackets!")
        val = await self.bot.pool.fetchval(
            'SELECT task FROM hacked WHERE "user"=$1;', ctx.author.id
        )
        try:
            input = self.bot.data.levels[val][1]
        except KeyError:
            return await ctx.send("You finished all levels.")
        for i in input:
            c = self.make_code(i[0], code)
            async with aiofiles.open(f"users/u{ctx.author.id}.mb", mode="w") as f:
                await f.write(c)
            o = (
                await self.bot.shell.run(
                    f"/home/jens/.local/bin/mamba users/u{ctx.author.id}.mb -l"
                )
            ).stdout
            if "Undefined variable 'output'" in o:
                # await ctx.send(f"{c}, {o}")
                return await ctx.send("You did not define `output`!")
            l = o.split("\n")[-2]
            if l != str(i[1]):
                return await ctx.send(
                    f"Your code didn't meet a test! We tested it with the input `{str(i[0])}` and got `{l}`! Expected output was `{i[1]}`.\n\nFull output below:\n```sh\n{o}```"
                )
        await self.bot.pool.execute(
            'UPDATE hacked SET task=task+1 WHERE "user"=$1;', ctx.author.id
        )
        await ctx.send("Correct code! You have a new task available!")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command()
    async def run(self, ctx, *, code: str):
        code = self.cleanup_code(code)
        async with aiofiles.open(f"users/u{ctx.author.id}.mb", mode="w") as f:
            await f.write(code)
        o = (
            await self.bot.shell.run(
                f"/home/jens/.local/bin/mamba users/u{ctx.author.id}.mb -l"
            )
        ).stdout
        await ctx.send(f"```sh\n{o}\n```")


def setup(bot):
    bot.add_cog(Run(bot))

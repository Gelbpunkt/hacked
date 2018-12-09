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

    def make_code(self, pre, code):
        """Make the code for ///solve"""
        code = textwrap.indent(code, "    ")
        code = f"function main(input) {{\n{code}\n    return output;\n}}\nsay(main({pre}));"
        return code

    async def run_code(self, code, identifier):
        """Runs our code using a new file for it."""
        async with aiofiles.open(f"users/u{identifier}.mb", mode="w") as f:
            await f.write(c)
        return (await self.bot.shell.run(f"mamba users/u{identifier}.mb -l")).stdout

    @no_acc()
    @commands.command()
    async def start(self, ctx):
        """Make an account for playing hacked."""
        await self.bot.pool.execute(
            'INSERT INTO hacked ("user", "task") VALUES ($1, $2);', ctx.author.id, 1
        )
        await ctx.send(self.bot.data.msg.format(ctx.prefix))

    @acc()
    @commands.command()
    async def task(self, ctx):
        """View your current task."""
        val = await self.bot.pool.fetchval(
            'SELECT task FROM hacked WHERE "user"=$1;', ctx.author.id
        )
        try:
            await ctx.send(self.bot.data.tasks[val][1].format(ctx.prefix))
        except KeyError:
            await ctx.send("You finished all levels.")

    @acc()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command()
    async def solve(self, ctx, *, code: str):
        """Solve your current task."""
        code = self.cleanup_code(code)
        val = await self.bot.pool.fetchval(
            'SELECT task FROM hacked WHERE "user"=$1;', ctx.author.id
        )
        try:
            input = self.bot.data.tasks[val][2]
        except KeyError:
            return await ctx.send("You finished all levels.")
        for i in input:
            c = self.make_code(i[0], code)
            o = await self.run_code(c, ctx.author.id)
            if "Undefined variable 'output'" in o:
                return await ctx.send("You did not define `output`!")
            elif (
                "illegal token 'return' found" in o
            ):  # most likely that they forgot the colon
                return await ctx.send("You're missing a `;` at your last line.")
            l = o.split("\n")[-2]
            if l != str(i[1]):
                return await ctx.send(
                    f"Your code didn't meet a test! We tested it with the input `{str(i[0])}` and got `{l}`! Expected output was `{i[1]}`.\n\nFull output below:\n```sh\n{o}```"
                )
        await self.bot.pool.execute(
            'UPDATE hacked SET task=task+1 WHERE "user"=$1;', ctx.author.id
        )
        await ctx.send("Correct code! You have a new task available!")

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command()
    async def run(self, ctx, *, code: str):
        """Run Mamba code."""
        code = self.cleanup_code(code)
        o = await self.run_code(code, ctx.author.id)
        await ctx.send(f"```sh\n{o}\n```")


def setup(bot):
    bot.add_cog(Run(bot))

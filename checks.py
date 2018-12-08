from discord.ext import commands


class NeedsAcc(commands.CheckFailure):
    pass


class NoAcc(commands.CheckFailure):
    pass


def acc():
    async def predicate(ctx):
        if await ctx.bot.pool.fetchrow(
            'SELECT * FROM hacked WHERE "user"=$1;', ctx.author.id
        ):
            return True
        raise NeedsAcc()

    return commands.check(predicate)


def no_acc():
    async def predicate(ctx):
        if not await ctx.bot.pool.fetchrow(
            'SELECT * FROM hacked WHERE "user"=$1;', ctx.author.id
        ):
            return True
        raise NoAcc()

    return commands.check(predicate)

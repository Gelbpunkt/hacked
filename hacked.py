import discord
import asyncio
import config
import mamba
import aioshell
import aiohttp
import asyncpg
from discord.ext import commands
import data

bot = commands.Bot(command_prefix="///", case_insensitive=True)
bot.owners = [356091260429402122]


@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    await bot.process_commands(msg)


@bot.event
async def on_ready():
    print("hacked. is ready")


async def start():
    bot.data = data
    bot.config = config
    bot.shell = aioshell
    bot.load_extension("jishaku")
    bot.pool = await asyncpg.create_pool(**config.db)
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    for i in config.exts:
        bot.load_extension(i)
    await bot.start(config.token)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())

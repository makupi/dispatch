import os

from utils import monkey_patch, Context
from discord.ext import commands
from dotenv import load_dotenv

monkey_patch()
load_dotenv()

bot = commands.Bot(command_prefix="?")


@bot.command()
async def test(ctx: Context):
    answer = await ctx.ask("Do you like dpy-utils?")
    print(answer)


bot.run(os.getenv("TOKEN"))

import utils
import discord
from discord.ext import commands
from dotenv import load_dotenv

utils.monkey_patch()
load_dotenv()

bot = commands.Bot()


@bot.command()
async def ask(ctx: utils.Context):
    answer = await ctx.ask("Do you like dpy-utils?")
    print(answer)


@bot.command()
async def paginate(ctx: utils.Context, size: int = 5):
    embeds = list()
    for index in range(size):
        embeds.append(discord.Embed(description=f"Embed #{index}\n\n\ntest embed"))

    paginator = utils.Paginator(ctx, embeds)
    await paginator.start()


bot.run()

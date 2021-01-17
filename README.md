# dis.patch
*A [discord.py](https://github.com/rapptz/discord.py) utility library.*


> ## Warning
> 
> This is a very early alpha version. There might be some unknown issues.

## Features
- custom Context with additional features like `ctx.ask`
- patched `Bot` and `AutoShardedBot` classes:
  - use custom Context
  - automatically loads token and prefix from `.env` file
  - automatically loads cogs/extensions if `cogs_path` is passed (e.g. `cogs_path="bot/cogs"`)
      
- `monkey_patch()` to overwrite `discord.py` classes with `dispatch`

## Installation
```
pip install dis.patch
```


## Usage
*.env*
```env
TOKEN=token
PREFIX=?
```

*bot.py*
```py
import dispatch
from discord.ext import commands

dispatch.monkey_patch()

bot: dispatch.Bot = commands.Bot(cogs_path="bot/cogs")


@bot.command()
async def test(ctx: dispatch.Context):
    answer = await ctx.ask("Do you like dispatch?")
    print(answer)


bot.run()
```


## Requirements
- Python >= 3.6
- [pydantic](https://github.com/samuelcolvin/pydantic)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [discord.py](https://github.com/rapptz/discord.py)

## Contributing and Issues
If you want to contribute or want to suggest additional features please use [github issues](https://github.com/makupi/dispatch/issues).


[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A015HXK)

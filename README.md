# dpy-utils
*A [discord.py](https://github.com/rapptz/discord.py) utility library.*


> ## Warning
> 
> This is a very early alpha version. There might be some unknown issues.

## Features
- custom Context with additional features like `ctx.ask`
- patched `Bot` and `AutoShardedBot` classes that that use the custom Context
- patched `Bot` automatically loads token and prefix from `.env` file
- `monkey_patch()` to overwrite `discord.py` classes with `dpy-utils`

## Installation
```
pip install dpy-utils
```


## Usage
*.env*
```env
TOKEN=token
PREFIX=?
```

*bot.py*
```py
import os

import utils
from discord.ext import commands

utils.monkey_patch()

bot: utils.Bot = commands.Bot()


@bot.command()
async def test(ctx: utils.Context):
    answer = await ctx.ask("Do you like dpy-utils?")
    print(answer)


bot.run()
```


## Requirements
- Python >= 3.6
- [pydantic](https://github.com/samuelcolvin/pydantic)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [discord.py](https://github.com/rapptz/discord.py)

## Contributing and Issues
If you want to contribute or want to suggest additional features please use [github issues](https://github.com/makupi/dpy-utils/issues).


[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A015HXK)

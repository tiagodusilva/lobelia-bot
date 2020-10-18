import cogs.utils.bot_macros as macros

import discord
import os, sys, traceback

from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='x! ', intents=intents, description='IEEExtreme Bot')
token_file = "token.txt"

try:
    with open(token_file) as f:
        TOKEN = f.read()
except:
    TOKEN = os.environ.get('TOKEN')

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nDiscord.py version: {discord.__version__}\n')

    # await bot.change_presence(activity=discord.Activity(type=5, name="Energy drink comsumption 🔋"))
    await bot.change_presence(activity=discord.Activity(type=0, name="x! help"))

    print(f'Successfully logged in and booted...!')

# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.teams',
                        'cogs.others',
                        'cogs.admin',
                        'cogs.events']

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()



bot.run(TOKEN, bot=True, reconnect=True)

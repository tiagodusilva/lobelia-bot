import cogs.utils.botMacros as macros

import os, random

import discord
from discord.ext import commands

class OthersCog(commands.Cog, name="Other"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['commandlist', 'commands', 'h'], hidden=True)
    async def _help(self, ctx):
        await ctx.send_help()

    @commands.command(aliases=["d"])
    async def dice(self, ctx, sides :int):
        """Throws an N sided dice"""
        if (sides < 1):
            return

        if (len(str(sides)) >= 1980):
            await ctx.send("Were you trying to pull a 20m radius Emerald Splash on me? 👀")
            return

        await ctx.send(f"You rolled {random.randrange(1, sides + 1)}!")
        pass

    @commands.command()
    async def info(self, ctx):
        """Info about the bot"""
        embed = discord.Embed(
            title="Xtreme Bot",
            url='https://github.com/tiagodusilva/XtremeBot',
            type="rich",
            description="My code is open source and can be found here!",
            colour=discord.Colour(0x0051A0)
        )
        embed.add_field(name="Author", value="Tiago Silva")
        embed.add_field(name="Version 1.01", value="Now 20% more useless!")
        
        await ctx.send(embed=embed)


# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(OthersCog(bot))

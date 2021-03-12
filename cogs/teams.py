from cogs.utils.dbInterface import DbInterface as DB
import cogs.utils.botMacros as macros

import discord
from discord.ext import commands

class TeamsCog(commands.Cog, name="Teams"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def evict(self, ctx):

        """Blocks access to the team's voice channel
        Must be sent from the team's text channel"""

        team = DB.get_team_from_text_channel(ctx.guild.id, ctx.channel.id)
        if (team == None):
            await ctx.send(macros.FORBIDDEN_EMOTE + " This channel doesn't belong to a team!")
            return

        channel = discord.utils.get(ctx.guild.voice_channels, id=team.voice_channel_id)

        for member in channel.members:
            if member.guild_permissions.administrator:
                continue
            member_team = DB.get_member_team(ctx.guild.id, member)
            if (member_team == None) or (team.team_id != member_team.team_id):
                await member.move_to(None)

        await ctx.send("Evicted non-team members")


    @commands.command()
    @commands.guild_only()
    async def lock(self, ctx):

        """Blocks access to the team's voice channel
        Must be sent from the team's text channel"""

        team = DB.get_team_from_text_channel(ctx.guild.id, ctx.channel.id)
        if (team == None):
            await ctx.send(macros.FORBIDDEN_EMOTE + " This channel doesn't belong to a team!")
            return

        channel = discord.utils.get(ctx.guild.voice_channels, id=team.voice_channel_id)
        await channel.set_permissions(ctx.guild.default_role, view_channel=False, connect=False)

        await ctx.send("Locked voice channel")


    @commands.command()
    @commands.guild_only()
    async def unlock(self, ctx):
        
        """Allows anyone into the team's voice channel
        Must be sent from the team's text channel"""

        team = DB.get_team_from_text_channel(ctx.guild.id, ctx.channel.id)
        if (team == None):
            await ctx.send(macros.FORBIDDEN_EMOTE + " This channel doesn't belong to a team!")
            return

        channel = discord.utils.get(ctx.guild.voice_channels, id=team.voice_channel_id)
        await channel.set_permissions(ctx.guild.default_role, view_channel=True, connect=True)

        await ctx.send("Unlocked voice channel")


    @commands.command(aliases=['setTeamColour'])
    @commands.guild_only()
    async def setTeamColor(self, ctx, role: discord.Role, colour: discord.Colour):
        """Sets the color for the team role from hex
        Can only be used by admins or team members"""
        if (ctx.author.guild_permissions.administrator or discord.utils.get(ctx.author.roles, id=role.id)):
            await role.edit(colour=colour)
        else:
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins or team members can change that role")


    @commands.command(aliases=['setTeamColourRGB'])
    @commands.guild_only()
    async def setTeamColorRGB(self, ctx, role: discord.Role, r :int, g :int, b :int):
        """Sets the color for the team role from RGB (0-255)
        Can only be used by admins or team members"""
        colour = discord.Colour.from_rgb(r, g, b)
        if (ctx.author.guild_permissions.administrator or discord.utils.get(ctx.author.roles, id=role.id)):
            await role.edit(colour=colour)
        else:
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins or team members can change that role")


    # @commands.command()
    # @commands.guild_only()
    # async def listTeams(self, ctx):

    #     """Prints a list of all teams and members"""

    #     message = ""
    #     for team in DB.getTeams(ctx.guild.id):
    #         message += f"\n{team[1]}:"
    #         for member in ctx.guild.members:
    #             if discord.utils.get(member.roles, name=team[1] ) != None:
    #                 message += f"\n\t{member.display_name}"

    #     message_pos = 0
    #     while (len(message) - message_pos > macros.CHARACTER_LIMIT):
    #         await ctx.send(message[message_pos:message_pos + macros.CHARACTER_LIMIT])
    #         message_pos += macros.CHARACTER_LIMIT
    #     await ctx.send(message[message_pos:])

# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(TeamsCog(bot))

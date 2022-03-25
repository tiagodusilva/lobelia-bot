import discord
from discord.ext import commands

import cogs.utils.botMacros as macros
from cogs.utils.dbInterface import DbInterface as DB

class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def deleteTeam(self, ctx, role: discord.Role, s = ""):
        
        """Deletes a team
        Deletes a team's role from the server
        If an optional string '--channels' is given, the team's text and voice channels will also be deleted
        """

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return

        team = DB.get_team_from_role(ctx.guild.id, role.id)
        if team != None:
            DB.delete_team(team.team_id)
            await role.guild.system_channel.send(f"Warning: Role {role.name} was deleted by {ctx.author.mention}")
        
            if s == "--channels":
                await ctx.guild.get_channel(team.text_channel_id).delete()
                await ctx.guild.get_channel(team.voice_channel_id).delete()
                await ctx.guild.get_channel(team.category_channel_id).delete()
                await role.guild.system_channel.send(f"Warning: Channels of role {role.name} were deleted by {ctx.author.mention}")
            

    @commands.command()
    @commands.guild_only()
    async def addTeam(self, ctx, roleName):

        """Add a team to the server
        -> Creates role (if it doesn't exist)
        -> Adds role to internal database
        -> Creates team channels and sets their permissions"""

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return

        warnings = ""
        roleName = f"Team {roleName}"

        # Find/Create Role
        existingTeam = DB.get_team_from_name(ctx.guild.id, roleName)
        if (existingTeam != None):
            await ctx.send(f"{roleName} already exists in database: Aborting")
            return

        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if (role != None):
            warnings += f"Warning: Role for {roleName} already exists\n"
        else:
            try:
                role = await ctx.guild.create_role(name=roleName, hoist=True, mentionable=True, reason=f"{ctx.author.display_name} ran the addTeam command")
            except:
                await ctx.send(warnings + f"Failed to create role for {roleName}: Aborting")
                return

        category, textChannel, voiceChannel = None, None, None
        # Create channels and set their permissions
        if (discord.utils.get(ctx.guild.voice_channels, name=roleName)):
            warnings += f"Warning: Channels for {roleName} may already exist\n"
        else:
            try:
                categoryOverwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    ctx.guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True, manage_permissions=True, manage_messages=True),
                    role: discord.PermissionOverwrite(view_channel=True)
                }

                textChannelOverwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    ctx.guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True, manage_permissions=True, manage_messages=True),
                    role: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, read_messages=True)
                }

                voiceChannelOverwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
                    ctx.guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True, manage_permissions=True, manage_messages=True),
                    role: discord.PermissionOverwrite(view_channel=True, connect=True)
                }   

                category = await ctx.guild.create_category_channel(roleName, overwrites=categoryOverwrites)
                textChannel = await category.create_text_channel(roleName, overwrites=textChannelOverwrites)
                voiceChannel = await category.create_voice_channel(roleName, overwrites=voiceChannelOverwrites)
            except:
                await ctx.send(warnings + "Failed to create channels: Aborting")
                return

            await textChannel.send(f"""Welcome to {role.mention}!
    This is your own private channel that can only be seen by you and the admins!
    
    Your respective voice channel is initially locked, but you can open it to allow anyone else to join via the `{macros.BOT_PREFIX}lock` and `{macros.BOT_PREFIX}unlock` commands!
    If anyone is in your voice channel and you wish they no longer were, look no further, as you can evict anyone who isn't a member of your team via the `{macros.BOT_PREFIX}unlock` command.
    
    Everyone loves to add their personal visual flare, so customize your team's color with the `{macros.BOT_PREFIX}setTeamColor` or `{macros.BOT_PREFIX}setTeamColor` commands!
    
    To learn more about these commands use `{macros.BOT_PREFIX}help Teams`""")
            
        # Add team to database
        try:
            DB.add_team(ctx.guild.id, roleName, role.id, category.id, textChannel.id, voiceChannel.id)
        except:
            await ctx.send(warnings + "Error in database: Aborting")
            return
        
        if warnings != "":
            await ctx.send(warnings.rstrip('\n'))
        
        await ctx.message.add_reaction(macros.CONFIRMATION_EMOTE)


    @commands.command(aliases=['teamRoleReact', 'trr'])
    @commands.guild_only()
    async def teamRoleReaction(self, ctx, role: discord.Role):

        """Sends a message to assign teams based on reacts
        The bot will send a message and anyone who reacts to it will get assigned/unassigned to the corresponding team
        If a user attempts to join multiple teams, will get unassigned from the previous one
        This command is admin only"""

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return
        
        team = DB.get_team_from_role(ctx.guild.id, role.id)
        if team == None:
            await ctx.send(f"{macros.FORBIDDEN_EMOTE} Role {role.name} does not correspond to a team!")
            return

        message = await ctx.send(f"To enter {role.mention} use the {macros.REACT_EMOTE} react below!\nWarning: Joining another team will get you unassigned from the previous one")
        await message.add_reaction(macros.REACT_EMOTE)

        try:
            DB.add_team_role_reaction(ctx.guild.id, message.id, ctx.channel.id, team.team_id)
        except:
            await message.delete()
            return
        
        # await ctx.message.delete()


    @commands.command()
    @commands.guild_only()
    async def disableRoleReactions(self, ctx):

        """Disables all previous role reactions
        All role reactions in this channel will be edited to mention they are no longer valid and any reacts on them will be ignored
        This command is admin only"""

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return

        messages = DB.get_team_role_reaction_channel_messages(ctx.guild.id, ctx.channel.id)

        try:
            DB.delete_role_reaction_from_channel(ctx.guild.id, ctx.channel.id)
        except:
            await ctx.send("Failed to commit database transaction: Aborting")
            return

        for p in messages:
            message = await ctx.channel.fetch_message(p[0])
            await message.edit(content=f"{macros.FORBIDDEN_EMOTE} < DEACTIVATED >\n{message.content}")

        await ctx.send("All previous messages are now invalid")



# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(AdminCog(bot))

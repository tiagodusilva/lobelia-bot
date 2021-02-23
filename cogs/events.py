from cogs.utils.dbInterface import DbInterface as DB
import cogs.utils.botMacros as macros

import discord
from discord.ext import commands


class EventsCog(commands.Cog, name="Events"):

    def __init__(self, bot):
        self.bot = bot

    async def on_raw_reaction(self, payload):
        # Only listen to reactions on messages made by the bot and whose emote matches 
        if (payload.user_id == macros.BOT_ID or not payload.emoji.name in macros.REACTS):
            return None, None, None

        message_ids = DB.get_message_react_pairs(payload.guild_id)

        role_id = None
        # Check if it's one of the messages we're listening to
        for m_id in message_ids:
            if (m_id[0] == payload.message_id):
                role_id = m_id[2]
                break
        else:
            # RuntimeError("Message id not found in database")
            return None, None, None

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)

        return guild, member, role

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):
        try:
            guild, member, role = await self.on_raw_reaction(payload)

            old_role = DB.getMemberTeamRole(payload.guild_id, member.roles)

            if (old_role != None):
                await member.remove_roles(old_role)
                await member.add_roles(role)
                await guild.system_channel.send(f"Member {member.name} changed from team {old_role.name} to team {role.name}")
            else:
                await guild.system_channel.send(f"Member {member.name} joined team {role.name}")
                await member.add_roles(role)
        except:
            pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_remove(self, payload):
        try:
            guild, member, role = await self.on_raw_reaction(payload)
            await member.remove_roles(role)
            await guild.system_channel.send(f"Member {member.name} left team {role.name}")
        except:
            pass


    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_role_delete(self, role):
        if (DB.roleIsTeam(role.guild.id, role.id)):
            DB.deleteTeamRole(role.guild.id, role.id)
            DB.deleteRoleReaction(role.guild.id, role.id)
            print(f"Warning: Deleted role {role.name} from guild {role.guild.name} with id {role.guild.id}")
    
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_role_update(self, before, after):
        if (before.name == after.name or not DB.roleIsTeam(before.guild.id, before.id)):
            return
        
        DB.updateTeamName(before.guild.id, before.id, after.name)
        print(f"Update database role name of {before.name} to {after.name} from guild {before.guild.name}")

        for channel in before.guild.channels:
            if (channel.name == f"team-{before.name}"):
                await channel.edit(name=f"team-{after.name}")

    # @commands.Cog.listener()
    # @commands.guild_only()
    # async def on_member_join(self, member: discord.Member):
    #     await member.guild.text_channels[0].send(f"Welcome to {member.guild.name} {member.mention}")


# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(EventsCog(bot))

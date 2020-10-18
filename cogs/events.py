from cogs.utils.db_interactor import DbInteractor as DB
import cogs.utils.bot_macros as macros

import discord
from discord.ext import commands


class EventsCog(commands.Cog, name="Events"):

    def __init__(self, bot):
        self.bot = bot

    async def on_raw_reaction(self, payload):
        # Only listen to 'eject' emote reactions
        if (payload.emoji.name != macros.REACT_EMOTE or payload.user_id == macros.BOT_ID):
            return

        message_ids = DB.get_message_react_pairs(payload.guild_id)

        role_id = None
        # Check if it's one of the messages we're listening to
        for m_id in message_ids:
            if (m_id[0] == payload.message_id):
                role_id = m_id[2]
                break
        else:
            RuntimeError("Message id not found in database")

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


# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(EventsCog(bot))

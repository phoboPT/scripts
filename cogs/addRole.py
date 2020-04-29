from discord.ext import commands
import discord


class Role(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Role command initialized")

    def cog_unload(self):
        print("Unload role command")

    @commands.command(name="role", help='Add the price notify role', description='Just call me an i will give you the PriceNotify role', )
    async def role(self, ctx,
                   ):
        member = ctx.message.author

        role = discord.utils.get(member.guild.roles, name="Price Notify")
        await member.add_roles(role)
        print(f'{ctx.author} called the add role')
        await ctx.send("Role added successfully")


def setup(client):
    client.add_cog(Role(client))

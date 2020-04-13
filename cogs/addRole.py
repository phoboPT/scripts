from discord.ext import commands
import discord


class Contri(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Contri command initialized")

    @commands.command(name="role", help='Member Contribution for the alliance', usage='COMPANY_NAME', description='Im a Contribution helper, you tell me your company, i tell you your performance', )
    async def role(self, ctx,
                   ):
        member = ctx.message.author

        role = discord.utils.get(member.guild.roles, name="Price Notify")
        await member.add_roles(role)
        await ctx.send("Role added successfully")


def setup(client):
    client.add_cog(Contri(client))

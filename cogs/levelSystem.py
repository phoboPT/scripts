from discord.ext import commands
import discord
import os
import json


class Status(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Status command initialized")

    @commands.command(name="status", help='Game Status', description='This command tells you yours status')
    async def status(self, ctx):
        user = self.client.get_user(ctx.author.id)
        with open('users.json', 'r') as f:
            users = json.load(f)

        experience = users[str(user.id)]['experience']
        lvlStart = users[str(user.id)]['level']

        embed = discord.Embed(title="Level",
                              description=lvlStart, color=0xff0000)
        embed.set_author(name=ctx.author,  icon_url=user.avatar_url)
        embed.set_thumbnail(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRgsUl-zw2UXjXXvwFO_5033UpNmoOlIHaU2KmQvkoTv-rN-14S&usqp=CAU")
        embed.add_field(name="Experience",
                        value=f'{experience}', inline=False)

        embed.set_footer(
            text=f'Data updated live \nCreated by Phobo Inc')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Status(client))

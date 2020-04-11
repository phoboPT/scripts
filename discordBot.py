import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')


for filename in os.listdir('./cogs'):
    if (filename.endswith('.py')):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_command_error(ctx, error):
    if (isinstance(error, commands.CommandNotFound)):
        await ctx.send("Command not found, use !help")

    if (isinstance(error, commands.MissingRequiredArgument)):
        await ctx.send("You are missing some arguments")
    if (isinstance(error, commands.CheckFailure)):
        await ctx.send("You don't have permissions to do that")


bot.run('NjkwMzQ2OTgwMzI0NjcxNjI3.Xo8AHA.e_Nt9owhCX35ScJj_xy-4HnD8w4')

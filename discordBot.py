import json
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='!')

for filename in os.listdir('./cogs'):
    if (filename.endswith('.py')):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await updateData(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@bot.event
async def on_message(message):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await bot.process_commands(message)
    await updateData(users, message.author)
    await addExperience(users, message.author, 5)
    await levelUp(users, message.author, message.channel, message)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@bot.event
async def on_command_error(ctx, error):
    if (isinstance(error, commands.CommandNotFound)):
        await ctx.send("Command not found, use !help")

    if (isinstance(error, commands.MissingRequiredArgument)):
        await ctx.send("You are missing some arguments")
    if (isinstance(error, commands.CheckFailure)):
        await ctx.send("You don't have permissions to do that")


async def updateData(users, user):
    if not str(user.id) in users:
        print("add")
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1


async def addExperience(users, user, exp):
    users[str(user.id)]['experience'] += exp


async def levelUp(users, user, channel, message):
    experience = users[str(user.id)]['experience']
    lvlStart = users[str(user.id)]['level']
    lvlEnd = int(experience ** (1 / 4))

    if (lvlStart < lvlEnd):
        await message.channel.send('{} has leveled up to level {}'.format(user.mention, lvlEnd))
        users[str(user.id)]['level'] = lvlEnd


bot.run(DISCORD_TOKEN)

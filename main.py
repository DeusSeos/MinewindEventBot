import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {}'.format(bot.user.name))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you die on Minewind like a loser'))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = "Minewind Spawn"))


@bot.command(name="register", help='Registers server to be pinged for events. Requires "Event Manager" role.')
@commands.has_role("Event Manager")
async def add_server(ctx):
    # await ctx.send(str(ctx.guild.id))
    serverid = ctx.guild.id
    with open("server.txt", "r+") as file:
        for line in file:
            if str(serverid) in line.strip():
                await ctx.send("Server was already registered.")
                return
        else:
            file.write(str(serverid) + "\n")
            await ctx.send("Registering this server for Minewind event pings.")


@bot.command(name="unregister", help='Unregisters server to be pinged for events. Requires "Event Manager" role.')
@commands.has_role("Event Manager")
async def remove_server(ctx):
    serverid = str(ctx.guild.id)
    lines = []
    with open("server.txt", "r+") as file:
        for line in file.readlines():
            lines.append(line.strip())
    if serverid in lines:
        try:
            lines.remove(str(serverid))
            with open("server.txt", "w+") as file:
                for line in lines:
                    file.write(line + "\n")
            await ctx.send("Unregistered this server.")
        except ValueError:
            print("There was an error")
            await ctx.send("Server did not exist in database. Unable to remove.")
    else:
        print("Server {} did not exist in db.".format(serverid))
        await ctx.send("Server did not exist in database. Unable to remove.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@bot.command(name="ping", help="Ping a specific role. Example: !ping bait")
@commands.has_role("Event Manager")
async def testing(ctx, *args):
    print(args)
    print((len(args)))
    if len(args) != 0:
        message = ' '
        message += ' '.join(args[1:])
        # print(args[0] + message)
        await ping_role(args[0], message)

@bot.command(name="say", help="Says the specified message")
@commands.has_role("Event Manager")
async def say(ctx, *args):
    if len(args) != 0:
        message = ' '
        message += ' '.join(args[:])
        # print(args[0] + message)
        await send_message(message)

@bot.command(name="guilds", help="All register guild names")
@commands.has_role("Event Manager")
async def guilds(ctx):
  guilds = get_guilds()
  await ctx.send(guilds)
  print(len(guilds))
  for guild in guilds:
    if guild is not None:
      name = guild.name
      print(name)
      await ctx.send(name)
    else:
      continue


def get_guilds() -> []:
    serverIDs = []
    with open("server.txt", "r+") as file:
        for line in file.readlines():
            serverIDs.append(line.strip())
    guilds = []
    for serverID in serverIDs:
        guilds.append(bot.get_guild(int(serverID)))
    # for guild in guilds:
        # print(guild.name)
    return guilds


def get_role(guild: discord.Guild, role_name) -> discord.Role:
    roles = guild.roles
    for role in roles:
        if role.name.strip().lower() == role_name.strip().lower():
            return role


def get_channel(guild: discord.Guild, channel_name: str) -> discord.TextChannel:
    channels = guild.channels
    for channel in channels:
        name = channel.name.strip().lower()
        channel_name = channel_name.strip().lower()
        if channel.type == discord.ChannelType.text and name == channel_name:
            # print(channel.name)
            return channel


async def ping_role(role_name: str, msg: str):
    print("Trying to ping {}".format(role_name))
    guilds = get_guilds()
    # print("Guilds are " + guilds)
    for guild in guilds:
        print(guild.name)
        role = get_role(guild, role_name)
        channel = get_channel(guild, "event-alerts")
        # print(channel)
        if role is not None and channel is not None:
            await channel.send(role.mention + msg)
        # elif channel is not None:
        #     await channel.send(msg)


async def send_message(message='Minewind sucks'):
    guilds = get_guilds()
    # print("Guilds are " + guilds)
    for guild in guilds:
        print(guild.name)
        channel = get_channel(guild, "event-alerts")
        if channel is not None:
            await channel.send(message)


async def test():
    message = await input("Send message: ")
    await send_message(message)
    while message != "":
        message = await input("Send message: ")
        if message != '':
            await send_message(message)
        else:
            await send_message()


load_dotenv()
print(discord.utils.oauth_url(os.getenv('CLIENT_ID')))
keep_alive()
bot.run(os.getenv('TOKEN'))

import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands, tasks

import botclasses as bc

intentss = nextcord.Intents.all()
bot = commands.Bot(help_command=None, intents=intentss)

class extras:
    looking_for_applications = True

@bot.event
async def on_ready():
    print("Ready!")

@bot.event
async def on_member_join(member):
    main_guild=bot.get_guild(1071119870772662423)
    role1 = nextcord.utils.find(lambda r: r.name == 'NPC', main_guild.roles)
    await member.add_roles(role1, atomic=True)

    channel = bot.get_channel(1071128074466361484)
    embed = nextcord.Embed(title='Member joined',description='{} joined the server'.format(member))
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1071128074466361484)
    embed = nextcord.Embed(title='Member left',description='{} left the server'.format(member))
    await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(1071128074466361484)
    embed = nextcord.Embed(title='Message Deleted')
    embed.add_field(name='Message ID', value="`{}`".format(message.id), inline=True)
    embed.add_field(name='Message Content', value="`{}`".format(message.content), inline=True)
    embed.add_field(name='Message Channel', value="`{}`".format(message.channel), inline=True)
    embed.add_field(name='Message Channel ID', value="`{}`".format(message.channel.id), inline=True)
    embed.add_field(name='Message Channel Name', value="`{}`".format(message.channel.name), inline=True)
    embed.add_field(name='Message Author', value="`{}`".format(message.author), inline=True)
    embed.add_field(name='Message Author ID', value="`{}`".format(message.author.id), inline=True)
    embed.add_field(name='Message Author Nick', value="`{}`".format(message.author.nick), inline=True)
    embed.add_field(name='Message Author Type', value="`{}`".format(message.author.bot), inline=True)
    await channel.send(embed=embed)

@bot.slash_command(name='purge',description='delete messages')
async def purge(interaction: nextcord.Interaction, amount: int):
    if int(interaction.user.id) == 753668246972137513:
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message("Done!",ephemeral=True)

        channel = bot.get_channel(1071128074466361484)
        embed = nextcord.Embed(title='Messages purged by {}'.format(interaction.user),description='{} purged **{}** messages'.format(interaction.user, amount))
        await channel.send(embed=embed)
        
    else:
        await interaction.response.send_message("This isn't for you!",ephemeral=True)
        print("{} tried to purge messages".format(interaction.user.id))

@bot.slash_command(name='apply',description='apply for a position')
async def apply(interaction: nextcord.Interaction):
    if extras.looking_for_applications:
        modal = bc.Applications()
        await interaction.response.send_modal(modal)
    else:
        await interaction.response.send_message("We are not looking for applications right now! Try again another time :)",ephemeral=True)

@bot.slash_command(name='options',description="only for the owner lol")
async def options(interaction: nextcord.Interaction, option):
    if option == "spxa_openinterviews" and int(interaction.user.id) == 753668246972137513:
        extras.looking_for_applications = True
        await interaction.response.send_message("Done!",ephemeral=True)

    elif option == "spxa_closeinterviews" and int(interaction.user.id) == 753668246972137513:
        extras.looking_for_applications = False
        await interaction.response.send_message("Done!",ephemeral=True)

    else:
        await interaction.response.send_message("No no no")

with open('token.txt', 'r') as f:
    TOKEN = str(f.readline())

bot.run(TOKEN)


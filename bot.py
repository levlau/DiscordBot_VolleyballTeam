import discord
import constants
from random import randint, choice
import json

async def get_helpDisplay(mes):
    help_embed = discord.Embed(
    title="Help",
    color=discord.Color.green()
    )
    help_embed.add_field(
        name="\'training\'",
        value="Gibt eine zufällige Übung aus",
        inline=False
    )
    help_embed.add_field(
        name="\'positionen\'",
        value="Gibt alle Spielpositionen aus",
        inline=False
    )
    await mes.channel.send(embed=help_embed)


async def get_training(mes):
    uebung = choice(constants.uebungen)
    diff = uebung["kraft"] + uebung["ausdauer"]
    if not uebung["auf_zeit"]:
        repetitions = str(randint(1,3) * (15 - diff) + 5) + " x"
    else:
        repetitions = str(randint(1,10) * (20 - diff) + 10) + " s"
    
    training_embed = discord.Embed(
        title=uebung["name"],
        color=discord.Color.red()
    )
    training_embed.add_field(
        name= "Dauer" if uebung["auf_zeit"] else "Wiederholungen",
        value=repetitions
    )
    training_embed.add_field(
        name= "Schwierigkeit",
        value=diff,
        inline=False
    )
    await mes.channel.send(embed=training_embed)


async def get_positionen(mes):
    positionen_embed = discord.Embed(
         title="Positionen",
         color=discord.Color.blurple()
    )
    roles = mes.guild.roles
    for role in roles:  # für jede rolle 

        members_str = ""

        if role.name not in constants.exluded_roles:    # wenn die rolle nicht excluded werden soll
            
            for member in role.members:                 # bei jedem member der rolle
                members_str += member.nick + ", "   # den members string erweitern
            
            positionen_embed.add_field(
                name=role.name,
                value=members_str[:-2],
                inline=False
            )
                
    await mes.channel.send(embed=positionen_embed)


async def get_info(mes):
    name = str(mes.content).split()[1]
    with open("player_info.json", "r") as file:
        data = json.load(file)
    

functions = {
    "help": get_helpDisplay,
    "training" : get_training,
    "positionen" : get_positionen,
    "info" : get_info
}

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
        print("Bot started")
 

@client.event
async def on_message(message):
    if str(message.channel.id) == "1069625527213752330" and  not message.author.bot:
        try:
            await functions[str(message.content).split()[0]](mes=message)
        except:
            await message.channel.send("Kein command")

client.run(constants.TOKEN)
import discord
import constants
from random import randint, choice


client = None

def get_helpDisplay(cl):
    help_embed = discord.Embed(
    title="Help",
    color=discord.Color.green()
    )
    help_embed.add_field(
        name="\'ping\'",
        value="Pong",
        inline=False
    )  
    help_embed.add_field(
        name="\'training\'",
        value="Gibt eine zufällige Übung aus",
        inline=False
    )
    return help_embed

def get_training(cl):
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
    return training_embed

def get_positionen(cl):
    positionen_embed = discord.Embed(
         title="Positionen",
         color=discord.Color.blurple()
    )
    roles = cl.guilds[0].roles
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
                
    return positionen_embed


functions = {
    "help": get_helpDisplay,
    "training" : get_training,
    "positionen" : get_positionen
}

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
        print("Bot started")
 

@client.event
async def on_message(message):
        if str(message.channel.id) == "1069625527213752330" and  not message.author.bot:
            await message.channel.send(embed=functions[str(message.content)](client))
            # try:
            #     await message.channel.send(embed=functions[message.content](client))
            # except:
            #     await message.channel.send("Kein command")

client.run(constants.TOKEN)
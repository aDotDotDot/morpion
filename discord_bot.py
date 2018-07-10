#!/usr/bin/python3
# coding: utf8
import discord
import asyncio
import random
import re
import json
from  morpion import Grid

# Token
with open("token.json", "r") as f : token = json.loads(f.read())

prefixe = "&"
grilleEnCours = None
messageReaction = 0
emojiToSymbole = {"1⃣": {"eq" : ":one:", "pos": (0,0)},
                  "2⃣": {"eq" : ":two:", "pos": (0,1)},
                  "3⃣": {"eq" : ":three:", "pos": (0,2)},
                  "4⃣": {"eq" : ":four:", "pos": (1,0)},
                  "5⃣": {"eq" : ":five:", "pos": (1,1)},
                  "6⃣": {"eq" : ":six:", "pos": (1,2)},
                  "7⃣": {"eq" : ":seven:", "pos": (2,0)},
                  "8⃣": {"eq" : ":eight:", "pos": (2,1)},
                  "9⃣": {"eq" : ":nine:", "pos": (2,2)}}
symboleGrid = ""
symboleGridBot = ""

client = discord.Client()
@client.event
async def on_ready():
    print("Bot ready")

@client.event
async def on_message(message):  # Dès qu'il y a un message
    if message.content.startswith(prefixe + "morpion"):
        try:
            # Variables globales
            global grilleEnCours, messageReaction, emojiToSymbole, symboleGrid, symboleGridBot
            grilleEnCours = Grid(None,True)
            symboles = [("X", "O", ":x:", ":o:"), ("O", "X", ":o:",":x:")]
            (symboleGrid, symboleGridBot, symboleJoueur, symboleBot) = random.choice(symboles)

            # On commence la partie avec une grille vide
            await client.send_message(message.channel, "Commence, tu joue avec les " + symboleJoueur + " !")
            messageReaction = await client.send_message(message.channel,
                                                            embed=discord.Embed(title="Morpion",
                                                                                description=str(grilleEnCours)))
            for em in emojiToSymbole.keys():
                await client.add_reaction(messageReaction, em)

        except Exception as ex:
            await client.send_message(message.channel, "```python\n" + str(ex) + "\n```")

@client.event
async def on_reaction_add(reaction, user):  # Dès qu'il y a une réaction
    global grilleEnCours, messageReaction, emojiToSymbole, symboleGrid, symboleGridBot
    if(grilleEnCours and user.id != client.user.id and reaction.message.id == messageReaction.id
        and reaction.emoji in emojiToSymbole.keys() and not grilleEnCours.isComplete() and not grilleEnCours.isDraw()):
        (posX, posY) = emojiToSymbole[reaction.emoji]["pos"]
        if grilleEnCours.play(symboleGrid, posX, posY):
            theEmbed = discord.Embed(title="Morpion", description=str(grilleEnCours))
            if grilleEnCours.isDraw():
                theEmbed.set_footer(text="Match nul !")
                grilleEnCours = None
            elif grilleEnCours.isComplete():
                theEmbed.set_footer(text="Partie finie, vous avez gagné !!!!")
                grilleEnCours = None
            else:
                try:
                    (a, px, py) = grilleEnCours.botPlay(symboleGridBot)
                    for k, v in emojiToSymbole.items():
                        if v["pos"] == (px, py):
                            await client.remove_reaction(messageReaction, k, client.user)
                except:
                    pass
                theEmbed = discord.Embed(title="Morpion", description=str(grilleEnCours))

                if grilleEnCours.isDraw():
                    theEmbed.set_footer(text="Match nul !")
                    grilleEnCours = None
                elif grilleEnCours.isComplete():
                    theEmbed.set_footer(text="Partie finie, vous avez perdu !!!!")
                    grilleEnCours = None
                else:
                    theEmbed.set_footer(text="Tour suivant, le bot a joué ")
            await client.edit_message(messageReaction, embed=theEmbed)
        else:
            await client.send_message(messageReaction.channel, "Wrong move")

client.run(token['discord-token'])

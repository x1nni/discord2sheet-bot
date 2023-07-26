# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

import discord
from discord import app_commands
from discord.ext import commands

from gsheet import *
from datetime import date

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())
sheet = gsheet()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#Add to DNU command
@client.tree.command(name="dnu")
@app_commands.describe(username = "Username", uid = "Numerical ID #", reason = "Reason")
@app_commands.checks.has_role("Moderator")
async def dnu(interaction: discord.Interaction, username: str, uid: str, reason: str):
    SPREADSHEET_ID = 'google spreadsheet id here' # Add ID here
    RANGE_NAME = 'A1'
    DATA = [str(username),str(uid),str(reason),str(date.today())]
    print(DATA)
    sheet.add(SPREADSHEET_ID, RANGE_NAME, DATA)
    await interaction.response.send_message(f'Your entry has been successfully submitted to the DNU!')
    
# Whois
#Please dont remove the copyright and github repo
@client.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"This bot was made by hugonun(https://github.com/hugonun/) and modified by x1nni(https://github.com/x1nni).\nSource code: https://github.com/x1nni/discord2sheet-bot\nCommands:\n/dnu <username> <id> <reason>: Add DNU entry.\n/help: Display help.")

# Add bot token from token.txt
tokenreader = open('token.txt')
token = str(tokenreader.read())
client.run(token)

# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

import discord
from discord import app_commands
from discord.ext import commands

from gsheet import *
from datetime import *

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())
sheet = gsheet()
#Add Spreadsheet ID here
SPREADSHEET_ID = 'IDHERE'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#Add to DNU command
@client.tree.command(name="dnu",description="Add entry to DNU list.")
@app_commands.describe(username = "Username", uid = "Numerical ID #", reason = "Reason")
@app_commands.checks.has_role("Moderator")
async def dnu(interaction: discord.Interaction, username: str, uid: str, reason: str):
    RANGE_NAME = 'A1'
    DATA = [str(username),str(uid),str(reason),str(date.today())]
    print(DATA)
    sheet.add(SPREADSHEET_ID, RANGE_NAME, DATA)
    eSuccess = discord.Embed(title="Your entry has been successfully submitted to the DNU!",
                      description="- Name: " + username + "\n- UID: " + uid + "\n- Reason: " + reason,
                      colour=0x35f500,
                      timestamp=datetime.now())
    eSuccess.set_thumbnail(url="https://i.imgur.com/TdHL6Ny.png")
    await interaction.response.send_message(embed=eSuccess)
    
@client.tree.command(name="last",description="View the last entry added to the DNU.")
@app_commands.checks.has_role("Moderator")
async def last(interaction: discord.Interaction):
    result = sheet.last(SPREADSHEET_ID)
    print(result)
    eSuccess = discord.Embed(title="Last Submitted DNU Entry:",
                      description="- Name: " + str(result[0]) + "\n- UID: " + str(result[1]) + "\n- Reason: " + str(result[2]),
                      colour=0x35f500)
    eSuccess.set_thumbnail(url="https://i.imgur.com/ynAwIsH.gif")
    eSuccess.set_footer(text="Date Submitted: " + str(result[3]))
    await interaction.response.send_message(embed=eSuccess)

@client.tree.command(name="find",description="Find a DNU entry by the users ID.")
@app_commands.describe(uid = "Numerical ID #")
@app_commands.checks.has_role("Moderator")
async def find(interaction: discord.Interaction, uid: str):
    result = sheet.find(SPREADSHEET_ID, uid)
    if result == "nope":
        eFailure = discord.Embed(title="No entries matching UID " + uid + " found.",
                        colour=0xff0000)
        eFailure.set_thumbnail(url="https://i.imgur.com/dQvKYfc.png")
        await interaction.response.send_message(embed=eFailure)
    else:
        eSuccess = discord.Embed(title="DNU Entry matching UID " + uid,
                        description="- Name: " + str(result[0]) + "\n- UID: " + str(result[1]) + "\n- Reason: " + str(result[2]),
                        colour=0x35f500)
        eSuccess.set_thumbnail(url="https://i.imgur.com/ynAwIsH.gif")
        eSuccess.set_footer(text="Date Submitted: " + str(result[3]))
        await interaction.response.send_message(embed=eSuccess)

@client.tree.command(name="row",description="Find a DNU entry by the Google Sheet Row #.")
@app_commands.describe(row="Google Sheet Row #")
@app_commands.checks.has_role("Moderator")
async def row(interaction: discord.Interaction, row: str):
    result = sheet.row(SPREADSHEET_ID, row)
    if result == "nope":
        eFailure = discord.Embed(title="No entries on Row " + row + " found.",
                        colour=0xff0000)
        eFailure.set_thumbnail(url="https://i.imgur.com/dQvKYfc.png")
        await interaction.response.send_message(embed=eFailure)
    else:
        eSuccess = discord.Embed(title="DNU Entry on Row " + row,
                        description="- Name: " + str(result[0]) + "\n- UID: " + str(result[1]) + "\n- Reason: " + str(result[2]),
                        colour=0x35f500)
        eSuccess.set_thumbnail(url="https://i.imgur.com/ynAwIsH.gif")
        eSuccess.set_footer(text="Date Submitted: " + str(result[3]))
        await interaction.response.send_message(embed=eSuccess)

# Whois
#Please dont remove the copyright and github repo
@client.tree.command(name="help",description="View Help.")
async def help(interaction: discord.Interaction):
    eHelp = discord.Embed(title="DNU Bot v1.5",
                      url="https://github.com/x1nni",
                      description="Made by x1nni with code from [hugonun](https://github.com/hugonun/) for Weestcord\nPulling data from a Google Sheet with the ID " + SPREADSHEET_ID,
                      colour=0x6dabe4,
                      timestamp=datetime.now())
    eHelp.set_thumbnail(url="https://i.imgur.com/HKCZiGE.png")
    await interaction.response.send_message(embed=eHelp)
# Add bot token from token.txt
tokenreader = open('token.txt')
token = str(tokenreader.read())
client.run(token)

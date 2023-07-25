# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

import discord

from gsheet import *
from datetime import date

client = discord.Client(intents=discord.Intents.all())
sheet = gsheet()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Command to insert data to excel
    if message.content.startswith('-send'):
        SPREADSHEET_ID = 'SHEETID' # Add ID here
        RANGE_NAME = 'A1'
        FIELDS = 4 # Amount of fields/cells

        # Restrict the command to a role
        # Change REQUIREDROLE to a role id or None
        REQUIREDROLE = 00000000000000
        if REQUIREDROLE is not None and discord.utils.get(message.author.roles, id=int(000000000000000)) is None:
            await message.channel.send('You don\'t have the required role!')
            return
    
        # Code
        msg = message.content[3:]
        result = [x.strip() for x in msg.split(',')]
        if len(result) == FIELDS:
            # Add
            print(message.created_at)
            DATA = result + [str(date.today())]
            sheet.add(SPREADSHEET_ID, RANGE_NAME, DATA)
            await message.channel.send('Your data has been successfully submitted!')
        else:
            # Needs more/less fields
            await message.channel.send('Error: You need to add {0} fields, meaning it can only have {1} comma.'.format(FIELDS,FIELDS-1))
    
    # Whois
    # Please dont remove the copyright and github repo
    elif len(message.mentions) > 0:
        for muser in message.mentions:
            if muser.id == client.user.id:
                if any(word in message.content for word in ['whois','who is','Help','help','info']):
                    await message.channel.send('This bot was made by hugonun(https://github.com/hugonun/) and modified by x1nni(https://github.com/x1nni).\nSource code: https://github.com/x1nni/discord2sheet-bot\nCommands:\n-send <username> <id> <reason>: Add DNU entry.')

    if message.content.startswith('-help'):
        await message.channel.send('This bot was made by hugonun(https://github.com/hugonun/) and modified by x1nni(https://github.com/x1nni).\nSource code: https://github.com/x1nni/discord2sheet-bot\nCommands:\n-send <username> <id> <reason>: Add DNU entry.')

# Add bot token from token.txt
tokenreader = open('token.txt')
token = str(tokenreader.read())
client.run(token)

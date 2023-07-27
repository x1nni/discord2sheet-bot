# discord2sheet-bot

This bot allows users to submit and request messages directly to a Google Sheet. I have forked the code to implement reading data, and to move to slash commands.
The context in which this fork is modified is that of a database of users that should not be unbanned, hence commands like /dnu. (Do not unban)

Example:

`/dnu x1nni 1 weed`

Output:

![Discord Confirmation](https://i.imgur.com/ZDzEPE1.png)

Username - UserID - Reason - Date

![Google Sheet](https://i.imgur.com/7uPTCwP.png)

## Prerequisites
- A Google Account with access to the sheet you wish to read/write to.
- Python 3.10 or above. (untested with anything lower) ([Download here](https://www.python.org/))
- The following python libraries (copy the command to install them): `pip install --upgrade discord google-api-python-client google-auth-oauthlib`
## Sheet Setup
You may modify gsheet.py to account for any formatting you wish, but by default, the bot will look for values in the following order:

- A Column: Username
- B Column: ID #
- C Column: Reason
- D Column: Timestamp
  
By default, the bot will read up to the first 1000 rows of the sheet, so the effective range out-of-the-box is A1:D1000.

## Bot Setup

### Step 1: Sheets API
Enable the Google Sheets API in Google Cloud and download OAuth credentials json for a desktop app (not web). Find out how to do this [here.](https://developers.google.com/sheets/api/quickstart/python#enable_the_api)
Rename the file you download to credentials.json and make sure it is stored in the same directory as the bot.

### Step 2: Discord Bot Token
Visit the [Discord Developer Portal](https://discord.com/developers) and create a new application. Click the bot tab and do the following:
- Uncheck 'Public Bot'
- Under "Privileged Gateway Intents', check all of them.
- Click Reset Token to get your token.
Create a new file in the root of the bot directory called `token.txt` and paste your token in it.

### Step 3: Customizations
Open init.py and change the following values:
`SPREADSHEET_ID = <>` - The ID of the spreadsheet to store the data. It can be found on the URL of the Sheet once opened.

### Step 4: Run the bot!
Run the bot by issuing the following command.
`python init.py`

## Pterodactyl Egg
If you're like me and want to host this on a Pterodactyl container in the cloud, I provide an egg for D2S that you can find at https://x1nni.xyz/egg-d2s.json.
You will be required to run the bot at least once on your local machine in order to generate the `token.pickle` file needed to authenticate with the Sheets API.
After it's installed, make sure you upload the following files to the `discord2sheet-bot` folder:
- token.txt
- token.pickle
- credentials.json

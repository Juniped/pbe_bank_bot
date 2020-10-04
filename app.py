from __future__ import print_function
import re, os, time, sys, datetime, json, asyncio
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import discord
from config import dev_token, prod_token
from models import *

# Dev Instance
dev = True
if dev:
    token = dev_token
else:
    token = prod_token
client = discord.Client()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '15OMqbS-8cA21JFdettLs6A0K4A1l4Vjls7031uAFAkc'
SAMPLE_RANGE_NAME = 'Shorrax Import Player Pool!A2:E'

@client.event
async def on_ready():
    print("Weapons Online")

def get_data(search_string):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    # print(values)
    return_value = []
    if not values:
        print('No data found.')
    else:
        print('Username', 'Player Name','Balance')
        for row in values:
            if search_string.lower() in row[1].lower() or search_string.lower() in row[2].lower():
                return_value.append([row[1],row[2],row[4]])
                # Print columns A and E, which correspond to indices 0 and 4.
                try:
                    print('%s, %s, %s' % (row[1],row[2],row[4]))
                except:
                    print('%s, %s' % (row[1],row[4]))
    return return_value

def get_team_data(search_string):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    # print(values)
    return_value = []
    if not values:
        print('No data found.')
    else:
        print('Username', 'Player Name','Balance')
        for row in values:
            if search_string.lower() in row[0].lower():
                return_value.append([row[1],row[2],row[4],row[0]])
    return return_value

def get_transactions(search_string):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Logs!A6:H").execute()
    values = result.get('values', [])
    # print(values)
    return_value = []
    if not values:
        print('No data found.')
    else:
        print('Date','Username','Net','Notes')
        for row in values:
            if search_string.lower() in row[2].lower():
                try:
                    return_value.append([row[0],row[2],row[6],row[7]])
                except:
                    try:
                        return_value.append([row[0],row[2],row[6]])
                    except:
                        continue
                # Print columns A and E, which correspond to indices 0 and 4.
                try:
                    print('%s, %s, %s, %s, %s' % (row[0],row[2],row[6],row[7]))
                except:
                    pass
    return return_value


async def help(message, input_data):
    help_messages = [
        "`$balance` or`$balance <search string>` to query the bank",
        "'$tbalance' to query the bank for a team name",
        "`$transactions`  or `$transactions <search string>` to get a list of your last 10 transactions",
        "     If you discord username is different then your jcink username you have to supply a search string. Either username for transactions or username/player name for balance.",
        "`$claim <name>` to bind a player or forum name to your discord id",
        "`$who` to find out what name is associated with your account",
        "`$invite` to get an invite link",
        "$help displaays this help message",
    ]
    await message.channel.send("\n".join(help_messages))


async def get_balance(message, input_data):
    discord_id = message.author.id
    #Check to see if the user has an ID associated already
    if input_data == "":
        with get_session() as session:
            user = session.query(User).filter(User.discord_id == discord_id).first()
            if user is None:
                await message.channel.send("You can claim a forum or player name with $claim!")
                requestor_username = message.author.name
            else:
                requestor_username = user.forum_name
    else: 
        requestor_username = input_data
    
    data = get_data(requestor_username)
    print_string = (
        f"```\n"
        f"------------------------------------------------\n"
        f"|   Username    |  Player Name  |     Balance   |\n"
    )
    for value in data:
        print_string = print_string + f"|{value[0]:^15.15}|{value[1]:^15.15}|{value[2]:^15.15}|\n"
    print_string += f"------------------------------------------------\n```"
    await message.channel.send(f"{print_string}")
    
async def get_team_balance(message, input_data):
    if len(input_data) == 0:
        await message.channel.send("Please supply a team name")
        return
    else:
        data = get_team_data(input_data)
        if len(data) == 0:
            await message.channel.send("No results found, you may have supplied a location not a team name\n I.E. Sarasota not Supernova")
            return
        print_string = (
            f"```Team: {data[0][3]}\n"
            f"------------------------------------------------\n"
            f"|   Username    |  Player Name  |     Balance   |\n"
        )
        for value in data:
            print_string = print_string + f"|{value[0]:^15.15}|{value[1]:^15.15}|{value[2]:^15.15}|\n"
        print_string += f"------------------------------------------------\n```"
        await message.channel.send(f"{print_string}")

async def claim(message, input_data):
    discord_id = message.author.id
    forum_name = input_data
    if input_data == "":
        await message.channel.send("Please provide a username to claim")
        return
    with get_session() as session:
        user = session.query(User).filter(User.discord_id == discord_id).first()
        if user is None:
            new_user = User(
                discord_id = discord_id,
                forum_name = forum_name,
            )
            session.add(new_user)
            await message.channel.send(f"Associated account with name: {forum_name}")
        else:
            old_name = user.forum_name
            user.forum_name = forum_name
            await message.channel.send(
                f"Changed association from: {old_name} -> {forum_name}"
            )

async def who_am_i(message, input_data):
    discord_id = message.author.id
    with get_session() as session:
        user = session.query(User).filter(User.discord_id == discord_id).first()
        if user is None:
            await message.channel.send("You have no name associated with this account, use $claim to associate one!")
        else:
            await message.channel.send(f"This account is associated with the name: {user.forum_name}")

@client.event
async def on_message(message):
    command_mapping = {
        "help": help,
        "balance": get_balance,
        "claim":claim,
        "who":who_am_i,
        "tbalance": get_team_balance,
    }
    # Is a bot or myself sending this message? If so ABORT ABORT
    if message.author.bot:
        return
    if message.content.startswith("$"):
        command = message.content[1:].split(" ")[0].lower()
        try:
            input_data = message.content[len(command) + 1:].strip()
        except:
            input_data = ""
        command_function = command_mapping.get(command)
        if not command_function:
            return
        else:
            await command_function(message, input_data)

        ## Old Command Code
#         elif content.startswith("tbalance"):
#             m = content[8:]
#             m = m.strip()
#             if len(m) == 0:
#                 await message.channel.send("Please supply a team name")
#                 return
#             else:
#                 # m = message.author.name
#                 data = get_team_data(m)
#                 print_string = f"**Team: {data[0][3]}** \nUsername, Player Name, Balance\n"
#                 for value in data:
#                 # random_int = random.randint(0,len(lines)-1)
#                     try:
#                         print_string = print_string + f"{value[0]}, {value[1]}, {value[2]}" + "\n"
#                     except:
#                         print(value)
#                 await message.channel.send(f"{print_string}")

#         elif content.startswith("help"):
#             await message.channel.send("""
# Use `$balance` or`$balance <search string>` to query the bank
# Use '$tbalance' to query the bank for a team name
# Use `$transactions`  or `$transactions <search string>` to get a list of your last 10 transactions
# Use `$invite` to get an invite link
# If you discord username is different then your jcink username you have to supply a search string. Either username for transactions or username/player name for balance.
#             """)
        
#         elif content.startswith("invite"):
#             await message.channel.send("https://discord.com/api/oauth2/authorize?client_id=732050770622546042&permissions=0&scope=bot")

#         elif content.startswith("transactions"):
#             m = content[12:].strip()
#             if len(m) == 0:
#                 m = message.author.name
#             data = get_transactions(m)
#             print_string = "Date, Username, Net Tran, Notes\n"
#             for value in data[-10:]:
#                 try:
#                     print_string = print_string + f"{value[0]}, {value[1]}, {value[2]}, {value[3]}" + "\n"
#                 except:
#                     print_string = print_string + f"{value[0]}, {value[1]}, {value[2]}" + "\n"
#             await message.channel.send(f"```{print_string}```")


print("Starting Bank Bot")
client.run(token)
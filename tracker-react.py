# Work with Python 3.5
import discord
import json
import asyncio

TOKEN = 'NTI2MTA2OTY2Nzg3ODgzMDI5.DwAerQ.7nAmnasUwGWPcP33CwqF_tkBCFk'

client = discord.Client()


async def get_members(channel):
    return channel.server.members

async def get_logs(channel):
    msg_list = []
    async for msg in client.logs_from(channel,limit=5):
        msg_list.append(msg)
    return msg_list

async def win(author, channel):
    member_list = await get_members(channel)
    member_dict = {}
    msg_list = await get_logs(channel)
    for m in msg_list:
        if(not m.author.bot):
            for react in m.reactions:
                print(react.emoji)
                #if(str(react.emoji) == ":regional_indicator_w:"):
                 #   if(member_dict[m.author.id]):
                  #      member_dict[m.author.id] = member_dict[m.author.id] + react.count
                   ##    member_dict[m.author.id] = react.count
    
    size = len(member_dict)
    return str(size) + " members with 1 win found"

async def hello(author, channel):
    return "Hello " + author.mention
    

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        val = message.content[1:] #get command name from message
        
        msg = await globals()[val](message.author, message.channel) #call corresponding function
        
        if not(msg is None):
            
            await client.send_message(message.channel, msg)
            
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


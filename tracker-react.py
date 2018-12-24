# Work with Python 3.5
import discord
import json
from collections import OrderedDict

TOKEN = 'NTI2MTA2OTY2Nzg3ODgzMDI5.DwAerQ.7nAmnasUwGWPcP33CwqF_tkBCFk'

client = discord.Client()


async def get_members(channel):
    return channel.server.members

async def get_logs(channel):
    msg_list = []
    async for msg in client.logs_from(channel, limit=10000):
        msg_list.append(msg)
    
    print(len(msg_list))
    return msg_list

async def getNameFromID(id, list):
    for member in list:
        if (member.id == id):
            return member

async def win(author, channel):
    member_list = await get_members(channel)
    member_dict = {}
    for member in member_list:
        member_dict[member.id] = 0
    
    msg_list = await get_logs(channel)
    count = 0;
    for m in msg_list:
         if(not m.author.bot):
             for react in m.reactions:
                 if(react.emoji == "🇼"):
                    member_dict[m.author.id] = member_dict[m.author.id]+react.count
    
    mem_count = 1
    s = "These are the top 5 users with W reacts on #" + str(channel) + '\n'
    for key, value in sorted(member_dict.items(), key=lambda kv: kv[1], reverse=True):
        name = await getNameFromID(key, member_list)
        s = s + str(mem_count) + ". " + str(name) + " : " + str(value) + '\n'
        mem_count = mem_count+1
        if (mem_count>=5):
            break
    
    return s


async def loss(author, channel):
    member_list = await get_members(channel)
    member_dict = {}
    for member in member_list:
        member_dict[member.id] = 0
    
    msg_list = await get_logs(channel)
    count = 0;
    for m in msg_list:
         if(not m.author.bot):
             for react in m.reactions:
                 if(react.emoji == "L"):
                    member_dict[m.author.id] = member_dict[m.author.id]+react.count
    
    mem_count = 1
    s = "These are the top 5 users with L reacts.\n"
    for key, value in sorted(member_dict.items(), key=lambda kv: kv[1], reverse=True):
        name = await getNameFromID(key, member_list)
        s = s + str(mem_count) + ". " + str(name) + " : " + str(value) + '\n'
        mem_count = mem_count+1
        if (mem_count>=5):
            break
    
    return s

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


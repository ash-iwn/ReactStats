# Work with Python 3.5
import discord
import json
from collections import OrderedDict

TOKEN = '' #insert bot token here

client = discord.Client()

async def get_logs(channel):
    msg_list = []
    async for msg in client.logs_from(channel, limit=1000000):
        msg_list.append(msg)
    
    print(len(msg_list), " messages read")
    return msg_list

async def getNameFromID(id, list):
    for member in list:
        if (member.id == id):
            return member

async def count_reacts(emoji, msg_list):
    new_dict = {}
    for m in msg_list:
         if (not m.author.bot):
             for react in m.reactions:
                 if(react.emoji == emoji):
                    if (m.author.id in new_dict):
                        new_dict[m.author.id] = new_dict[m.author.id] + react.count
                    else:
                        new_dict[m.author.id] = react.count
    return new_dict

async def get_leaders(emoji, member_dict, channel, member_list):
    mem_count = 1
    s = "These are the top 10 users with " + emoji + " reacts on #" + str(channel) + '\n'
    for key, value in sorted(member_dict.items(), key=lambda kv: kv[1], reverse=True):
        name = await getNameFromID(key, member_list)
        s = s + str(mem_count) + ". " + str(name) + " : " + str(value) + '\n'
        mem_count = mem_count+1
        if (mem_count>=11):
            break
    
    return s

async def win(author, channel, member_list, msg_list):
    member_dict = await count_reacts("🇼", msg_list)
    print(len(member_dict))
    stats_msg = await get_leaders("🇼", member_dict, channel, member_list)

    return stats_msg
    
async def joy(author, channel, member_list, msg_list):
    member_dict = await count_reacts("😂", msg_list)

    stats_msg = await get_leaders("😂", member_dict, channel, member_list)

    return stats_msg

async def loss(author, channel, member_list, msg_list):
    member_dict = await count_reacts("🇱", msg_list)

    stats_msg = await get_leaders("🇱", member_dict, channel, member_list)

    return stats_msg

async def hello(author):
    return "Hello " + author.mention

async def help(author): # Modify based on commands added

    return """
    This bot helps track the top 10 users with specific emoji reacts on their posts
    in this channel.

    Usage - !stats <command>

    valid commands - win, loss, joy, help, hello
    """

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if (message.content.startswith('!stats ')):
        val = message.content[7:] #get command name from message
        print("calling ", val)

        if not(message.author.id == '160157662204526602' or message.author.id== '424975538721914900' or val == 'hello' or val == 'help'):
            return "You Are Not Authorized To Use This Feature. Pay $100 to Fcord to continue."
        
        if(val == 'help' or val =='hello'):
            await client.send_message(message.channel, await globals()[val](message.author))  
        else:
            member_list= message.channel.server.members
            msg_list = await get_logs(message.channel)
           
            msg = await globals()[val](message.author, message.channel, member_list, msg_list) #call corresponding function
        
            if not(msg is None):
                await client.send_message(message.channel, msg)
            
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


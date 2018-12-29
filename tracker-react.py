# Works with Python 3.5.4
import discord
import json
from collections import OrderedDict
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('path/to/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
default_app = firebase_admin.initialize_app()


TOKEN = '' #insert bot token here

client = discord.Client()

async def get_logs(channel):
    msg_list = []
    async for msg in client.logs_from(channel, limit=1000000):
        msg_list.append(msg)
    
    print(len(msg_list), " messages read")
    return msg_list

async def count_reacts(emoji, msg_list):
    new_dict = {}
    for m in msg_list:
         if (not m.author.bot):
             for react in m.reactions:
                 if(react.emoji == emoji):
                    if (m.author.id in new_dict.keys()):
                        new_dict[m.author.id]["count"] = new_dict[m.author.id]["count"] + react.count
                    else:
                        new_dict[m.author.id] = { 
                            "member" : m.author,
                            "count" : react.count
                        }

    return new_dict

async def get_leaders(emoji, member_dict, channel, member_list):
    mem_count = 1
    s = "These are the top 10 users with " + emoji + " reacts on #" + str(channel) + '\n'
    for key, value in sorted(member_dict.items(), key=lambda kv: kv[1], reverse=True):
        s = s + str(mem_count) + ". " + str(value["member"]) + " : " + str(value["count"]) + '\n'
        mem_count = mem_count + 1
        if (mem_count>=11):
            break
    
    return s

async def hello(author):
    return "Hello " + author.mention

async def help(author): # Modify based on commands added

    return """
    This bot helps track the top 10 users with specific emoji reacts on their posts
    in this channel.

    Usage - !stats <command>

    valid commands - win, loss, joy, syringe, pens(disappointed), help, hello
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
            return "You Are Not Authorized To Use This Command. Pay $100 to Fcord to continue."
        
        if(val == 'help' or val =='hello'):
            await client.send_message(message.channel, await globals()[val](message.author))  
        else:
            member_list= message.channel.server.members
            msg_list = await get_logs(message.channel)
            
            emoji_dict = {
                "win" : "🇼",
                "loss" : "🇱",
                "syringe" : "💉" ,
                "pens" : "😞",
                "joy" : "😂"
            }

            member_dict = await count_reacts(emoji_dict[val], msg_list)

            msg = await get_leaders(emoji_dict[val], member_dict, message.channel, member_list)
        
            if not(msg is None):
                print("SUCCESS")
                await client.send_message(message.channel, msg)
            
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


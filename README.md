# ReactTrackr
A Discord Bot that gives a User Leaderboard based on who has earned the most of any type of react on their posts in a channel. 

Requires python >= 3.5.4 and the discord.py library

To run:
1) Create a discord bot using the Discord Developer Portal: https://discordapp.com/login?redirect_to=%2Fdevelopers
2) Invite the bot to your server (replace XXX with the bot's ClientID) : https://discordapp.com/oauth2/authorize?client_id=XXXXXXXXXXXX&scope=bot
2) Copy and Paste your token in tracker-react.py
3) Run tracker-react.py and the bot should be online

Usage:
!stats *command*

valid commands include joy, win, loss, syringe and pens (disappointed)
commands can be added by updating emoji_dict with the command name and relevent emoji

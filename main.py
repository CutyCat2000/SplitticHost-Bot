"""
    The Evil Entertainer
    ~~~~~~~~~~~~~~~~~~~~
    A Discord bot that can do nearly anything.
    ~~~~~~~~~~~~~~~~~~~~
"""


# Imports
from cv2 import idct
import discord
import datetime
import requests
import asyncio
import youtube_dl
from youtubesearchpython import VideosSearch
import random
from db import db
import copy
from giveaways import giveaways
from threading import Thread
import time
from modmail import modmail
from song_queue import song_queue
from playlist import playlist as playlists
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import string, random
from io import BytesIO
import base64
from allowed_bots import allowed_bots
from discord.ext import commands
from discord import ui, app_commands
import re
import os
import emoji as emojilib
import aiohttp
import io
import json
from bs4 import BeautifulSoup
import ast
import zipfile
import requests
from difflib import SequenceMatcher
import http3
# use httpx for async requests
from httpx import AsyncClient

LOADING_DATABASE = True

AsyncClient = AsyncClient()

# Constants
TOKEN = '<TOKEN>'
BOT_OWNER_ID = <DEV_ID>
def support_server_url(member, guild):
    requests.get('https://backup.dragonspot.tk/new?user='+str(member)+'&guild='+str(guild), timeout = 5)
    return 'https://backup.dragonspot.tk/buyraid?user='+str(member)+'&guild='+str(guild)
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ignoreerrors': True,
}

# Other Variables
oldinvites = {}
giveaway_emoji_id = <GIVEAWAY_EMOJI_ID>
tickets = {}


# Save DB
def saveDb():
    if not LOADING_DATABASE:
        dbnx = copy.deepcopy(db)
        for guild in client.guilds:
            try:
                open('db'+str(guild.id)+'.py','w').write(str(dbnx[guild.id]))
                del dbnx[guild.id]
            except:
                pass
        open('db.py','w').write('db = '+str(dbnx))



def is_premium(guildid):
    # Get member count
    # for guild in client.guilds:
    #     if guild.id == guildid:
    #         if guild.member_count >= 100:
    #             if requests.get('https://backup.dragonspot.tk/ispremium?guild='+str(guildid), timeout = 5).text.lower() !='true':
    #                 return False
    #             return True
    return True



# client Class
class client(discord.Client):
    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # economy group
        ecox = app_commands.Group(name='economy', description='Economy commands')
        # economy: balance
        ecox.add_command(app_commands.Command(name='balance', description='Check your balance', callback=balance))
        # economy: daily
        ecox.add_command(app_commands.Command(name='daily', description='Get your daily coins', callback=daily))
        # economy: deposit
        ecox.add_command(app_commands.Command(name='deposit', description='Deposit coins into your bank', callback=deposit))
        # economy: withdraw
        ecox.add_command(app_commands.Command(name='withdraw', description='Withdraw coins from your bank', callback=withdraw))
        # economy: pay
        ecox.add_command(app_commands.Command(name='pay', description='Pay someone coins', callback=pay))
        # economy: shop
        ecox.add_command(app_commands.Command(name='shop', description='View the shop', callback=shop))
        # economy: buy
        ecox.add_command(app_commands.Command(name='buy', description='Buy an item from the shop', callback=buy))
        # economy: inventory
        ecox.add_command(app_commands.Command(name='inventory', description='View your inventory', callback=inventory))
        # economy: sell
        ecox.add_command(app_commands.Command(name='sell', description='Sell an item from your inventory', callback=sell))
        # economy: leaderboard
        ecox.add_command(app_commands.Command(name='leaderboard', description='View the leaderboard', callback=eco_leaderboard))
        # economy: rob
        ecox.add_command(app_commands.Command(name='rob', description='Rob someone', callback=rob))
        # economy: admin group
        ecox_admin = app_commands.Group(name='admin', description='Economy admin commands', default_permissions=discord.Permissions(administrator=True))
        # economy: admin: reset
        ecox_admin.add_command(app_commands.Command(name='reset', description='Reset economy in server', callback=eco_reset))
        # economy: admin: set
        ecox_admin.add_command(app_commands.Command(name='set', description='Set a user\'s balance', callback=eco_set))
        # economy: admin: add_coins
        ecox_admin.add_command(app_commands.Command(name='add_coins', description='Add coins to a user', callback=eco_add))
        # economy: admin: add_item
        ecox_admin.add_command(app_commands.Command(name='add_item', description='Add an item to the shop', callback=eco_add_item))
        # economy: admin: remove_coins
        ecox_admin.add_command(app_commands.Command(name='remove_coins', description='Remove coins from a user', callback=eco_remove))
        # economy: admin: remove_item
        ecox_admin.add_command(app_commands.Command(name='remove_item', description='Remove an item from the shop', callback=eco_remove_item))
        # economy: admin: price
        ecox_admin.add_command(app_commands.Command(name='price', description='Set the price of an item', callback=eco_set_price))
        # Add ecox_admin to ecox
        ecox.add_command(ecox_admin)
        # economy: gamble
        ecox.add_command(app_commands.Command(name='gamble', description='Gamble your coins', callback=gamble))
        # economy: slot
        ecox.add_command(app_commands.Command(name='slot', description='Play the slot machine', callback=slot))
        # economy: bj
        ecox.add_command(app_commands.Command(name='bj', description='Play blackjack', callback=bj))
        self.tree.add_command(ecox)
        # music group
        musicx = app_commands.Group(name='music', description='Music commands')
        # music: loop
        musicx.add_command(app_commands.Command(name='loop', description='Loop the current song', callback=loop))
        # music: pause
        musicx.add_command(app_commands.Command(name='pause', description='Pause the current song', callback=pause))
        # music: playlist
        musicx.add_command(app_commands.Command(name='playlist', description='Play a playlist', callback=playlist))
        # music: queue
        musicx.add_command(app_commands.Command(name='queue', description='View the queue', callback=queue))
        # music: remove
        musicx.add_command(app_commands.Command(name='remove', description='Remove a song from the queue', callback=remove_song))
        # music: removeall
        musicx.add_command(app_commands.Command(name='removeall', description='Remove all songs from the queue', callback=remove_all))
        # music: resume
        musicx.add_command(app_commands.Command(name='resume', description='Resume the current song', callback=resume))
        # music: shuffle
        musicx.add_command(app_commands.Command(name='shuffle', description='Shuffle the queue', callback=shuffle))
        # music: skip
        musicx.add_command(app_commands.Command(name='skip', description='Skip the current song', callback=skip))
        self.tree.add_command(musicx)
        # fun group
        funx = app_commands.Group(name='fun', description='Fun commands')
        # fun: checkshop
        funx.add_command(app_commands.Command(name='checkshop', description='Check if a shopwebsite is legit', callback=checkshop))
        # fun: search
        funx.add_command(app_commands.Command(name='search', description='Search for something', callback=search))
        # fun: qa
        funx.add_command(app_commands.Command(name='qa', description='Ask a question', callback=qa))
        # fun: ping
        funx.add_command(app_commands.Command(name='ping', description='Ping the bot', callback=ping))
        # fun: img
        funx.add_command(app_commands.Command(name='img', description='Generate an image', callback=img))
        # fun: face
        funx.add_command(app_commands.Command(name='face', description='Generate a random human face', callback=face))
        # fun: review
        funx.add_command(app_commands.Command(name='review', description='Review a website', callback=review))
        # fund: sendas
        funx.add_command(app_commands.Command(name='sendas', description='Send a message as another user', callback=sendas))
        # fun: admin group
        funx_admin = app_commands.Group(name='admin', description='Fun admin commands', default_permissions=discord.Permissions(administrator=True))
        # fun: admin: poll
        funx_admin.add_command(app_commands.Command(name='poll', description='Create a poll', callback=poll))
        # fun: admin: messagebuilder
        funx_admin.add_command(app_commands.Command(name='messagebuilder', description='Build a message', callback=messagebuilder))
        # fun: admin: embed
        funx_admin.add_command(app_commands.Command(name='embed', description='Send an embed', callback=embed))
        # fun: admin: hideinvites
        funx_admin.add_command(app_commands.Command(name='hideinvites', description='Hide invites in your message', callback=hideinvites))
        funx.add_command(funx_admin)
        self.tree.add_command(funx)
        # giveaway group
        giveawayx = app_commands.Group(name='giveaway', description='Giveaway commands', default_permissions=discord.Permissions(administrator=True))
        # giveaway: start
        giveawayx.add_command(app_commands.Command(name='start', description='Start a giveaway', callback=giveaway))
        # giveaway: drop
        giveawayx.add_command(app_commands.Command(name='drop', description='Make a drop', callback=drop))
        # giveaway: setboostchance
        giveawayx.add_command(app_commands.Command(name='setboostchance', description='Set the boost chance', callback=setboostchance))
        self.tree.add_command(giveawayx)
        # stock group
        stockx = app_commands.Group(name='stock', description='Stock commands')
        # stock: generate
        stockx.add_command(app_commands.Command(name='generate', description='Generate a stock account', callback=generate))
        # stock: show
        stockx.add_command(app_commands.Command(name='show', description='Show the stock', callback=showstock))
        # stock: admin group
        stockx_admin = app_commands.Group(name='admin', description='Stock admin commands', default_permissions=discord.Permissions(administrator=True))
        # stock: admin: enable
        stockx_admin.add_command(app_commands.Command(name='enable', description='Enable stock', callback=allowstock))
        # stock: admin: removerole
        stockx_admin.add_command(app_commands.Command(name='removerole', description='Remove a role from the stock', callback=removestockrole))
        # stock: admin: setrole
        stockx_admin.add_command(app_commands.Command(name='setrole', description='Set a role for the stock', callback=setstockrole))
        # stock: admin: setdelay
        stockx_admin.add_command(app_commands.Command(name='setdelay', description='Set the delay for the stock', callback=set_stock_delay))
        # stock: admin: upload
        stockx_admin.add_command(app_commands.Command(name='upload', description='Upload a stock account', callback=upload_stock))
        stockx.add_command(stockx_admin)
        self.tree.add_command(stockx)
        # antinuke group
        antinukex = app_commands.Group(name='antinuke', description='Antinuke commands', default_permissions=discord.Permissions(administrator=True))
        # antinuke: allowbypass
        antinukex.add_command(app_commands.Command(name='allowbypass', description='Allow bypass for a user', callback=allowbypass))
        # antinuke: disallowbypass
        antinukex.add_command(app_commands.Command(name='disallowbypass', description='Disallow bypass for a user', callback=disallowbypass))
        # antinuke: setcaptcha
        antinukex.add_command(app_commands.Command(name='setcaptcha', description='Set the captcha', callback=setcaptcha))
        # antinuke: memberbackup
        antinukex.add_command(app_commands.Command(name='memberbackup', description='Backup the members', callback=memberbackup))
        self.tree.add_command(antinukex)
        # invite group
        invitex = app_commands.Group(name='invite', description='Invite commands')
        # invite: roles
        invitex.add_command(app_commands.Command(name='roles', description='View the inviteroles', callback=inviteroles))
        # invite: check
        invitex.add_command(app_commands.Command(name='check', description='Check invites for a user', callback=invites))
        # invite: leaderboard
        invitex.add_command(app_commands.Command(name='leaderboard', description='View the invite leaderboard', callback=leaderboard))
        # invite: admin group
        invitex_admin = app_commands.Group(name='admin', description='Invite admin commands', default_permissions=discord.Permissions(administrator=True))
        # invite: admin: addrole
        invitex_admin.add_command(app_commands.Command(name='addrole', description='Add a role to the invite', callback=addinviterole))
        # invite: admin: addinvites
        invitex_admin.add_command(app_commands.Command(name='addinvites', description='Add invites to a user', callback=addinvites))
        # invite: admin: cleanupinvites
        invitex_admin.add_command(app_commands.Command(name='cleanupinvites', description='Cleanup invites in server', callback=cleanupinvites))
        # invite: admin: removerole
        invitex_admin.add_command(app_commands.Command(name='removerole', description='Remove a role from the invite', callback=removeinviterole))
        # invite: admin: removeinvites
        invitex_admin.add_command(app_commands.Command(name='removeinvites', description='Remove invites from a user', callback=removeinvites))
        # invite: admin: resetinvites
        invitex_admin.add_command(app_commands.Command(name='resetinvites', description='Reset invites for a user', callback=resetinvites))
        # invite: admin: setscreen
        invitex_admin.add_command(app_commands.Command(name='setscreen', description='Set the invite screen', callback=setinvitescreen))
        # invite: admin: setjoin
        invitex_admin.add_command(app_commands.Command(name='setjoin', description='Set the join message', callback=setjoin))
        # invite: admin: setleave
        invitex_admin.add_command(app_commands.Command(name='setleave', description='Set the leave message', callback=setleave))
        # invite: admin: setwelcomeimage
        invitex_admin.add_command(app_commands.Command(name='setwelcomeimage', description='Set the welcome image', callback=setwelcomeimage))
        invitex.add_command(invitex_admin)
        self.tree.add_command(invitex)
        # moderation group
        moderationx = app_commands.Group(name='admin', description='Moderation admin commands', default_permissions=discord.Permissions(administrator=True))
        # moderation: unban
        moderationx.add_command(app_commands.Command(name='unban', description='Unban a user', callback=unban))
        # moderation: setboostmessage
        moderationx.add_command(app_commands.Command(name='setboostmessage', description='Set the boost message', callback=setboostmessage))
        # moderation: removeselfrole
        moderationx.add_command(app_commands.Command(name='removeselfrole', description='Remove a selfrole', callback=removeselfrole))
        # moderation: removerole
        moderationx.add_command(app_commands.Command(name='removerole', description='Remove a role from a user', callback=removerole))
        # moderation: removereactionrole
        moderationx.add_command(app_commands.Command(name='removereactionrole', description='Remove a reaction role', callback=removereactionrole))
        # moderation: removeautorole
        moderationx.add_command(app_commands.Command(name='removeautorole', description='Remove an autorole', callback=removeautorole))
        # moderation: purge
        moderationx.add_command(app_commands.Command(name='purge', description='Purge messages', callback=purge))
        # moderation: nuke
        moderationx.add_command(app_commands.Command(name='nuke', description='Nuke a channel', callback=nuke))
        # moderation: kick
        moderationx.add_command(app_commands.Command(name='kick', description='Kick a user', callback=kick))
        # moderation: editrole
        moderationx.add_command(app_commands.Command(name='editrole', description='Edit a role', callback=editrole))
        # moderation: editchannel
        moderationx.add_command(app_commands.Command(name='editchannel', description='Edit a channel', callback=editchannel))
        # moderation: deleterole
        moderationx.add_command(app_commands.Command(name='deleterole', description='Delete a role', callback=delete_role))
        # moderation: deletechannel
        moderationx.add_command(app_commands.Command(name='deletechannel', description='Delete a channel', callback=deletechannel))
        # moderation: createrole
        moderationx.add_command(app_commands.Command(name='createrole', description='Create a role', callback=create_role))
        # moderation: createchannel
        moderationx.add_command(app_commands.Command(name='createchannel', description='Create a channel', callback=createchannel))
        # moderation: ban
        moderationx.add_command(app_commands.Command(name='ban', description='Ban a user', callback=ban))
        # moderation: assignrole
        moderationx.add_command(app_commands.Command(name='assignrole', description='Assign a role to a user', callback=assignrole))
        # moderation: addselfrole
        moderationx.add_command(app_commands.Command(name='addselfrole', description='Add a selfrole', callback=addselfrole))
        # moderation: addreactionrole
        moderationx.add_command(app_commands.Command(name='addreactionrole', description='Add a reaction role', callback=addreactionrole))
        # moderation: addautorole
        moderationx.add_command(app_commands.Command(name='addautorole', description='Add an autorole', callback=addautorole))
        # moderation: addroletoall
        moderationx.add_command(app_commands.Command(name='addroletoall', description='Add a role to all users', callback=addroletoall))
        # moderation: removerolefromall
        moderationx.add_command(app_commands.Command(name='removerolefromall', description='Remove a role from all users', callback=removerolefromall))
        moderationxnoadmin = app_commands.Group(name='moderation', description='Moderation commands')
        # moderation: selfroles
        moderationxnoadmin.add_command(app_commands.Command(name='selfroles', description='View the selfroles', callback=selfroles))
        # moderation: autodelete
        moderationxnoadmin.add_command(app_commands.Command(name='autodelete', description='Toggle autodelete in a channel', callback=autodelete))
        # moderation: autoping
        moderationxnoadmin.add_command(app_commands.Command(name='autoping', description='Toggle autoping in a channel', callback=autoping))
        moderationxnoadmin.add_command(moderationx)
        self.tree.add_command(moderationxnoadmin)
        # xp group
        xpx = app_commands.Group(name='xp', description='XP commands')
        # xp: leaderboard
        xpx.add_command(app_commands.Command(name='leaderboard', description='View the XP leaderboard', callback=xp_leaderboard))
        # xp: level
        xpx.add_command(app_commands.Command(name='level', description='View your level', callback=level))
        # xp: rewards
        xpx.add_command(app_commands.Command(name='rewards', description='View the XP Level rewards', callback=xp_rewards))
        xpx_admin = app_commands.Group(name='admin', description='XP admin commands', default_permissions=discord.Permissions(administrator=True))
        # xp: admin: addreward
        xpx_admin.add_command(app_commands.Command(name='addreward', description='Add an XP Level reward role', callback=addreward))
        # xp: admin: removereward
        xpx_admin.add_command(app_commands.Command(name='removereward', description='Remove an XP Level reward role', callback=removereward))
        # xp: admin: addxp
        xpx_admin.add_command(app_commands.Command(name='addxp', description='Add XP to a user', callback=addxp))
        # xp: admin: removexp
        xpx_admin.add_command(app_commands.Command(name='removexp', description='Remove XP from a user', callback=removexp))
        # xp: admin: setlevelupchannel
        xpx_admin.add_command(app_commands.Command(name='setchannel', description='Set the level up channel', callback=setlevelupchannel))
        xpx.add_command(xpx_admin)
        self.tree.add_command(xpx)
        # stats group
        statsx = app_commands.Group(name='stats', description='Server Stats commands', default_permissions=discord.Permissions(administrator=True))
        # stats: setmembers
        statsx.add_command(app_commands.Command(name='setmembers', description='Set the member count channel', callback=setmembers))
        # stats: setbots
        statsx.add_command(app_commands.Command(name='setbots', description='Set the bot count channel', callback=setbots))
        # stats: setonline
        statsx.add_command(app_commands.Command(name='setonline', description='Set the online count channel', callback=setonline))
        # stats: setoffline
        statsx.add_command(app_commands.Command(name='setoffline', description='Set the offline count channel', callback=setoffline))
        # stats: setboosters
        statsx.add_command(app_commands.Command(name='setboosters', description='Set the booster count channel', callback=setboosters))
        # stats: setboostlevel
        statsx.add_command(app_commands.Command(name='setboostlevel', description='Set the boost level count channel', callback=setboostlevel))
        # stats: setboosttiers
        statsx.add_command(app_commands.Command(name='setboosttiers', description='Set the boost tier count channel', callback=setboosttiers))
        # stats: setadmins
        statsx.add_command(app_commands.Command(name='setadmins', description='Set the admin count channel', callback=setadmins))
        self.tree.add_command(statsx)
        # autoresponse group
        autoresponsex = app_commands.Group(name='autoresponse', description='Autoresponses | Custom commands', default_permissions=discord.Permissions(administrator=True))
        # autoresponse: add 
        autoresponsex.add_command(app_commands.Command(name='add', description='Add an autoresponse', callback=addresponse))
        # autoresponse: remove
        autoresponsex.add_command(app_commands.Command(name='remove', description='Remove an autoresponse', callback=removeresponse))
        # autoresponse: list
        autoresponsex.add_command(app_commands.Command(name='list', description='List the autoresponses', callback=listresponses))
        self.tree.add_command(autoresponsex)
        # automod group
        automodx = app_commands.Group(name='automod', description='Automoderation commands', default_permissions=discord.Permissions(administrator=True))
        # automod: block group
        blockx = app_commands.Group(name='block', description='Block commands')
        # automod: block: add
        blockx.add_command(app_commands.Command(name='add', description='Add a blocked word / regex', callback=addblock))
        # automod: block: remove
        blockx.add_command(app_commands.Command(name='remove', description='Remove a blocked word / regex', callback=removeblock))
        # automod: block: list
        blockx.add_command(app_commands.Command(name='list', description='List the blocked words / regex', callback=listblocks))
        automodx.add_command(blockx)
        autox = app_commands.Group(name='ai', description='Think commands', default_permissions=discord.Permissions(administrator=True))
        autox.add_command(app_commands.Command(name='activate', description='Activate Artificial Intelligence',callback=activate_automod))
        autox.add_command(app_commands.Command(name='deactivate', description='Deactivate Artificial Intelligence',callback=deactivate_automod))
        automodx.add_command(autox)
        self.tree.add_command(automodx)
        # backup group
        backupx = app_commands.Group(name='backup', description='Backup commands', default_permissions=discord.Permissions(administrator=True))
        # backup: create
        backupx.add_command(app_commands.Command(name='create', description='Create a backup', callback=create_backup))
        # backup: list
        backupx.add_command(app_commands.Command(name='list', description='List the backups', callback=list_backups))
        # backup: restore
        backupx.add_command(app_commands.Command(name='restore', description='Restore a backup', callback=restore_backup))
        self.tree.add_command(backupx)
        # Bump group
        bumpx = app_commands.Group(name='share', description='Share commands')
        # Share: setup
        bumpx.add_command(app_commands.Command(name='setup', description='Setup the share system', callback=bump_setup))
        # Share: bump
        bumpx.add_command(app_commands.Command(name='bump', description='Bump the server', callback=bump))
        # Share: rewards
        bumpx.add_command(app_commands.Command(name='rewards', description='View/Edit the bump rewards', callback=bump_rewards))
        self.tree.add_command(bumpx)
        # Announce group
        announcex = app_commands.Group(name='announce', description='Announce commands', default_permissions=discord.Permissions(administrator=True))
        # Announce: twitch
        announcex.add_command(app_commands.Command(name='twitch', description='Follow a twitch channel', callback=follow_twitch))
        self.tree.add_command(announcex)
        # Game group
        gamex = app_commands.Group(name='game', description='Game commands')
        # Game: activity
        gamex.add_command(app_commands.Command(name='activity', description='Start an activity', callback=activity))
        # Game: tod group
        todx = app_commands.Group(name='tod', description='Truth or Dare commands')
        # Game: tod: truth
        todx.add_command(app_commands.Command(name='truth', description='Get a truth question', callback=truth_command))
        # Game: tod: dare
        todx.add_command(app_commands.Command(name='dare', description='Get a dare question', callback=dare_command))
        gamex.add_command(todx)
        # Meme group
        memex = app_commands.Group(name='meme', description='Meme commands')
        # Meme: random
        memex.add_command(app_commands.Command(name='random', description='Get a random meme', callback=random_meme))
        # Meme: create
        memex.add_command(app_commands.Command(name='create', description='Create a meme', callback=create_meme))
        self.tree.add_command(memex)

        self.tree.add_command(gamex)
        await self.tree.sync()
    async def on_ready(self):
        global LOADING_DATABASE, oldinvites
        for guild in client.guilds:
            for channel in guild.channels:
                if channel.id in song_queue:
                    play_next(channel.id)
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        asyncio.gather(updateStats())
        asyncio.gather(isLive())
        asyncio.gather(status_task())
        for guild in client.guilds:
            try:
                db[guild.id] = eval(open('db'+str(guild.id)+'.py','r').read())
                tickets[guild.id] = eval(open('tickets'+str(guild.id)+'.py','r').read())
            except:
                pass
        print('Loading database...')
        for guild in client.guilds:
            try:
                oldinvites[guild.id] = await guild.invites()
                print('Working: '+str(guild.id))
            except:
                print('Not working: '+str(guild.id))
        for guild in giveaways:
            for giveaway in giveaways[guild]:
                asyncio.gather(continueGiveaway(guild,giveaway))
        LOADING_DATABASE = False
        # Read
        with open('members.txt', 'r') as f:
            members = f.read().splitlines()
client = client()

def saveTickets():
    for guild in tickets:
        open('tickets'+str(guild)+'.py', 'w').write(str(tickets[guild]))

async def continueGiveaway(guildId, giveawayId):
    gwchannel = giveaways[guildId][giveawayId]['gwchannel']
    gwid = giveawayId
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.id == gwchannel:
                gwchannel = channel
                try:
                    gwmessage = await gwchannel.fetch_message(giveawayId)
                except Exception as es:
                    print(es)
                    del giveaways[guildId][giveawayId]
                    open('giveaways.py','w').write('giveaways = '+str(giveaways))
                    return
    try:
        print(gwchannel)
        int(gwchannel)
        del giveaways[guildId][giveawayId]
        open('giveaways.py','w').write('giveaways = '+str(giveaways))
        return
    except:
        pass
    gwname = giveaways[guildId][giveawayId]['gwname']
    gwprize = giveaways[guildId][giveawayId]['gwprize']
    gwtime = giveaways[guildId][giveawayId]['gwtime']
    gwinvites = giveaways[guildId][giveawayId]['gwinvites']
    gwemoji = client.get_emoji(giveaway_emoji_id)
    gwlevels = giveaways[guildId][giveawayId]['gwlevels']
    gwsponsor = giveaways[guildId][giveawayId]['gwsponsor']
    gwtime = int(gwtime)
    while gwtime > time.time()+60:
        await asyncio.sleep(60)
    while gwtime > time.time():
        await asyncio.sleep(5)
    del gwmessage
    gwmessage = await gwchannel.fetch_message(gwid)
    gwusers = []
    for reaction in gwmessage.reactions:
        try:
            if reaction.emoji == gwemoji:
                async for user in reaction.users():
                    print(user)
                    try:
                        if not guildId in db:
                            db[guildId] = {}
                        if not 'invites' in db[guildId]:
                            db[guildId] = {}
                        if not user.id in db[guildId]['invites']:
                            db[guildId]['invites'][user.id] = 0
                        if db[guildId]['invites'][user.id] >= int(gwinvites) and user.id != client.user.id:
                            if not 'xp' in db[guildId]:
                                db[guildId]['xp'] = {}
                            if not user.id in db[guildId]['xp']:
                                db[guildId]['xp'][user.id] = {'level': 0, 'xp': 0}
                            if int(db[guildId]['xp'][user.id]['level']) >= int(gwlevels):
                                gwusers.append(user.id)
                    except Exception as es:
                        print(es)
        except:
            pass
    if len(gwusers) == 0:
        await gwmessage.reply('Noone reacted or matched the requirements.')
        del giveaways[guildId][gwid]
        open('giveaways.py', 'w').write('giveaways = '+str(giveaways))
        return
    elif len(gwusers) == 1:
        winner = gwusers[0]
    else:
        winner = random.choice(gwusers)
    await gwchannel.send('<@'+str(winner)+'> won the giveaway!\nCongratulations, you now get '+str(gwprize)+'!')
    if int(gwinvites) > 0:
        if int(gwlevels) > 0:
            embed = discord.Embed(title=gwname, color = 123456, description = 'Price: '+str(gwprize)+'\nGiveaway Ended\nRequired invites: '+str(gwinvites)+'\nRequired xp level: '+str(gwlevels)+'\n'+gwsponsor + '\nWinner: <@'+str(winner)+'>')
        else:
            embed = discord.Embed(title=gwname, color = 123456, description = 'Price: '+str(gwprize)+'\nGiveaway Ended\nRequired invites: '+str(gwinvites)+'\n'+gwsponsor + '\nWinner: <@'+str(winner)+'>')
    else:
        if int(gwlevels) > 0:
            embed = discord.Embed(title=gwname, color = 123456, description = 'Price: '+str(gwprize)+'\nGiveaway Ended\n'+gwsponsor + '\nRequired xp level: '+str(gwlevels)+'\nWinner: <@'+str(winner)+'>')
        else:
            embed = discord.Embed(title=gwname, color = 123456, description = 'Price: '+str(gwprize)+'\nGiveaway Ended\n'+gwsponsor + '\nWinner: <@'+str(winner)+'>')
    try:
        await gwmessage.edit(embed=embed)
    except Exception as es:
        print(es)
        del giveaways[guildId][gwid]
        open('giveaways.py', 'w').write('giveaways = '+str(giveaways))
    del giveaways[guildId][gwid]
    open('giveaways.py', 'w').write('giveaways = '+str(giveaways))


async def truth_command(interaction: discord.Interaction):
    """Send a truth question, that needs to be answered truthfully."""
    await interaction.response.defer()
    # truth.txt
    with open('truth.txt', 'r') as f:
        data = f.read().splitlines()
    # send a random truth question
    await interaction.followup.send(data[random.randint(0, len(data) - 1)])

async def dare_command(interaction: discord.Interaction):
    """Send a dare, that needs to be completed."""
    await interaction.response.defer()
    # dare.txt
    with open('dare.txt', 'r') as f:
        data = f.read().splitlines()
    # send a random dare
    await interaction.followup.send(data[random.randint(0, len(data) - 1)])



# sendprivatemessagemodal Class
class sendprivatemessagemodal(ui.Modal, title='Send Private Message'):
    timeout = None
    privatemessageinput = ui.TextInput(label='Enter the private message', style=discord.TextStyle.long, placeholder="https://c.tenor.com/x8v1oNUOmg4AAAAd/rickroll-roll.gif", required = True, max_length=500)

    async def on_submit(self, interaction:discord.Interaction):
        # Get the user by the id
        user = client.get_user(send_private_message_modal_list[interaction.user.id])
        # Send the message
        await user.send(self.privatemessageinput.value)
        # Notify the user
        await interaction.response.send_message(f'Message sent to {user.name}\nTo add me to your server, click my profile', ephemeral=True)


send_private_message_modal_list = {}



# Context menu
@client.tree.context_menu(name="Report as bad")
async def report_as_bad(interaction: discord.Interaction, message: discord.Message):
    """Report a message as bad."""
    await interaction.response.defer()
    # Save message to database with bad_rate +1
    database = json.load(open("database.json", "r"))
    if message.content in database:
        database[message.content]["bad_rate"] += 1
    else:
        database[message.content] = {"bad_rate": 1, "good_rate": 0}
    json.dump(database, open("database.json", "w"))
    # Send a message
    await interaction.followup.send("Message reported as bad.", ephemeral=True)

@client.tree.context_menu(name="Report as good")
async def report_as_good(interaction: discord.Interaction, message: discord.Message):
    """Report a message as good."""
    await interaction.response.defer()
    # Save message to database with good_rate +1
    database = json.load(open("database.json", "r"))
    if message.content in database:
        database[message.content]["good_rate"] += 1
    else:
        database[message.content] = {"bad_rate": 0, "good_rate": 1}
    json.dump(database, open("database.json", "w"))
    # Send a message
    await interaction.followup.send("Message reported as good.", ephemeral=True)

def is_message_bad(message):
    """Check if the message is bad."""
    try:
        # Open database
        database = json.load(open("database.json", "r"))
        # If the message is in the database
        if message in database:
            # If the bad rate is higher than the good rate
            if database[message]["bad_rate"] > database[message]["good_rate"]:
                # Return True
                return True
        # Find most similair message
        most_similair_message = ""
        most_similair_message_rate = 0
        for message_in_database in database:
            rate = similar(message, message_in_database)
            if rate > most_similair_message_rate:
                most_similair_message = message_in_database
                most_similair_message_rate = rate
        # If the most similair message is bad
        if database[most_similair_message]["bad_rate"] > database[most_similair_message]["good_rate"]:
            # Return True
            return True
        # Return False
        return False
    except:
        # Return False
        return False

def similar(a, b):
    """Return the similarity ratio between a and b."""
    return SequenceMatcher(None, a, b).ratio()

# Context menu to send a private message
@client.tree.context_menu(name='Send message')
async def send_private_message(interaction: discord.Interaction, member: discord.Member):
    send_private_message_modal_list[interaction.user.id] = member.id
    await interaction.response.send_modal(sendprivatemessagemodal())


# Context menu to see the member's info
@client.tree.context_menu(name='Information')
async def user_info(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title='Member info', description=f'{member.name}#{member.discriminator}', color=0x00ff00)
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name='ID', value=member.id, inline=False)
    embed.add_field(name='Status', value=member.status, inline=False)
    embed.add_field(name='Joined at', value=member.joined_at, inline=False)
    embed.add_field(name='Created at', value=member.created_at, inline=False)
    embed.add_field(name='Roles', value=', '.join([role.name for role in member.roles]), inline=False)
    embed.add_field(name='Voice channel', value=member.voice.channel.name if member.voice else 'None', inline=False)
    embed.add_field(name='Nickname', value=member.nick, inline=False)
    embed.add_field(name='Bot', value=member.bot, inline=False)
    embed.add_field(name='Game', value=member.activity.name if member.activity else 'None', inline=False)
    embed.add_field(name='Top role', value=member.top_role.name, inline=False)
    embed.add_field(name='Color', value=member.color, inline=False)
    embed.set_footer(text=f'These are the latest infos about {member.name}')
    await interaction.response.send_message('To add me to your server, click my profile', embed = embed, ephemeral=True)



# Context menu to mute the member
@client.tree.context_menu(name='Mute')
async def mute(interaction: discord.Interaction, member: discord.Member):
    if member.id == interaction.user.id:
        await interaction.response.send_message('You can\'t mute yourself!', ephemeral=True)
        return
    if member.id == client.user.id:
        await interaction.response.send_message('I can\'t mute myself!', ephemeral=True)
        return
    if member.id == member.guild.owner_id:
        await interaction.response.send_message('I can\'t mute the owner!', ephemeral=True)
        return
    if member.guild.owner_id != member.id:
        if member.top_role.position >= interaction.user.top_role.position and interaction.user.id != member.guild.owner_id:
            await interaction.response.send_message('I can\'t mute someone with the same or higher role!', ephemeral=True)
            return
    bot = member.guild.get_member(client.user.id)
    if member.top_role.position >= bot.top_role.position and member.top_role.position != 0:
        await interaction.response.send_message('I can\'t mute someone with the same or higher role than I have!', ephemeral=True)
        return
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message('I can\'t mute someone if you don\'t have the mute_members permission!', ephemeral=True)
        return
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_guild:
                await interaction.response.send_message('I can\'t mute someone if I don\'t have the mute_members permission!', ephemeral=True)
                return
    try:
        await member.send(f'You have been muted in {member.guild.name}')
    except:
        pass
    endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(member.guild.id, member.id)
    headers = {
        'Authorization': 'Bot ' + TOKEN,
    }
    data = {
        'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).isoformat()
    }
    response = await AsyncClient.patch(endpoint, headers=headers, json=data)
    if response.status_code >= 200 and response.status_code < 300:
        await interaction.response.send_message(f'{member.name} has been muted!\nTo add me to your server, click my profile', ephemeral=True)
    else:
        await interaction.response.send_message('I couldn\'t mute the member!', ephemeral=True)

# Context menu to translate the message
@client.tree.context_menu(name='Translate')
async def translate(interaction: discord.Interaction, message: discord.Message):
    # Send deferred response
    await interaction.response.defer(ephemeral=True)
    # https://libretranslate.com/translate
    headers = {
        'authority': 'libretranslate.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,it;q=0.8',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryBp7m4ePdyyrr06QU',
        # requests sorts cookies= alphabetically
        # 'cookie': '_ga=GA1.1.821781889.1662635212; _ga_KPKM1EP5EW=GS1.1.1662635212.1.1.1662635278.0.0.0',
        'origin': 'https://libretranslate.com',
        'referer': 'https://libretranslate.com/?source=auto&target=es&q=test1',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    data = '------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="q"\r\n\r\n{}\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="source"\r\n\r\nauto\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="target"\r\n\r\nes\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU--'.format(message.content)
    translate_it = await AsyncClient.post('https://libretranslate.com/translate', headers=headers, data=data)
    translate_it = translate_it.json()
    data = '------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="q"\r\n\r\n{}\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="source"\r\n\r\nauto\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="target"\r\n\r\nen\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU--'.format(translate_it['translatedText'])
    translate_en = await AsyncClient.post('https://libretranslate.com/translate', headers=headers, data=data)
    translate_en = translate_en.json()
    data = '------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="q"\r\n\r\n{}\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="source"\r\n\r\nauto\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="target"\r\n\r\nen\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU--'.format(message.content)
    translate_es = await AsyncClient.post('https://libretranslate.com/translate', headers=headers, data=data)
    translate_es = translate_es.json()
    data = '------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="q"\r\n\r\n{}\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="source"\r\n\r\nauto\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="target"\r\n\r\nfr\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU--'.format(message.content)
    translate_fr = await AsyncClient.post('https://libretranslate.com/translate', headers=headers, data=data)
    translate_fr = translate_fr.json()
    data = '------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="q"\r\n\r\n{}\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="source"\r\n\r\nauto\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="target"\r\n\r\nde\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU--'.format(message.content)
    translate_de = await AsyncClient.post('https://libretranslate.com/translate', headers=headers, data=data)
    translate_de = translate_de.json()
    data = '------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="q"\r\n\r\n{}\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="source"\r\n\r\nauto\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="target"\r\n\r\nru\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU--'.format(message.content)
    translate_ru = await AsyncClient.post('https://libretranslate.com/translate', headers=headers, data=data)
    translate_ru = translate_ru.json()
    data = '------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="q"\r\n\r\n{}\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="source"\r\n\r\nauto\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="target"\r\n\r\nja\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU--'.format(message.content)
    translate_ja = await AsyncClient.post('https://libretranslate.com/translate', headers=headers, data=data)
    translate_ja = translate_ja.json()
    data = '------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="q"\r\n\r\n{}\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="source"\r\n\r\nauto\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU\r\nContent-Disposition: form-data; name="target"\r\n\r\nzh\r\n------WebKitFormBoundaryBp7m4ePdyyrr06QU--'.format(message.content)
    translate_zh = await AsyncClient.post('https://libretranslate.com/translate', headers=headers, data=data)
    translate_zh = translate_zh.json()

    embed = discord.Embed(title='Translation', description=f'{message.content}', color=0x00ff00)
    embed.set_author(name=message.author.name, icon_url=message.author.avatar)
    embed.add_field(name='English', value=translate_en['translatedText'], inline=False)
    embed.add_field(name='Italian', value=translate_it['translatedText'], inline=False)
    embed.add_field(name='Spanish', value=translate_es['translatedText'], inline=False)
    embed.add_field(name='French', value=translate_fr['translatedText'], inline=False)
    embed.add_field(name='German', value=translate_de['translatedText'], inline=False)
    embed.add_field(name='Russian', value=translate_ru['translatedText'], inline=False)
    embed.add_field(name='Japanese', value=translate_ja['translatedText'], inline=False)
    embed.add_field(name='Chinese', value=translate_zh['translatedText'], inline=False)
    embed.set_footer(text=f'Translated by {client.user.name}')
    await message.reply(embed=embed, mention_author=False)
    # Send a success message to the user
    await interaction.followup.send('Translation sent!', ephemeral=True)



# Command to purge messages
async def purge(interaction: discord.Interaction, *, amount: int):
    """Purge messages"""
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message('You don\'t have the manage_messages permission!', ephemeral=True)
        return
    if not interaction.user.guild_permissions.read_message_history:
        await interaction.response.send_message('You don\'t have the read_message_history permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_messages:
                await interaction.response.send_message('I don\'t have the manage_messages permission!', ephemeral=True)
                return
            if not memberx.guild_permissions.read_message_history:
                await interaction.response.send_message('I don\'t have the read_message_history permission!', ephemeral=True)
                return
    if amount > 100:
        await interaction.response.send_message('You can\'t purge more than 100 messages at once!', ephemeral=True)
        return
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f'{amount} messages have been purged!', ephemeral=True)


# Command to nuke a channel
async def nuke(interaction: discord.Interaction, *, channel: discord.TextChannel):
    """Nuke a channel"""
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message('You don\'t have the manage_channels permission!', ephemeral=True)
        return
    if not interaction.user.guild_permissions.read_message_history:
        await interaction.response.send_message('You don\'t have the read_message_history permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_channels:
                await interaction.response.send_message('I don\'t have the manage_channels permission!', ephemeral=True)
                return
            if not memberx.guild_permissions.read_message_history:
                await interaction.response.send_message('I don\'t have the read_message_history permission!', ephemeral=True)
                return
    if not channel.permissions_for(interaction.user).manage_channels:
        await interaction.response.send_message('You don\'t have the manage_channel permission!', ephemeral=True)
        return
    if not channel.permissions_for(interaction.user).read_message_history:
        await interaction.response.send_message('You don\'t have the read_message_history permission!', ephemeral=True)
        return
    new_channel = await channel.clone()
    await new_channel.edit(position=channel.position)
    await channel.delete()
    await interaction.response.send_message(f'{channel.name} has been nuked!', ephemeral=True)


# Command to delete a channel
async def deletechannel(interaction: discord.Interaction, *, channel: discord.TextChannel):
    """Delete a channel"""
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message('You don\'t have the manage_channels permission!', ephemeral=True)
        return
    if not interaction.user.guild_permissions.read_message_history:
        await interaction.response.send_message('You don\'t have the read_message_history permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_channels:
                await interaction.response.send_message('I don\'t have the manage_channels permission!', ephemeral=True)
                return
            if not memberx.guild_permissions.read_message_history:
                await interaction.response.send_message('I don\'t have the read_message_history permission!', ephemeral=True)
                return
    if not channel.permissions_for(interaction.user).manage_channels:
        await interaction.response.send_message('You don\'t have the manage_channel permission!', ephemeral=True)
        return
    if not channel.permissions_for(interaction.user).read_message_history:
        await interaction.response.send_message('You don\'t have the read_message_history permission!', ephemeral=True)
        return
    await channel.delete()
    await interaction.response.send_message(f'{channel.name} has been deleted!', ephemeral=True)


# Command to delete a role
async def delete_role(interaction: discord.Interaction, *, role: discord.Role):
    """Delete a role"""
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('You don\'t have the manage_roles permission!', ephemeral=True)
        return
    if not interaction.user.guild_permissions.read_message_history:
        await interaction.response.send_message('You don\'t have the read_message_history permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_roles:
                await interaction.response.send_message('I don\'t have the manage_roles permission!', ephemeral=True)
                return
            if not memberx.guild_permissions.read_message_history:
                await interaction.response.send_message('I don\'t have the read_message_history permission!', ephemeral=True)
                return
    if not role.permissions_for(interaction.user).manage_roles:
        await interaction.response.send_message('You don\'t have the managerole permission!', ephemeral=True)
        return
    if not role.permissions_for(interaction.user).read_message_history:
        await interaction.response.send_message('You don\'t have the read_message_history permission!', ephemeral=True)
        return
    await role.delete()
    await interaction.response.send_message(f'{role.name} has been deleted!', ephemeral=True)


# Modal to create a channel
class CreateChannelModal(ui.Modal, title='Create Channel'):
    timeout = None
    channel_name = ui.TextInput(label='Channel Name', placeholder='', max_length=100, style=discord.TextStyle.short)
    channel_type = ui.TextInput(label='Channel Type', placeholder='text', max_length=100, style=discord.TextStyle.short)
    channel_topic = ui.TextInput(label='Channel Topic', placeholder='', max_length=100, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.guild.create_text_channel(self.channel_name.value, topic=self.channel_topic.value, category=interaction.channel.category)
        await interaction.response.send_message(f'{self.channel_name.value} has been created!', ephemeral=True)


# Command to create a channel
async def createchannel(interaction: discord.Interaction):
    """Create a channel"""
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message('You don\'t have the manage_channels permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_channels:
                await interaction.response.send_message('I don\'t have the manage_channels permission!', ephemeral=True)
                return
    await interaction.response.send_modal(CreateChannelModal())


edit_channel_modal = {}

# Modal to edit a channel
class EditChannelModal(ui.Modal, title='Edit Channel'):
    timeout = None
    channel_name = ui.TextInput(label='Channel Name', placeholder='', max_length=100, style=discord.TextStyle.short)
    channel_topic = ui.TextInput(label='Channel Topic', placeholder='', max_length=100, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await edit_channel_modal[interaction.user.id].edit(name=self.channel_name.value, topic=self.channel_topic.value)
        await interaction.response.send_message(f'{self.channel_name.value} has been edited!', ephemeral=True)


# Command to edit a channel
async def editchannel(interaction: discord.Interaction, *, channel: discord.TextChannel):
    """Edit a channel"""
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message('You don\'t have the manage_channels permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_channels:
                await interaction.response.send_message('I don\'t have the manage_channels permission!', ephemeral=True)
                return
    if not channel.permissions_for(interaction.user).manage_channels:
        await interaction.response.send_message('You don\'t have the manage_channel permission!', ephemeral=True)
        return
    edit_channel_modal[interaction.user.id] = channel
    await interaction.response.send_modal(EditChannelModal())


# Modal to create a role
class CreateRoleModal(ui.Modal, title='Create Role'):
    timeout = None
    role_name = ui.TextInput(label='Role Name', placeholder='', max_length=100, style=discord.TextStyle.short)
    role_color = ui.TextInput(label='Role Color', placeholder='', max_length=100, style=discord.TextStyle.short)
    role_permissions = ui.TextInput(label='Is Administrator', placeholder='false', max_length=100, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        if self.role_permissions.value == 'true':
            await interaction.guild.create_role(name=self.role_name.value, color=discord.Color(int(self.role_color.value, 16)), permissions=discord.Permissions(administrator=True))
        else:
            await interaction.guild.create_role(name=self.role_name.value, color=discord.Color(int(self.role_color.value, 16)))
        await interaction.response.send_message(f'{self.role_name.value} has been created!', ephemeral=True)


# Command to create a role
async def create_role(interaction: discord.Interaction):
    """Create a role"""
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('You don\'t have the manage_roles permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_roles:
                await interaction.response.send_message('I don\'t have the manage_roles permission!', ephemeral=True)
                return
    await interaction.response.send_modal(CreateRoleModal())


editrole_modal = {}


# Modal to edit a role
class EditRoleModal(ui.Modal, title='Edit Role'):
    timeout = None
    role_name = ui.TextInput(label='Role Name', placeholder='', max_length=100, style=discord.TextStyle.short)
    role_color = ui.TextInput(label='Role Color', placeholder='', max_length=100, style=discord.TextStyle.short)
    role_permissions = ui.TextInput(label='Is Administrator', placeholder='false', max_length=100, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        if self.role_permissions.value == 'true':
            await editrole_modal[interaction.user.id].edit(name=self.role_name.value, color=discord.Color(int(self.role_color.value, 16)), permissions=discord.Permissions(administrator=True))
        else:
            await editrole_modal[interaction.user.id].edit(name=self.role_name.value, color=discord.Color(int(self.role_color.value, 16)), permissions=discord.Permissions(administrator=False))
        await interaction.response.send_message(f'{self.role_name.value} has been edited!', ephemeral=True)
    

# Command to edit a role
async def editrole(interaction: discord.Interaction, *, role: discord.Role):
    """Edit a role"""
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('You don\'t have the manage_roles permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_roles:
                await interaction.response.send_message('I don\'t have the manage_roles permission!', ephemeral=True)
                return
    editrole_modal[interaction.user.id] = role
    await interaction.response.send_modal(EditRoleModal())


# Command to assign a role to a user
async def assignrole(interaction: discord.Interaction, *, user: discord.Member, role: discord.Role):
    """Assign a role to a user"""
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('You don\'t have the manage_roles permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_roles:
                await interaction.response.send_message('I don\'t have the manage_roles permission!', ephemeral=True)
                return
    if role.position >= interaction.user.top_role.position:
        await interaction.response.send_message('You can\'t assign a role that is higher than or equal your highest role!', ephemeral=True)
        return
    await user.add_roles(role)
    await interaction.response.send_message(f'{user.name} has been assigned the {role.name} role!', ephemeral=True)

# Add Role To All
async def addroletoall(interaction: discord.Interaction, *, role: discord.Role):
    """Add a role to all users"""
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('You don\'t have the manage_roles permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_roles:
                await interaction.response.send_message('I don\'t have the manage_roles permission!', ephemeral=True)
                return
    if role.position >= interaction.user.top_role.position:
        await interaction.response.send_message('You can\'t assign a role that is higher than or equal your highest role!', ephemeral=True)
        return
    # Has role any moderator perms
    if role.permissions.administrator or role.permissions.ban_members or role.permissions.kick_members or role.permissions.manage_channels or role.permissions.manage_guild or role.permissions.manage_messages or role.permissions.manage_nicknames or role.permissions.manage_roles or role.permissions.manage_webhooks or role.permissions.mute_members or role.permissions.move_members or role.permissions.priority_speaker or role.permissions.mention_everyone or role.permissions.manage_emojis or role.permissions.manage_threads:
        await interaction.response.send_message('You can\'t assign a role that has moderator permissions!', ephemeral=True)
        return
    await interaction.response.send_message(f'Everyone has been assigned the {role.name} role!', ephemeral=True)
    for member in await interaction.guild.chunk():
        await member.add_roles(role)

# Remove Role From All
async def removerolefromall(interaction: discord.Interaction, *, role: discord.Role):
    """Remove a role from all users"""
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('You don\'t have the manage_roles permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_roles:
                await interaction.response.send_message('I don\'t have the manage_roles permission!', ephemeral=True)
                return
    if role.position >= interaction.user.top_role.position:
        await interaction.response.send_message('You can\'t assign a role that is higher than or equal your highest role!', ephemeral=True)
        return
    # Has role any moderator perms
    if role.permissions.administrator or role.permissions.ban_members or role.permissions.kick_members or role.permissions.manage_channels or role.permissions.manage_guild or role.permissions.manage_messages or role.permissions.manage_nicknames or role.permissions.manage_roles or role.permissions.manage_webhooks or role.permissions.mute_members or role.permissions.move_members or role.permissions.priority_speaker or role.permissions.mention_everyone or role.permissions.manage_emojis or role.permissions.manage_threads:
        await interaction.response.send_message('You can\'t assign a role that has moderator permissions!', ephemeral=True)
        return
    await interaction.response.send_message(f'Everyone has been removed from the {role.name} role!', ephemeral=True)
    for member in await interaction.guild.chunk():
        await member.remove_roles(role)


# Command to remove a role from a user
async def removerole(interaction: discord.Interaction, *, user: discord.Member, role: discord.Role):
    """Remove a role from a user"""
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('You don\'t have the manage_roles permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_roles:
                await interaction.response.send_message('I don\'t have the manage_roles permission!', ephemeral=True)
                return
    if role.position >= interaction.user.top_role.position:
        await interaction.response.send_message('You can\'t remove a role that is higher than or equal your highest role!', ephemeral=True)
        return
    await user.remove_roles(role)
    await interaction.response.send_message(f'{user.name} has been removed from the {role.name} role!', ephemeral=True)


# Command to remove all roles from a user
@client.tree.command(name='remove_roles')
async def remove_roles(interaction: discord.Interaction, *, user: discord.Member):
    """Remove all roles from a user"""
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message('You don\'t have the manage_roles permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.manage_roles:
                await interaction.response.send_message('I don\'t have the manage_roles permission!', ephemeral=True)
                return
    if user.top_role.position >= interaction.user.top_role.position:
        await interaction.response.send_message('You can\'t remove all roles that are higher than or equal your highest role!', ephemeral=True)
        return
    await user.remove_roles(*user.roles)
    await interaction.response.send_message(f'{user.name} has been removed from all roles!', ephemeral=True)


# Command to kick and notify a user
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    """Kick a user and notify them"""
    if member.id == interaction.user.id:
        await interaction.response.send_message('You can\'t kick yourself!', ephemeral=True)
        return
    if member.id == client.user.id:
        await interaction.response.send_message('I can\'t kick myself!', ephemeral=True)
        return
    if member.id == member.guild.owner_id:
        await interaction.response.send_message('I can\'t kick the owner!', ephemeral=True)
        return
    if member.guild.owner_id != member.id:
        if member.top_role.position >= interaction.user.top_role.position and interaction.user.id != member.guild.owner_id:
            await interaction.response.send_message('I can\'t kick someone with the same or higher role!', ephemeral=True)
            return
    bot = member.guild.get_member(client.user.id)
    if member.top_role.position >= bot.top_role.position and interaction.user.id != member.guild.owner_id:
        await interaction.response.send_message('I can\'t kick someone with the same or higher role than I have!', ephemeral=True)
        return
    if not member.guild_permissions.kick_members and member.top_role.position != 0:
        await interaction.response.send_message('I can\'t kick someone if you don\'t have the mute_members permission!', ephemeral=True)
        return
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.kick_members:
                await interaction.response.send_message('I can\'t kick someone if I don\'t have the mute_members permission!', ephemeral=True)
                return
    try:
        await member.send(f'You have been kicked from {member.guild.name} for the following reason: {reason}')
    except:
        pass
    await member.kick(reason=reason)
    await interaction.response.send_message(f'{member.name} has been kicked!', ephemeral=True)


# Command to ban and notify a user
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    """Ban a user and notify them"""
    if member.id == interaction.user.id:
        await interaction.response.send_message('You can\'t ban yourself!', ephemeral=True)
        return
    if member.id == client.user.id:
        await interaction.response.send_message('I can\'t ban myself!', ephemeral=True)
        return
    if member.id == member.guild.owner_id:
        await interaction.response.send_message('I can\'t ban the owner!', ephemeral=True)
        return
    if member.guild.owner_id != member.id:
        if member.top_role.position >= interaction.user.top_role.position and interaction.user.id != member.guild.owner_id:
            await interaction.response.send_message('I can\'t ban someone with the same or higher role!', ephemeral=True)
            return
    bot = member.guild.get_member(client.user.id)
    if member.top_role.position >= bot.top_role.position and interaction.user.id != member.guild.owner_id:
        await interaction.response.send_message('I can\'t ban someone with the same or higher role than I have!', ephemeral=True)
        return
    if not member.guild_permissions.ban_members and member.top_role.position != 0:
        await interaction.response.send_message('I can\'t ban someone if you don\'t have the ban_members permission!', ephemeral=True)
        return
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.ban_members:
                await interaction.response.send_message('I can\'t ban someone if I don\'t have the ban_members permission!', ephemeral=True)
                return
    try:
        await member.send(f'You have been banned from {member.guild.name} for the following reason: {reason}')
    except:
        pass
    await member.ban(reason=reason)
    await interaction.response.send_message(f'{member.name} has been banned!', ephemeral=True)


# Command to unban and notify a user
async def unban(interaction: discord.Interaction, *, user: discord.User):
    """Unban a user and notify them"""
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message('You don\'t have the ban_members permission!', ephemeral=True)
        return
    bot = interaction.user.guild.get_member(client.user.id)
    for memberx in interaction.guild.members:
        if memberx.id == client.user.id:
            if not memberx.guild_permissions.ban_members:
                await interaction.response.send_message('I don\'t have the ban_members permission!', ephemeral=True)
                return
    try:
        await user.send(f'You have been unbanned from {interaction.user.guild.name}')
    except:
        pass
    await interaction.guild.unban(user)
    await interaction.response.send_message(f'{user.name} has been unbanned!', ephemeral=True)

# Context menu to set sticky message
@client.tree.context_menu(name='Set Sticky')
async def sticky(interaction: discord.Interaction, message: discord.Message):
    """Set a message as sticky"""
    if not interaction.user.id ==963125433770070096:
        for members in interaction.guild.members:
            if members.id == interaction.user.id:
                if not members.guild_permissions.manage_messages:
                    await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                    return
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message('You don\'t have the manage_messages permission!', ephemeral=True)
            return
    bot = interaction.user.guild.get_member(client.user.id)
    if not bot.guild_permissions.manage_messages:
        await interaction.response.send_message('I don\'t have the manage_messages permission!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'sticky' in db[interaction.guild.id]:
        db[interaction.guild.id]['sticky'] = {}
    if not 'sticky-embed' in db[interaction.guild.id]:
        db[interaction.guild.id]['sticky-embed'] = {}
    if not 'sticky-attachments' in db[interaction.guild.id]:
        db[interaction.guild.id]['sticky-attachments'] = {}
    if not message.channel.id in db[interaction.guild.id]['sticky']:
        db[interaction.guild.id]['sticky'][message.channel.id] = message.content
    else:
        db[interaction.guild.id]['sticky'][message.channel.id] = message.content
    if len(message.embeds) > 0:
        if not message.channel.id in db[interaction.guild.id]['sticky-embed']:
            db[interaction.guild.id]['sticky-embed'][message.channel.id] = message.embeds[0].to_dict()
        else:
            db[interaction.guild.id]['sticky-embed'][message.channel.id] = message.embeds[0].to_dict()
    else:
        db[interaction.guild.id]['sticky-embed'][message.channel.id] = None
    if len(message.attachments) > 0:
        if not message.channel.id in db[interaction.guild.id]['sticky-attachments']:
            db[interaction.guild.id]['sticky-attachments'][message.channel.id] = message.attachments[0].url
        else:
            db[interaction.guild.id]['sticky-attachments'][message.channel.id] = message.attachments[0].url
    else:
        db[interaction.guild.id]['sticky-attachments'][message.channel.id] = None
    await interaction.response.send_message(f'{message.channel.mention}\'s sticky message has been set to {message.content}!', ephemeral=True)
    saveDb()

doEmbedMention = []

# Modal to create an embed
class EmbedModal(ui.Modal, title='Create an embed'):
    timeout = None
    titletext = ui.TextInput(label='Title', placeholder='', max_length=256)
    description = ui.TextInput(label='Description', placeholder='', max_length=2048, style=discord.TextStyle.long)
    color = ui.TextInput(label='Color', placeholder=0xffffff)
    footer = ui.TextInput(label='Footer', placeholder='', max_length=2048)
    image = ui.TextInput(label='Image', placeholder='', max_length=2048)

    async def on_submit(self, interaction: discord.Interaction):
        global doEmbedMention
        embed = discord.Embed(title=self.titletext.value, description=self.description.value, color=int(self.color.value, 16))
        if self.footer.value:
            embed.set_footer(text=self.footer.value)
        if self.image.value:
            embed.set_image(url=self.image.value)
        if interaction.user.id in doEmbedMention:
            await interaction.response.send_message(content = '@everyone', embed=embed)
        else:
            await interaction.response.send_message(embed=embed)
        doEmbedMention.remove(interaction.user.id)


async def embed(interaction: discord.Interaction, mention: bool = False):
    """Create an embed"""
    global doEmbedMention
    if mention:
        # Check perms
        for members in interaction.guild.members:
            if members.id == interaction.user.id:
                if not members.guild_permissions.mention_everyone:
                    await interaction.response.send_message('You do not have permission to mention everyone!', ephemeral=True)
                    return
        doEmbedMention.append(interaction.user.id)
    await interaction.response.send_modal(EmbedModal())



# Modal to create a choice poll using a select menu in the message
class ChoicePollModal(ui.Modal, title='Create a choice poll'):
    timeout = None
    titletext = ui.TextInput(label='Title', placeholder='This is a poll', max_length=256)
    description = ui.TextInput(label='Description', placeholder='The description of the poll', max_length=2048, style=discord.TextStyle.long)
    choices = ui.TextInput(label='Choices', placeholder='Choice 1 | Choice 2 | Choice 3', max_length=2048)
    descriptions = ui.TextInput(label='Descriptions', placeholder='Description 1 | Description 2 | Description 3', max_length=2048)

    async def on_submit(self, interaction: discord.Interaction):
        poll_modal_votes = []
        choices = self.choices.value.split('|')
        descriptions = self.descriptions.value.split('|')
        if len(choices) != len(descriptions):
            await interaction.response.send_message('The number of choices and descriptions must be the same!', ephemeral=True)
            return
        if len(choices) < 2:
            await interaction.response.send_message('You must have at least 2 choices!', ephemeral=True)
            return
        if len(choices) > 10:
            await interaction.response.send_message('You can only have 10 choices!', ephemeral=True)
            return
        embed = discord.Embed(title=self.titletext.value, description=self.description.value)
        for i in range(len(choices)):
            embed.add_field(name=choices[i] + ' | 0 votes', value=descriptions[i])
        class Select(ui.Select):
            def __init__(self):
                options = []
                super().__init__(placeholder='Select a choice', options=options)
            async def callback(self, interaction: discord.Interaction):
                if not interaction.user.id in poll_modal_votes:
                    poll_modal_votes.append(interaction.user.id)
                    for field in embed.fields:
                        if field.name.split(' | ')[0] == self.values[0]:
                            old_choice_vote_number = int(field.name.split(' | ')[1].replace(' votes', '').replace(' vote', ''))
                    new_choice_vote_number = old_choice_vote_number + 1
                    if new_choice_vote_number == 1:
                        new_choice_vote_number = '1 vote'
                    else:
                        new_choice_vote_number = f'{new_choice_vote_number} votes'
                    for field in range(len(embed.fields)):
                        if embed.fields[field].name.split(' | ')[0] == self.values[0]:
                            embed.set_field_at(field, name=self.values[0] + ' | ' + new_choice_vote_number, value=descriptions[field])
                            break
                    
                    await sent_msg.edit(embed=embed)
                    await interaction.response.send_message('You have voted for ' + self.values[0], ephemeral=True)
                else:
                    await interaction.response.send_message('You have already voted!', ephemeral=True)
        class View(discord.ui.View):
            timeout = None
            def __init__(self):
                super().__init__()
                sel=Select()
                for option in range(len(choices)):
                    sel.options.append(discord.SelectOption(label=descriptions[option],value=choices[option]))
                self.add_item(sel)
        sent_msg = await interaction.channel.send(embed=embed,view=View())
        await interaction.response.send_message('The poll has been sent!', ephemeral=True)


# Modal to create a text poll using a modal in the message to input after clicking on the suggest button
class TextPollModal(ui.Modal, title='Create a text poll'):
    timeout = None
    titletext = ui.TextInput(label='Title', placeholder='This is a poll', max_length=256)
    description = ui.TextInput(label='Description', placeholder='The description of the poll', max_length=2048, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        poll_modal_submissions = []
        embed = discord.Embed(title=self.description.value)
        embed.set_author(name=self.titletext.value)
        class SubmissionModal(ui.Modal, title='Write a submission'):
            submission = ui.TextInput(label='Your submission', placeholder='Your submission', max_length=2048)

            async def on_submit(self, interaction: discord.Interaction):
                if not interaction.user.id in poll_modal_submissions:
                    old_choice_vote_number = 0
                    poll_modal_submissions.append(interaction.user.id)
                    for field in embed.fields:
                        if field.name.lower() == self.submission.value.lower():
                            old_choice_vote_number = int(field.value.replace(' submissions', '').replace(' submission', ''))
                    new_choice_vote_number = old_choice_vote_number + 1
                    if new_choice_vote_number == 1:
                        new_choice_vote_number = '1 submission'
                    else:
                        new_choice_vote_number = f'{new_choice_vote_number} submissions'
                    setted_field = False
                    for field in range(len(embed.fields)):
                        if embed.fields[field].name.split(' | ')[0] == self.submission.value:
                            embed.set_field_at(field, name=self.submission.value, value=new_choice_vote_number)
                            setted_field = True
                            break
                    if not setted_field:
                        embed.add_field(name=self.submission.value, value=new_choice_vote_number)
                    await sent_msg.edit(embed=embed)
                    await interaction.response.send_message('You have submitted ' + self.submission.value, ephemeral=True)
                else:
                    await interaction.response.send_message('You have already voted!', ephemeral=True)
                
        class SubmitButton(ui.Button):
            def __init__(self):
                super().__init__(label='Submit')
            async def callback(self, interaction: discord.Interaction):
                await interaction.response.send_modal(SubmissionModal())
        class View(discord.ui.View):
            timeout = None
            def __init__(self):
                super().__init__()
                self.add_item(SubmitButton())
        sent_msg = await interaction.channel.send(embed=embed,view=View())
        await interaction.response.send_message('The poll has been sent!', ephemeral=True)



async def poll(interaction: discord.Interaction, type_of_poll:str='choice'):
    """Create a poll"""
    if type_of_poll == 'choice':
        await interaction.response.send_modal(ChoicePollModal())
    elif type_of_poll == 'text':
        await interaction.response.send_modal(TextPollModal())
    else:
        await interaction.response.send_message('Invalid poll type! Valid types are: choice, text', ephemeral=True)

# Context menu to report a message
@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    """Report a message to the moderators"""
    for channel in interaction.guild.channels:
        if channel.name == 'reports':
            await interaction.response.send_message(
                f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
            )
            log_channel = channel
            embed = discord.Embed(title='Reported Message')
            if message.content:
                embed.description = message.content
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
            embed.timestamp = message.created_at
            url_view = discord.ui.View()
            url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))
            class DeleteButton(ui.Button):
                def __init__(self):
                    super().__init__(label='Delete')
                async def callback(self, interaction: discord.Interaction):
                    await message.channel.send(f'{message.author.mention}, your message from {message.created_at} has been deleted.')
                    await message.delete()
                    await interaction.response.send_message('Message deleted!', ephemeral=True)
            url_view.add_item(DeleteButton())
            await log_channel.send(embed=embed, view=url_view)
            return
    log_channel = await interaction.guild.create_text_channel('reports')
    # Remove everyone from the channel
    await log_channel.set_permissions(interaction.guild.default_role, read_messages=False)
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )
    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at
    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))
    class DeleteButton(ui.Button):
        def __init__(self):
            super().__init__(label='Delete')
        async def callback(self, interaction: discord.Interaction):
            await message.channel.send(f'{message.author.mention}, your message from {message.created_at} has been deleted.')
            await message.delete()
            await interaction.response.send_message('Message deleted!', ephemeral=True)
    url_view.add_item(DeleteButton())
    await log_channel.send(embed=embed, view=url_view)



# Cleanup invites command - Delete all invites in the server
async def cleanupinvites(interaction: discord.Interaction):
    """Delete all invites in the server"""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        return
    await interaction.response.send_message('Deleting all invites...', ephemeral=True)
    for invite in interaction.guild.invites:
        await invite.delete()
    


async def ping(interaction: discord.Interaction):
    """Check the latency of the bot"""
    start = time.monotonic()
    msg = await interaction.channel.send('Pinging -- by {}'.format(interaction.user.mention))
    end = time.monotonic()
    ping = (end - start) * 1000
    await msg.delete()
    await interaction.response.send_message('Latency: {}ms'.format(int(ping)))


# Remove auto-role command - Remove a role from the list of auto-roles
async def removeautorole(interaction: discord.Interaction, role:discord.Role):
    """Remove a role from the list of auto-roles"""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'autoroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['autoroles'] = []
    rolefound = False
    for rolex in db[interaction.guild.id]['autoroles']:
        if rolex == role.id:
            rolefound = True
            therole = rolex
    if rolefound:
        db[interaction.guild.id]['autoroles'].remove(therole)
        await interaction.response.send_message('Role removed from auto-roles!', ephemeral=True)
    else:
        await interaction.response.send_message('Role not found in auto-roles!', ephemeral=True)
    saveDb()


# Add auto-role command - Add a role to the list of auto-roles
async def addautorole(interaction: discord.Interaction, role:discord.Role):
    """Add a role to the list of auto-roles"""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'autoroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['autoroles'] = []
    if role in db[interaction.guild.id]['autoroles']:
        await interaction.response.send_message('Role already in auto-roles!', ephemeral=True)
    else:
        db[interaction.guild.id]['autoroles'].append(role.id)
        await interaction.response.send_message('Role added to auto-roles!', ephemeral=True)
    saveDb()


# resetInvites command - Reset invites of a list of users
async def resetinvites(interaction: discord.Interaction, user:discord.User):
    """Reset invites of a list of users"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'invites' in db[interaction.guild.id]:
        db[interaction.guild.id]['invites'] = {}
    if not 'joins' in db[interaction.guild.id]:
        db[interaction.guild.id]['joins'] = {}
    if not 'leaves' in db[interaction.guild.id]:
        db[interaction.guild.id]['leaves'] = {}
    db[interaction.guild.id]['invites'][user.id] = 0
    db[interaction.guild.id]['joins'][user.id] = 0
    db[interaction.guild.id]['leaves'][user.id] = 0
    await interaction.response.send_message(f'Invites reset for {user}!', ephemeral=True)
    saveDb()


# addInvites command - Add invites to a list of users
async def addinvites(interaction: discord.Interaction, user:discord.User, invites:int):
    """Add invites to a list of users"""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'invites' in db[interaction.guild.id]:
        db[interaction.guild.id]['invites'] = {}
    if not user.id in db[interaction.guild.id]['invites']:
        db[interaction.guild.id]['invites'][user.id] = 0
    db[interaction.guild.id]['invites'][user.id] += invites
    await interaction.response.send_message('{} invites added to {}!'.format(invites, user), ephemeral=True)
    saveDb()


# removeInvites command - Remove invites from a list of users
async def removeinvites(interaction: discord.Interaction, user:discord.User, invites:int):
    """Remove invites from a list of users"""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'invites' in db[interaction.guild.id]:
        db[interaction.guild.id]['invites'] = {}
    if not user.id in db[interaction.guild.id]['invites']:
        db[interaction.guild.id]['invites'][user.id] = 0
    db[interaction.guild.id]['invites'][user.id] -= invites
    if db[interaction.guild.id]['invites'][user.id] < 0:
        db[interaction.guild.id]['invites'][user.id] = 0
    await interaction.response.send_message('{} invites removed from {}!'.format(invites, user), ephemeral=True)
    saveDb()


giveaway_modal_channels = {}
gwsponsors = {}

# Giveaway creation modal - Create a giveaway
class GiveawayModal(ui.Modal, title='Create giveaway'):
    timeout = None
    gwname = ui.TextInput(label='Giveaway name', placeholder='Name of the giveaway', required=True, max_length=100)
    gwprize = ui.TextInput(label='Giveaway prize', placeholder='Price of the giveaway', required=True, max_length=100)
    gwtimetext = ui.TextInput(label='Giveaway time', placeholder='Duration of the giveaway (d, h, m, s)', required=True, max_length=100)
    gwinvites = ui.TextInput(label='Giveaway invites', placeholder='Number of invites users need to win', required=True, max_length=100)
    gwlevels = ui.TextInput(label='Giveaway xp level', placeholder='XP Level users need to win', required=True, max_length=100)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('Giveaway created!', ephemeral=True)
        gwsponsor = gwsponsors[interaction.guild.id]
        gwchannel = giveaway_modal_channels[interaction.user.id]
        gwtime = 0
        currentnumber = ''
        gwlevels = self.gwlevels.value
        for letter in self.gwtimetext.value:
            if letter.isdigit():
                currentnumber += letter
            else:
                if currentnumber != '' and currentnumber != ' ' and currentnumber != '0':
                    if letter == 'd':
                        gwtime += int(currentnumber) * 86400
                    elif letter == 'h':
                        gwtime += int(currentnumber) * 3600
                    elif letter == 'm':
                        gwtime += int(currentnumber) * 60
                    elif letter == 's':
                        gwtime += int(currentnumber)
                    currentnumber = ''
        gwtime = time.time() + gwtime
        gwtime = int(gwtime)
        gwtimer = '<t:'+str(gwtime)+':R>'
        gwemoji = client.get_emoji(giveaway_emoji_id)
        try:
            invite = await client.fetch_invite(gwsponsor)
            gwsponsorname = invite.guild.name
            gwsponsor = '\nSponsored by [{}]({})'.format(gwsponsorname, gwsponsor)
        except:
            gwsponsor = ''
        if int(self.gwinvites.value) > 0:
            if int(self.gwlevels.value) > 0:
                embed = discord.Embed(title=self.gwname.value, color = 123456, description = 'Price: '+str(self.gwprize.value)+'\nEnds: <t:'+str(gwtime)+':R>\nRequired invites: '+str(self.gwinvites.value)+'\nRequired xp level: '+str(self.gwlevels.value)+'\n'+gwsponsor)
            else:
                embed = discord.Embed(title=self.gwname.value, color = 123456, description = 'Price: '+str(self.gwprize.value)+'\nEnds: <t:'+str(gwtime)+':R>\nRequired invites: '+str(self.gwinvites.value)+'\n'+gwsponsor)
        else:
            if int(self.gwlevels.value) > 0:
                embed = discord.Embed(title=self.gwname.value, color = 123456, description = 'Price: '+str(self.gwprize.value)+'\nEnds: <t:'+str(gwtime)+':R>\nRequired xp level: '+str(self.gwlevels.value)+'\n'+gwsponsor)
            else:
                embed = discord.Embed(title=self.gwname.value, color = 123456, description = 'Price: '+str(self.gwprize.value)+'\nEnds: <t:'+str(gwtime)+':R>\n'+gwsponsor)
        gwmessage = await gwchannel.send(content='Hosted by '+interaction.user.mention, embed=embed)
        await gwmessage.add_reaction(gwemoji)
        gwid = gwmessage.id
        if not interaction.guild.id in giveaways:
            giveaways[interaction.guild.id] = {}
        giveaways[interaction.guild.id][gwid] = {'gwname': self.gwname.value, 'gwprize': self.gwprize.value, 'gwtime': gwtime, 'gwinvites': self.gwinvites.value, 'gwlevels': self.gwlevels.value, 'gwchannel': gwchannel.id, 'gwsponsor': gwsponsor}
        open('giveaways.py', 'w').write('giveaways = '+str(giveaways))
        while gwtime > time.time()+60:
            await asyncio.sleep(60)
        while gwtime > time.time():
            await asyncio.sleep(5)
        del gwmessage
        gwmessage = await gwchannel.fetch_message(gwid)
        gwusers = []
        for reaction in gwmessage.reactions:
            try:
                if reaction.emoji == gwemoji:
                    async for user in reaction.users():
                        try:
                            if not user.id in db[interaction.guild.id]['invites']:
                                db[interaction.guild.id]['invites'][user.id] = 0
                            if db[interaction.guild.id]['invites'][user.id] >= int(self.gwinvites.value) and user.id != client.user.id:
                                if not 'xp' in db[interaction.guild.id]:
                                    db[interaction.guild.id]['xp'] = {}
                                if not user.id in db[interaction.guild.id]['xp']:
                                    db[interaction.guild.id]['xp'][user.id] = {'level': 0, 'xp': 0}
                                if (db[interaction.guild.id]['xp'][user.id]['level']) >= int(gwlevels):
                                    gwusers.append(user.id)
                        except:
                            pass
            except:
                pass
        if len(gwusers) == 0:
            await gwmessage.reply('Noone reacted or matched the requirements.')
            del giveaways[guildId][gwid]
            open('giveaways.py', 'w').write('giveaways = '+str(giveaways))
            return
        elif len(gwusers) == 1:
            winner = gwusers[0]
        else:
            winner = random.choice(gwusers)
        await gwchannel.send('<@'+str(winner)+'> won the giveaway!\nCongratulations, you now get '+str(self.gwprize.value)+'!')
        if int(self.gwinvites.value) > 0:
            if int(self.gwlevels.value) > 0:
                embed = discord.Embed(title=self.gwname.value, color = 123456, description = 'Price: '+str(self.gwprize.value)+'\nGiveaway Ended\nRequired invites: '+str(self.gwinvites.value)+'\nRequired xp level: '+str(self.gwlevels.value)+'\n'+gwsponsor + '\nWinner: <@'+str(winner)+'>')
            else:
                embed = discord.Embed(title=self.gwname.value, color = 123456, description = 'Price: '+str(self.gwprize.value)+'\nGiveaway Ended\nRequired invites: '+str(self.gwinvites.value)+'\n'+gwsponsor + '\nWinner: <@'+str(winner)+'>')
        else:
            if int(self.gwlevels.value) > 0:
                embed = discord.Embed(title=self.gwname.value, color = 123456, description = 'Price: '+str(self.gwprize.value)+'\nGiveaway Ended\n'+gwsponsor + '\nRequired xp level: '+str(self.gwlevels.value)+'\nWinner: <@'+str(winner)+'>')
            else:
                embed = discord.Embed(title=self.gwname.value, color = 123456, description = 'Price: '+str(self.gwprize.value)+'\nGiveaway Ended\n'+gwsponsor + '\nWinner: <@'+str(winner)+'>')
        try:
            await gwmessage.edit(embed=embed)
        except:
            del giveaways[interaction.guild.id][gwid]
            open('giveaways.py', 'w').write('giveaways = '+str(giveaways))
        del giveaways[interaction.guild.id][gwid]
        open('giveaways.py', 'w').write('giveaways = '+str(giveaways))



async def giveaway(interaction: discord.Interaction, channel: discord.TextChannel, sponsor:str=None):
    """Create a giveaway"""
    if sponsor:
        gwsponsors[interaction.guild.id] = sponsor
    else:
        gwsponsors[interaction.guild.id] = ''
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    giveaway_modal_channels[interaction.user.id] = channel
    await interaction.response.send_modal(GiveawayModal())


# setInviteScreen command - set the invite screen
async def setinvitescreen(interaction: discord.Interaction, invites:bool = False, joins:bool = False, leaves:bool = False):
    """Set the invite screen"""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    embed = discord.Embed()
    embed.title = 'Configuration for the invite screen'
    embed.description = 'Changed by: '+interaction.user.mention
    embed.color = 123456
    guild = interaction.guild
    if not guild.id in db:
        db[guild.id] = {}
    if 'inviteScreen' in db[guild.id]:
        embed.add_field(name = 'Show Invites: Old', value = db[guild.id]['inviteScreen']['invites'])
        embed.add_field(name = 'Show Joins: Old', value = db[guild.id]['inviteScreen']['joins'])
        embed.add_field(name = 'Show Leaves: Old', value = db[guild.id]['inviteScreen']['leaves'])
        db[guild.id]['inviteScreen']['invites'] = invites
        db[guild.id]['inviteScreen']['joins'] = joins
        db[guild.id]['inviteScreen']['leaves'] = leaves
        embed.add_field(name = 'Show Invites: New', value = db[guild.id]['inviteScreen']['invites'])
        embed.add_field(name = 'Show Joins: New', value = db[guild.id]['inviteScreen']['joins'])
        embed.add_field(name = 'Show Leaves: New', value = db[guild.id]['inviteScreen']['leaves'])
    else:
        db[guild.id]['inviteScreen'] = {'invites':invites, 'joins':joins, 'leaves':leaves}
        embed.add_field(name = 'Show Invites: New', value = db[guild.id]['inviteScreen']['invites'])
        embed.add_field(name = 'Show Joins: New', value = db[guild.id]['inviteScreen']['joins'])
        embed.add_field(name = 'Show Leaves: New', value = db[guild.id]['inviteScreen']['leaves'])
    saveDb()
    await interaction.response.send_message(embed=embed, ephemeral=True)


# invites command - show the invites
async def invites(interaction: discord.Interaction, user:discord.User = None):
    """Show the invites"""
    if user == None:
        user = interaction.user
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if 'invites' in db[interaction.guild.id]:
        if user.id in db[interaction.guild.id]['invites']:
            invites = db[interaction.guild.id]['invites'][user.id]
        else:
            invites = 0
    else:
        invites = 0
    if 'joins' in db[interaction.guild.id]:
        if user.id in db[interaction.guild.id]['joins']:
            joins = db[interaction.guild.id]['joins'][user.id]
        else:
            joins = 0
    else:
        joins = 0
    if 'leaves' in db[interaction.guild.id]:
        if user.id in db[interaction.guild.id]['leaves']:
            leaves = db[interaction.guild.id]['leaves'][user.id]
        else:
            leaves = 0
    else:
        leaves = 0
    embed = discord.Embed()
    embed.title = 'Invites by '+user.name + '#' + user.discriminator
    embed.description = 'I successfully calculated the invites for '+user.name + '#' + user.discriminator
    embed.color = 123456
    try:
        if 'inviteScreen' in db[interaction.guild.id]:
            if db[interaction.guild.id]['inviteScreen']['invites']:
                embed.add_field(name = 'Invites', value = invites)
            if db[interaction.guild.id]['inviteScreen']['joins']:
                embed.add_field(name = 'Joins', value = joins)
            if db[interaction.guild.id]['inviteScreen']['leaves']:
                embed.add_field(name = 'Leaves', value = leaves)
        else:
            embed.add_field(name = 'Invites', value = invites)
    except:
        embed.add_field(name = 'Invites', value = invites)
    await interaction.response.send_message(embed=embed)

# leaderboard command - show the top 10 invites
async def leaderboard(interaction: discord.Interaction):
    """Show the top 10 invites"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if 'invites' in db[interaction.guild.id]:
        invites = db[interaction.guild.id]['invites']
    else:
        invites = {}
    if not 'joins' in db[interaction.guild.id]:
        db[interaction.guild.id]['joins'] = {}
    if not 'leaves' in db[interaction.guild.id]:
        db[interaction.guild.id]['leaves'] = {}
    embed = discord.Embed()
    embed.title = 'Leaderboard'
    embed.description = 'The invites leaderboard for '+interaction.guild.name
    embed.color = 123456
    sortedInvites = sorted(invites.items(), key=lambda x: x[1], reverse=True)
    i = 0
    for user in sortedInvites:
        if i == 10:
            break
        if not user[0] in db[interaction.guild.id]['joins']:
            db[interaction.guild.id]['joins'][user[0]] = 0
        if not user[0] in db[interaction.guild.id]['leaves']:
            db[interaction.guild.id]['leaves'][user[0]] = 0
        embed.add_field(name = str(i+1)+'. '+client.get_user(user[0]).name + '#' + client.get_user(user[0]).discriminator, value = 'Invites: '+str(user[1])+' | Joins: '+str(db[interaction.guild.id]['joins'][user[0]])+' | Leaves: '+str(db[interaction.guild.id]['leaves'][user[0]]))
        i += 1
    await interaction.response.send_message(embed=embed, ephemeral=True)




# setjoin command - set the join message/embed and channel using a modal
async def setjoin(interaction: discord.Interaction, channel:discord.TextChannel, embed:bool = False):
    """Set the join message/embed and channel"""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    db[interaction.guild.id]['joinChannel'] = channel.id
    saveDb()
    if embed:
        await interaction.response.send_modal(SetJoinModalEmbed())
    else:
        await interaction.response.send_modal(SetJoinModal())

# setwelcome command - deisgn the welcome image and channel using a modal
async def setwelcomeimage(interaction: discord.Interaction, channel:discord.TextChannel):
    """Set the welcome image and channel"""
    global db
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    db[interaction.guild.id]['welcomeChannel'] = channel.id
    saveDb()
    await interaction.response.send_modal(SetWelcomeModal())



class SetJoinModal(ui.Modal, title = 'Set the join message'):
    timeout = None
    message = ui.TextInput(label = 'Join Message', placeholder = 'Join Message {user} | {inviter} | {invites}', style = discord.TextStyle.long)
    
    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild.id in db:
            db[interaction.guild.id] = {}
        db[interaction.guild.id]['joinMessage'] = self.message.value
        db[interaction.guild.id]['joinMessageIsEmbed'] = False
        saveDb()
        await interaction.response.send_message('Set the join message to: '+self.message.value, ephemeral=True)


def drawWelcomeImage(guild, member, invites, inviter):
    if not guild.id in db:
        db[guild.id] = {}
    if not 'welcomeImage' in db[guild.id]:
        db[guild.id]['welcomeImage'] = {}
    if not 'backgroundImage' in db[guild.id]['welcomeImage']:
        db[guild.id]['welcomeImage']['backgroundImage'] = 'https://th.bing.com/th/id/OIP.7BN_fhsMDFUktI_hRMuvZgHaEo?pid=ImgDet&rs=1'
    if not 'avatarPosition' in db[guild.id]['welcomeImage']:
        db[guild.id]['welcomeImage']['avatarPosition'] = 'left'
    if not 'showInviter' in db[guild.id]['welcomeImage']:
        db[guild.id]['welcomeImage']['showInviter'] = True
    if not 'showInvites' in db[guild.id]['welcomeImage']:
        db[guild.id]['welcomeImage']['showInvites'] = True
    if not 'showMemberCount' in db[guild.id]['welcomeImage']:
        db[guild.id]['welcomeImage']['showMemberCount'] = True
    saveDb()
    background = Image.open(requests.get(db[guild.id]['welcomeImage']['backgroundImage'], stream=True).raw)
    background = background.resize((1000, 400))
    avatar = Image.open(requests.get(member.avatar.url, stream=True).raw)
    avatar = avatar.resize((200, 200))
    if db[guild.id]['welcomeImage']['avatarPosition'] == 'left':
        background.paste(avatar, (50, 50))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype('Rubik.ttf', 50)
        draw.text((300, 50), 'Welcome', (255, 255, 255), font=font)
        font = ImageFont.truetype('Rubik.ttf', 30)
        draw.text((300, 100), member.name+'#'+member.discriminator, (255, 255, 255), font=font)
        font = ImageFont.truetype('Rubik.ttf', 30)
        if db[guild.id]['welcomeImage']['showInviter']:
            draw.text((300, 150), 'Invited by '+inviter.name+'#'+inviter.discriminator, (255, 255, 255), font=font)
        if db[guild.id]['welcomeImage']['showInvites']:
            draw.text((300, 200), 'Invites: '+str(invites), (255, 255, 255), font=font)
        if db[guild.id]['welcomeImage']['showMemberCount']:
            draw.text((300, 250), 'Member Count: '+str(guild.member_count), (255, 255, 255), font=font)
        background.save('welcome'+str(member.id)+'.png')
        return 'welcome'+str(member.id)+'.png'
    else:
        background.paste(avatar, (750, 50))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype('Rubik.ttf', 50)
        draw.text((50, 50), 'Welcome', (255, 255, 255), font=font)
        font = ImageFont.truetype('Rubik.ttf', 30)
        draw.text((50, 100), member.name+'#'+member.discriminator, (255, 255, 255), font=font)
        font = ImageFont.truetype('Rubik.ttf', 30)
        if db[guild.id]['welcomeImage']['showInviter']:
            draw.text((50, 150), 'Invited by '+inviter.name+'#'+inviter.discriminator, (255, 255, 255), font=font)
        if db[guild.id]['welcomeImage']['showInvites']:
            draw.text((50, 200), 'Invites: '+str(invites), (255, 255, 255), font=font)
        if db[guild.id]['welcomeImage']['showMemberCount']:
            draw.text((50, 250), 'Member Count: '+str(guild.member_count), (255, 255, 255), font=font)
        background.save('welcome'+str(member.id)+'.png')
        return 'welcome'+str(member.id)+'.png'

class SetWelcomeModal(ui.Modal, title = 'Design the welcome image'):
    timeout = None
    background_image = ui.TextInput(label = 'Background Image', placeholder = 'Background Image (1000, 400) -- Space > Default')
    avatar_position = ui.TextInput(label = 'Avatar Position', placeholder = 'Left | Right')
    show_inviter = ui.TextInput(label = 'Show Inviter', placeholder = 'True | False')
    show_invites = ui.TextInput(label = 'Show Invites', placeholder = 'True | False')
    show_member_count = ui.TextInput(label = 'Show Member Count', placeholder = 'True | False')
    
    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild.id in db:
            db[interaction.guild.id] = {}
        db[interaction.guild.id]['welcomeImage'] = {}
        if self.background_image.value.replace(' ','') == '':
            db[interaction.guild.id]['welcomeImage']['backgroundImage'] = 'https://th.bing.com/th/id/OIP.7BN_fhsMDFUktI_hRMuvZgHaEo?pid=ImgDet&rs=1'
        else:
            db[interaction.guild.id]['welcomeImage']['backgroundImage'] = self.background_image.value
        db[interaction.guild.id]['welcomeImage']['avatarPosition'] = self.avatar_position.value
        db[interaction.guild.id]['welcomeImage']['showInviter'] = self.show_inviter.value
        db[interaction.guild.id]['welcomeImage']['showInvites'] = self.show_invites.value
        db[interaction.guild.id]['welcomeImage']['showMemberCount'] = self.show_member_count.value
        saveDb()
        await interaction.response.send_message('Set the welcome image to: '+self.background_image.value, ephemeral=True, file=discord.File(drawWelcomeImage(interaction.guild, interaction.user, 0, interaction.user)))


class SetJoinModalEmbed(ui.Modal, title = 'Set the join message'):
    timeout = None
    titlex = ui.TextInput(label = 'Title', placeholder = 'Title')
    description = ui.TextInput(label = 'Description', placeholder = 'Description {user} | {inviter} | {invites}', style = discord.TextStyle.long)
    color = ui.TextInput(label = 'Color', placeholder = '388293')
    image = ui.TextInput(label = 'Image', placeholder = 'Image')
    footer = ui.TextInput(label = 'Footer', placeholder = 'Footer')

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild.id in db:
            db[interaction.guild.id] = {}
        db[interaction.guild.id]['joinMessage'] = ''
        db[interaction.guild.id]['joinMessageIsEmbed'] = True
        db[interaction.guild.id]['joinMessageEmbed'] = {'title':self.titlex.value, 'description':self.description.value, 'color':self.color.value, 'image':self.image.value, 'footer':self.footer.value}
        saveDb()
        await interaction.response.send_message('Set the join message to: '+self.description.value, ephemeral=True)


# setleave command - set the leave message/embed and channel using a modal
async def setleave(interaction: discord.Interaction, channel:discord.TextChannel, embed:bool = False):
    """Set the leave message/embed and channel"""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    db[interaction.guild.id]['leaveChannel'] = channel.id
    saveDb()
    if embed:
        await interaction.response.send_modal(SetLeaveModalEmbed())
    else:
        await interaction.response.send_modal(SetLeaveModal())


class SetLeaveModal(ui.Modal, title = 'Set the leave message'):
    timeout = None
    message = ui.TextInput(label = 'Leave Message', placeholder = 'Leave Message {user} | {inviter} | {invites}', style = discord.TextStyle.long)
    
    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild.id in db:
            db[interaction.guild.id] = {}
        db[interaction.guild.id]['leaveMessage'] = self.message.value
        db[interaction.guild.id]['leaveMessageIsEmbed'] = False
        saveDb()
        await interaction.response.send_message('Set the leave message to: '+self.message.value, ephemeral=True)


class SetLeaveModalEmbed(ui.Modal, title = 'Set the leave message'):
    timeout = None
    titlex = ui.TextInput(label = 'Title', placeholder = 'Title')
    description = ui.TextInput(label = 'Description', placeholder = 'Description {user} | {inviter} | {invites}', style = discord.TextStyle.long)
    color = ui.TextInput(label = 'Color', placeholder = '388293')
    image = ui.TextInput(label = 'Image', placeholder = 'Image')
    footer = ui.TextInput(label = 'Footer', placeholder = 'Footer')

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild.id in db:
            db[interaction.guild.id] = {}
        db[interaction.guild.id]['leaveMessage'] = ''
        db[interaction.guild.id]['leaveMessageIsEmbed'] = True
        db[interaction.guild.id]['leaveMessageEmbed'] = {'title':self.titlex.value, 'description':self.description.value, 'color':self.color.value, 'image':self.image.value, 'footer':self.footer.value}
        saveDb()
        await interaction.response.send_message('Set the leave message to: '+self.description.value, ephemeral=True)

tempmessagebuilder = {}


@app_commands.choices(color=[app_commands.Choice(name='White', value = int('ffffff', 16)), app_commands.Choice(name='Red', value = int('ff0000', 16)), app_commands.Choice(name='Orange', value = int('ff7f00', 16)), app_commands.Choice(name='Yellow', value = int('ffff00', 16)), app_commands.Choice(name='Green', value = int('00ff00', 16)), app_commands.Choice(name='Blue', value = int('0000ff', 16)), app_commands.Choice(name='Purple', value = int('7f00ff', 16)), app_commands.Choice(name='Pink', value = int('ff00ff', 16)), app_commands.Choice(name='Black', value = int('000000', 16))])
async def messagebuilder(interaction, channel: discord.TextChannel, message:str = None, embed:bool = False, title:str = None, description:str = None, color:int = None, footer:str = None, image:str = None, thumbnail:str = None, author:str = None, author_icon:str = None, author_url:str = None, fields:int = 0, buttons:int = 0, selects:int = 0):
    """Build + Send a message"""
    # Premium only
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.id ==963125433770070096:
        # Check if the user has permission
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message('You do not have permission to use this command.')
            return
    # Check if the user is in the tempmessagebuilder
    tempmessagebuilder[interaction.user.id] = {}
    tempmessagebuilder[interaction.user.id]['message'] = message
    tempmessagebuilder[interaction.user.id]['embed'] = embed
    tempmessagebuilder[interaction.user.id]['title'] = title
    tempmessagebuilder[interaction.user.id]['description'] = description
    tempmessagebuilder[interaction.user.id]['color'] = color
    tempmessagebuilder[interaction.user.id]['footer'] = footer
    tempmessagebuilder[interaction.user.id]['image'] = image
    tempmessagebuilder[interaction.user.id]['thumbnail'] = thumbnail
    tempmessagebuilder[interaction.user.id]['author'] = author
    tempmessagebuilder[interaction.user.id]['author_icon'] = author_icon
    tempmessagebuilder[interaction.user.id]['author_url'] = author_url
    tempmessagebuilder[interaction.user.id]['numfields'] = fields
    tempmessagebuilder[interaction.user.id]['fields'] = {}
    tempmessagebuilder[interaction.user.id]['numbuttons'] = buttons
    tempmessagebuilder[interaction.user.id]['buttons'] = {}
    tempmessagebuilder[interaction.user.id]['numselects'] = selects
    tempmessagebuilder[interaction.user.id]['selects'] = {}
    tempmessagebuilder[interaction.user.id]['currentfield'] = 0
    tempmessagebuilder[interaction.user.id]['currentbutton'] = 0
    tempmessagebuilder[interaction.user.id]['currentselect'] = 0
    tempmessagebuilder[interaction.user.id]['channel'] = channel.id
    if not message and not embed:
        await interaction.response.send_message('You need to provide a message or embed.')
        return
    if embed:
        if not title and not description:
            await interaction.response.send_message('You need to provide a title or description.')
            return
    if fields > 0:
        await interaction.response.send_modal(MessageBuilderModalField())
    elif buttons > 0:
        await interaction.response.send_modal(MessageBuilderModalButton())
    elif selects > 0:
        await interaction.response.send_modal(MessageBuilderModalSelect())
    else:
        await interaction.response.send_message('Message sent!', ephemeral=True)
        if embed:
            embed = discord.Embed(title=title, description=description, color=discord.Color(color))
            if footer:
                embed.set_footer(text=footer)
            if image:
                embed.set_image(url=image)
            if thumbnail:
                embed.set_thumbnail(url=thumbnail)
            if author:
                embed.set_author(name=author, icon_url=author_icon, url=author_url)
            await channel.send(message, embed=embed)
        else:
            await channel.send(message)

class MessageBuilderModalField(ui.Modal, title = 'Message Builder'):
    timeout = None
    name = ui.TextInput(label = 'Name', placeholder = 'Name')
    value = ui.TextInput(label = 'Value', placeholder = 'Value', style = discord.TextStyle.long)
    inline = ui.TextInput(label = 'Inline', placeholder = 'True | False')

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.user.id in tempmessagebuilder:
            await interaction.response.send_message('You are not in the message builder.')
            return
        if not 'fields' in tempmessagebuilder[interaction.user.id]:
            tempmessagebuilder[interaction.user.id]['fields'] = {}
        tempmessagebuilder[interaction.user.id]['fields'][tempmessagebuilder[interaction.user.id]['currentfield']] = {'name':self.name.value, 'value':self.value.value, 'inline':self.inline.value}
        tempmessagebuilder[interaction.user.id]['currentfield'] += 1
        if tempmessagebuilder[interaction.user.id]['currentfield'] >= tempmessagebuilder[interaction.user.id]['numfields']:
            if tempmessagebuilder[interaction.user.id]['numbuttons'] > 0:
                # Replace the modal
                class ContinueButtonView(ui.View):
                    @ui.button(label = 'Continue', style = discord.ButtonStyle.primary)
                    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_modal(MessageBuilderModalButton())
                await interaction.response.send_message('Please click the button to proceed with the first button.', ephemeral=True, view=ContinueButtonView())
            elif tempmessagebuilder[interaction.user.id]['numselects'] > 0:
                # Replace the modal
                class ContinueSelectView(ui.View):
                    @ui.button(label = 'Continue', style = discord.ButtonStyle.primary)
                    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_modal(MessageBuilderModalSelect())
                await interaction.response.send_message('Please click the button to proceed with the first select.', ephemeral=True, view=ContinueSelectView())
            else:
                await interaction.response.send_message('Message sent!', ephemeral=True)
                if tempmessagebuilder[interaction.user.id]['embed']:
                    embed = discord.Embed(title=tempmessagebuilder[interaction.user.id]['title'], description=tempmessagebuilder[interaction.user.id]['description'], color=discord.Color(tempmessagebuilder[interaction.user.id]['color']))
                    if tempmessagebuilder[interaction.user.id]['footer']:
                        embed.set_footer(text=tempmessagebuilder[interaction.user.id]['footer'])
                    if tempmessagebuilder[interaction.user.id]['image']:
                        embed.set_image(url=tempmessagebuilder[interaction.user.id]['image'])
                    if tempmessagebuilder[interaction.user.id]['thumbnail']:
                        embed.set_thumbnail(url=tempmessagebuilder[interaction.user.id]['thumbnail'])
                    if tempmessagebuilder[interaction.user.id]['author']:
                        embed.set_author(name=tempmessagebuilder[interaction.user.id]['author'], icon_url=tempmessagebuilder[interaction.user.id]['author_icon'], url=tempmessagebuilder[interaction.user.id]['author_url'])
                    for field in tempmessagebuilder[interaction.user.id]['fields']:
                        embed.add_field(name=tempmessagebuilder[interaction.user.id]['fields'][field]['name'], value=tempmessagebuilder[interaction.user.id]['fields'][field]['value'], inline=tempmessagebuilder[interaction.user.id]['fields'][field]['inline'])
                    await interaction.guild.get_channel(tempmessagebuilder[interaction.user.id]['channel']).send(tempmessagebuilder[interaction.user.id]['message'], embed=embed)
                else:
                    await interaction.guild.get_channel(tempmessagebuilder[interaction.user.id]['channel']).send(tempmessagebuilder[interaction.user.id]['message'])
        else:
            # Replace the modal
            class ContinueFieldView(ui.View):
                    @ui.button(label = 'Continue', style = discord.ButtonStyle.primary)
                    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_modal(MessageBuilderModalField())
            await interaction.response.send_message('Please click the button to proceed with the next field.', ephemeral=True, view=ContinueFieldView())

class MessageBuilderModalButton(ui.Modal, title = 'Message Builder'):
    timeout = None
    label = ui.TextInput(label = 'Label', placeholder = 'Label')
    stylex = ui.TextInput(label = 'Style', placeholder = 'Primary | Secondary | Success | Danger')
    url = ui.TextInput(label = 'URL', placeholder = 'URL', style = discord.TextStyle.long)
    disabled = ui.TextInput(label = 'Disabled', placeholder = 'True | False')
    customid = ui.TextInput(label = 'Custom ID', placeholder = 'Custom ID')

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.user.id in tempmessagebuilder:
            await interaction.response.send_message('You are not in the message builder.')
            return
        if not 'buttons' in tempmessagebuilder[interaction.user.id]:
            tempmessagebuilder[interaction.user.id]['buttons'] = {}
        tempmessagebuilder[interaction.user.id]['buttons'][tempmessagebuilder[interaction.user.id]['currentbutton']] = {'label':self.label.value, 'style':self.stylex.value, 'url':self.url.value, 'disabled':self.disabled.value, 'customid':self.customid.value}
        tempmessagebuilder[interaction.user.id]['currentbutton'] += 1
        if tempmessagebuilder[interaction.user.id]['currentbutton'] >= tempmessagebuilder[interaction.user.id]['numbuttons']:
            if tempmessagebuilder[interaction.user.id]['numselects'] > 0:
                class ContinueSelectView(ui.View):
                    @ui.button(label = 'Continue', style = discord.ButtonStyle.primary)
                    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_modal(MessageBuilderModalSelect())
                await interaction.response.send_message('Please click the button to proceed with the first select.', ephemeral=True, view=ContinueSelectView())
            else:
                await interaction.response.send_message('Message sent!', ephemeral=True)
                if tempmessagebuilder[interaction.user.id]['embed']:
                    embed = discord.Embed(title=tempmessagebuilder[interaction.user.id]['title'], description=tempmessagebuilder[interaction.user.id]['description'], color=discord.Color(tempmessagebuilder[interaction.user.id]['color']))
                    if tempmessagebuilder[interaction.user.id]['footer']:
                        embed.set_footer(text=tempmessagebuilder[interaction.user.id]['footer'])
                    if tempmessagebuilder[interaction.user.id]['image']:
                        embed.set_image(url=tempmessagebuilder[interaction.user.id]['image'])
                    if tempmessagebuilder[interaction.user.id]['thumbnail']:
                        embed.set_thumbnail(url=tempmessagebuilder[interaction.user.id]['thumbnail'])
                    if tempmessagebuilder[interaction.user.id]['author']:
                        embed.set_author(name=tempmessagebuilder[interaction.user.id]['author'], icon_url=tempmessagebuilder[interaction.user.id]['author_icon'], url=tempmessagebuilder[interaction.user.id]['author_url'])
                    for field in tempmessagebuilder[interaction.user.id]['fields']:
                        embed.add_field(name=tempmessagebuilder[interaction.user.id]['fields'][field]['name'], value=tempmessagebuilder[interaction.user.id]['fields'][field]['value'], inline=tempmessagebuilder[interaction.user.id]['fields'][field]['inline'])
                    class MessageBuilderView(discord.ui.View):
                        def __init__(self, buttons):
                            super().__init__()
                            for button in buttons:
                                if buttons[button]['style'] == 'Primary':
                                    style = discord.ButtonStyle.primary
                                elif buttons[button]['style'] == 'Secondary':
                                    style = discord.ButtonStyle.secondary
                                elif buttons[button]['style'] == 'Success':
                                    style = discord.ButtonStyle.success
                                elif buttons[button]['style'] == 'Danger':
                                    style = discord.ButtonStyle.danger
                                else:
                                    style = discord.ButtonStyle.primary
                                if not '://' in buttons[button]['url']:
                                    self.add_item(discord.ui.Button(label=buttons[button]['label'], style=style, disabled=buttons[button]['disabled'], custom_id=buttons[button]['customid']))
                                else:
                                    self.add_item(discord.ui.Button(label=buttons[button]['label'], style=style, disabled=buttons[button]['disabled'], url=buttons[button]['url']))
                    await interaction.guild.get_channel(tempmessagebuilder[interaction.user.id]['channel']).send(tempmessagebuilder[interaction.user.id]['message'], embed=embed, view=MessageBuilderView(tempmessagebuilder[interaction.user.id]['buttons']))
                else:
                    class MessageBuilderView(discord.ui.View):
                        def __init__(self, buttons):
                            super().__init__()
                            for button in buttons:
                                if buttons[button]['style'] == 'Primary':
                                    style = discord.ButtonStyle.primary
                                elif buttons[button]['style'] == 'Secondary':
                                    style = discord.ButtonStyle.secondary
                                elif buttons[button]['style'] == 'Success':
                                    style = discord.ButtonStyle.success
                                elif buttons[button]['style'] == 'Danger':
                                    style = discord.ButtonStyle.danger
                                else:
                                    style = discord.ButtonStyle.primary
                                if not '://' in buttons[button]['url']:
                                    self.add_item(discord.ui.Button(label=buttons[button]['label'], style=style, disabled=buttons[button]['disabled'], custom_id=buttons[button]['customid']))
                                else:
                                    self.add_item(discord.ui.Button(label=buttons[button]['label'], style=discord.ButtonStyle.link, url=buttons[button]['url'], disabled=buttons[button]['disabled']))
                    await interaction.guild.get_channel(tempmessagebuilder[interaction.user.id]['channel']).send(tempmessagebuilder[interaction.user.id]['message'], view=MessageBuilderView(tempmessagebuilder[interaction.user.id]['buttons']))
        else:
            # Replace the modal
            class ContinueButtonView(ui.View):
                    @ui.button(label = 'Continue', style = discord.ButtonStyle.primary)
                    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_modal(MessageBuilderModalButton())
            await interaction.response.send_message('Please click the button to proceed with the next button.', view = ContinueButtonView())


class MessageBuilderModalSelect(ui.Modal, title = 'Message Builder'):
    timeout = None
    label = ui.TextInput(label = 'Label', placeholder = 'Label')
    options = ui.TextInput(label = 'Options', placeholder = 'Option 1, Option 2, Option 3', style = discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.user.id in tempmessagebuilder:
            await interaction.response.send_message('You are not in the message builder.')
            return
        if not 'selects' in tempmessagebuilder[interaction.user.id]:
            tempmessagebuilder[interaction.user.id]['selects'] = {}
        tempmessagebuilder[interaction.user.id]['selects'][tempmessagebuilder[interaction.user.id]['currentselect']] = {'label':self.label.value, 'options':self.options.value}
        tempmessagebuilder[interaction.user.id]['currentselect'] += 1
        if tempmessagebuilder[interaction.user.id]['currentselect'] >= tempmessagebuilder[interaction.user.id]['numselects']:
            await interaction.response.send_message('Message sent!', ephemeral=True)
            if tempmessagebuilder[interaction.user.id]['embed']:
                embed = discord.Embed(title=tempmessagebuilder[interaction.user.id]['title'], description=tempmessagebuilder[interaction.user.id]['description'], color=discord.Color(tempmessagebuilder[interaction.user.id]['color']))
                if tempmessagebuilder[interaction.user.id]['footer']:
                    embed.set_footer(text=tempmessagebuilder[interaction.user.id]['footer'])
                if tempmessagebuilder[interaction.user.id]['image']:
                    embed.set_image(url=tempmessagebuilder[interaction.user.id]['image'])
                if tempmessagebuilder[interaction.user.id]['thumbnail']:
                    embed.set_thumbnail(url=tempmessagebuilder[interaction.user.id]['thumbnail'])
                if tempmessagebuilder[interaction.user.id]['author']:
                    embed.set_author(name=tempmessagebuilder[interaction.user.id]['author'], icon_url=tempmessagebuilder[interaction.user.id]['author_icon'], url=tempmessagebuilder[interaction.user.id]['author_url'])
                for field in tempmessagebuilder[interaction.user.id]['fields']:
                    embed.add_field(name=tempmessagebuilder[interaction.user.id]['fields'][field]['name'], value=tempmessagebuilder[interaction.user.id]['fields'][field]['value'], inline=tempmessagebuilder[interaction.user.id]['fields'][field]['inline'])
                class MessageBuilderView(discord.ui.View):
                    def __init__(self, buttons, selects):
                        super().__init__()
                        for button in buttons:
                            if buttons[button]['style'] == 'Primary':
                                style = discord.ButtonStyle.primary
                            elif buttons[button]['style'] == 'Secondary':
                                style = discord.ButtonStyle.secondary
                            elif buttons[button]['style'] == 'Success':
                                style = discord.ButtonStyle.success
                            elif buttons[button]['style'] == 'Danger':
                                style = discord.ButtonStyle.danger
                            else:
                                style = discord.ButtonStyle.primary
                            if not '://' in buttons[button]['url']:
                                self.add_item(discord.ui.Button(label=buttons[button]['label'], style=style, disabled=buttons[button]['disabled'], custom_id=buttons[button]['customid']))
                            else:
                                self.add_item(discord.ui.Button(label=buttons[button]['label'], style=discord.ButtonStyle.link, url=buttons[button]['url'], disabled=buttons[button]['disabled'], custom_id=buttons[button]['customid']))
                        for select in selects:
                            bigselect = discord.ui.Select(placeholder=selects[select]['label'])
                            for option in selects[select]['options'].split(','):
                                bigselect.options.append(discord.SelectOption(label=option, value=option))
                            self.add_item(bigselect)
                await interaction.guild.get_channel(tempmessagebuilder[interaction.user.id]['channel']).send(tempmessagebuilder[interaction.user.id]['message'], embed=embed, view=MessageBuilderView(tempmessagebuilder[interaction.user.id]['buttons'], tempmessagebuilder[interaction.user.id]['selects']))
            else:
                class MessageBuilderView(discord.ui.View):
                    def __init__(self, buttons, selects):
                        super().__init__()
                        for button in buttons:
                            if buttons[button]['style'] == 'Primary':
                                style = discord.ButtonStyle.primary
                            elif buttons[button]['style'] == 'Secondary':
                                style = discord.ButtonStyle.secondary
                            elif buttons[button]['style'] == 'Success':
                                style = discord.ButtonStyle.success
                            elif buttons[button]['style'] == 'Danger':
                                style = discord.ButtonStyle.danger
                            else:
                                style = discord.ButtonStyle.primary
                            if not '://' in buttons[button]['url']:
                                self.add_item(discord.ui.Button(label=buttons[button]['label'], style=style, disabled=buttons[button]['disabled'], custom_id=buttons[button]['customid']))
                            else:
                                self.add_item(discord.ui.Button(label=buttons[button]['label'], style=discord.ButtonStyle.link, url=buttons[button]['url'], disabled=buttons[button]['disabled'], custom_id=buttons[button]['customid']))
                        for select in selects:
                            bigselect = discord.ui.Select(placeholder=selects[select]['label'])
                            for option in selects[select]['options'].split(','):
                                bigselect.options.append(discord.SelectOption(label=option, value=option))
                            self.add_item(bigselect)
                await interaction.guild.get_channel(tempmessagebuilder[interaction.user.id]['channel']).send(tempmessagebuilder[interaction.user.id]['message'], view=MessageBuilderView(tempmessagebuilder[interaction.user.id]['buttons'], tempmessagebuilder[interaction.user.id]['selects']))
        else:
            # Replace the modal
            class ContinueSelectView(ui.View):
                    @ui.button(label = 'Continue', style = discord.ButtonStyle.primary)
                    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.response.send_modal(MessageBuilderModalSelect())
            await interaction.response.send_message('Please click the button to proceed with the next select.', ephemeral=True, view=ContinueSelectView())


# addinviterole command - add a role to the list of roles to give to the inviter
async def addinviterole(interaction: discord.Interaction, invites:int, role:discord.Role, reverse:bool = False):
    """Add a role to the list of roles to give to the inviter"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'inviteroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['inviteroles'] = {}
    if not role.id in db[interaction.guild.id]['inviteroles']:
        db[interaction.guild.id]['inviteroles'][role.id] = {}
    db[interaction.guild.id]['inviteroles'][role.id][invites] = {'reverse':reverse}
    saveDb()
    await interaction.response.send_message('Added inviter role: '+role.name+' with '+str(invites)+' invites', ephemeral=True)


# Temp voice channels with 'temp' in name
@client.event
async def on_voice_state_update(member, before, after):
    global db
    if not member.guild.id in db:
        db[member.guild.id] = {}
    if not 'tempchannels' in db[member.guild.id]:
        db[member.guild.id]['tempchannels'] = {}
    # If limit member count is 1, it's a temp channel creator
    if after.channel and len(after.channel.members) == 1 and after.channel.user_limit == 1:
        if len(after.channel.members) == 1:
            if after.channel.category:
                channel = await after.channel.category.create_voice_channel('temp-'+member.name, user_limit=2)
            else:
                channel = await member.guild.create_voice_channel('temp-'+member.name, user_limit=2)
            await member.move_to(channel)
            db[member.guild.id]['tempchannels'][channel.id] = {'owner':member.id}
            db[member.guild.id]['tempchannels'][channel.id]['name'] = channel.name
            db[member.guild.id]['tempchannels'][channel.id]['banned'] = []
            db[member.guild.id]['tempchannels'][channel.id]['private'] = False
            db[member.guild.id]['tempchannels'][channel.id]['allowed'] = []

            embed = discord.Embed(title='Temp channel', description='Manage your temp channel')
            embed.add_field(name='Private', value='No', inline=True)
            embed.add_field(name='Banned', value='None', inline=True)
            embed.add_field(name='Owner', value=member.mention, inline=True)
            embed.add_field(name='Name', value=channel.name, inline=True)
            embed.add_field(name='Limit', value='2', inline=True)
            # Send embed with buttons to manage temp channel
            class TempChannelView(ui.View):
                timeout = None
                @ui.button(label = 'Private', style = discord.ButtonStyle.primary)
                async def private_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                        db[member.guild.id]['tempchannels'][channel.id]['private'] = not db[member.guild.id]['tempchannels'][channel.id]['private']
                        if db[member.guild.id]['tempchannels'][channel.id]['private']:
                            button.label = 'Public'
                            button.style = discord.ButtonStyle.secondary
                        else:
                            button.label = 'Private'
                            button.style = discord.ButtonStyle.primary
                        embed.set_field_at(0, name='Private', value='Yes' if db[member.guild.id]['tempchannels'][channel.id]['private'] else 'No')
                        await interaction.response.edit_message(embed=embed, view=TempChannelView())
                        saveDb()
                @ui.button(label = 'Set Limit', style = discord.ButtonStyle.primary)
                async def limit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                        # Select a limit from Select
                        class LimitSelectView(ui.View):
                            timeout = None
                            @ui.select(options = [discord.SelectOption(label = 'New: '+str(limit), value = str(limit)) for limit in range(2, 12)]+[discord.SelectOption(label = 'No Limit', value = '0')])
                            async def limit_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                                if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                                    db[member.guild.id]['tempchannels'][channel.id]['limit'] = int(select.values[0])
                                    embed.set_field_at(4, name='Limit', value=select.values[0], inline=True)
    	                            # Edit Channel Limit
                                    await channel.edit(user_limit=db[member.guild.id]['tempchannels'][channel.id]['limit'])
                                    await interaction.response.edit_message(embed=embed, view=TempChannelView())
                        await interaction.response.send_message('Select a limit:', view=LimitSelectView())
                        saveDb()
                @ui.button(label = 'Set Name', style = discord.ButtonStyle.primary)
                async def name_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                        # Select a name from Select
                        class NameSelectModal(ui.Modal, title = 'Select a name'):
                            timeout = None
                            name = ui.TextInput(label= 'Name', placeholder = 'Name')
                            async def on_submit(self, interaction: discord.Interaction):
                                if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                                    db[member.guild.id]['tempchannels'][channel.id]['name'] = self.name.value
                                    embed.set_field_at(3, name='Name', value=self.name.value, inline=True)
                                    # Edit Channel Name
                                    await channel.edit(name=db[member.guild.id]['tempchannels'][channel.id]['name'])
                                    await interaction.response.edit_message(embed=embed, view=TempChannelView())
                        await interaction.response.send_modal(NameSelectModal())
                        saveDb()
                @ui.button(label = 'Ban', style = discord.ButtonStyle.danger)
                async def ban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                        # Select a member to ban from Select
                        class MemberSelectView(ui.View):
                            timeout = None
                            @ui.select(options = [discord.SelectOption(label = member.name, value = member.id) for member in channel.members if member.id not in db[member.guild.id]['tempchannels'][channel.id]['banned']])
                            async def member_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                                if interaction.user.id == db[interaction.guild.id]['tempchannels'][channel.id]['owner']:
                                    if int(select.values[0]) != interaction.user.id:
                                        db[interaction.guild.id]['tempchannels'][channel.id]['banned'].append(int(select.values[0]))
                                        saveDb()
                                        embed.set_field_at(1, name='Banned', value=', '.join(['<@'+str(member)+'>' for member in db[interaction.guild.id]['tempchannels'][channel.id]['banned']]))
                                        await interaction.response.edit_message(embed=embed, view=TempChannelView())
                                        await interaction.followup.send('Banned '+str(select.values[0]))
                                        for member in channel.members:
                                            if member.id in db[interaction.guild.id]['tempchannels'][channel.id]['banned']:
                                                await member.move_to(None)
                                    else:
                                        await interaction.response.send_message('You can\'t ban yourself')
                        await interaction.response.send_message('Select a member to ban', view=MemberSelectView())
                        saveDb()
                @ui.button(label = 'Unban', style = discord.ButtonStyle.success)
                async def allow_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                        members = await interaction.guild.chunk()
                        # Select a member to unban from Select
                        class MemberSelectView(ui.View):
                            timeout = None
                            @ui.select(options = [discord.SelectOption(label = member.name, value = member.id) for member in members if member.id in db[member.guild.id]['tempchannels'][channel.id]['banned']])
                            async def member_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                                if interaction.user.id == db[interaction.guild.id]['tempchannels'][channel.id]['owner']:
                                    db[interaction.guild.id]['tempchannels'][channel.id]['banned'].remove(int(select.values[0]))
                                    saveDb()
                                    if ', '.join(['<@'+str(member)+'>' for member in db[interaction.guild.id]['tempchannels'][channel.id]['banned']]) and ', '.join(['<@'+str(member)+'>' for member in db[interaction.guild.id]['tempchannels'][channel.id]['banned']]) != '':
                                        embed.set_field_at(1, name='Banned', value=', '.join(['<@'+str(member)+'>' for member in db[interaction.guild.id]['tempchannels'][channel.id]['banned']]), inline=True)
                                    else:
                                        embed.set_field_at(1, name='Banned', value='None', inline=True)
                                    await interaction.response.edit_message(embed=embed, view=TempChannelView())
                                    await interaction.followup.send('Unbanned '+str(select.values[0]))
                                    for member in channel.members:
                                        if member.id in db[interaction.guild.id]['tempchannels'][channel.id]['banned']:
                                            await member.move_to(None)
                        await interaction.response.send_message('Select a member to unban', view=MemberSelectView())
                        saveDb()
                @ui.button(label = 'Delete', style = discord.ButtonStyle.danger)
                async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                        # Confirm
                        class ConfirmView(ui.View):
                            timeout = None
                            @ui.button(label = 'Yes', style = discord.ButtonStyle.danger)
                            async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                await channel.delete()
                                del db[member.guild.id]['tempchannels'][channel.id]
                                saveDb()
                                await interaction.response.send_message('Deleted', view=TempChannelView())
                            @ui.button(label = 'No', style = discord.ButtonStyle.secondary)
                            async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                await interaction.response.send_message('Cancelled', view=TempChannelView())
                        await interaction.response.send_message('Are you sure you want to delete this channel?', view=ConfirmView())
                        del db[member.guild.id]['tempchannels'][channel.id]
                        saveDb()
                @ui.button(label = 'Change Owner', style = discord.ButtonStyle.secondary)
                async def change_owner_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                        # Select a member to change owner to from Select
                        class MemberSelectView(ui.View):
                            timeout = None
                            @ui.select(options = [discord.SelectOption(label = member.name, value = member.id) for member in channel.members if member.id != db[member.guild.id]['tempchannels'][channel.id]['owner']])
                            async def member_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                                if interaction.user.id == db[member.guild.id]['tempchannels'][channel.id]['owner']:
                                    db[member.guild.id]['tempchannels'][channel.id]['owner'] = int(select.values[0])
                                    embed.set_field_at(2, name='Owner', value=channel.guild.get_member(int(select.values[0])).mention)
                                    await interaction.response.edit_message(embed=embed, view=TempChannelView())
                                    await interaction.followup.send('Changed owner to <@'+select.values[0]+'>')
                        await interaction.response.send_message('Select a member to change owner to', view=MemberSelectView())
                        saveDb()
            await channel.send(embed=embed, view=TempChannelView())
            saveDb()
    else:
        if after.channel:
            if after.channel.id in db[member.guild.id]['tempchannels']:
                if member.id in db[member.guild.id]['tempchannels'][after.channel.id]['banned']:
                    await member.move_to(None)
                if db[member.guild.id]['tempchannels'][after.channel.id]['private']:
                    if not member.id in db[member.guild.id]['tempchannels'][after.channel.id]['allowed']:
                        await member.move_to(None)
        if before.channel.id in db[member.guild.id]['tempchannels']:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                del db[member.guild.id]['tempchannels'][before.channel.id]
                saveDb()
            else:
                if member.id in db[member.guild.id]['tempchannels'][before.channel.id]['banned']:
                    await member.move_to(None)
                if db[member.guild.id]['tempchannels'][before.channel.id]['private']:
                    if not member.id in db[member.guild.id]['tempchannels'][before.channel.id]['allowed']:
                        await member.move_to(None)





# removeinviterole command - remove a role from the list of roles to give to the inviter
async def removeinviterole(interaction: discord.Interaction, invites:int, role:discord.Role):
    """Remove a role from the list of roles to give to the inviter"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'inviteroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['inviteroles'] = {}
    if role.id in db[interaction.guild.id]['inviteroles']:
        if not invites in db[interaction.guild.id]['inviteroles'][role.id]:
            await interaction.response.send_message('Role not found', ephemeral=True)
            return
        del db[interaction.guild.id]['inviteroles'][role.id][invites]
        saveDb()
        await interaction.response.send_message('Removed inviter role: '+role.name, ephemeral=True)
    else:
        await interaction.response.send_message('Role not found', ephemeral=True)


# inviteroles command - list the roles to give or remove from the inviter
async def inviteroles(interaction: discord.Interaction):
    """List the roles to give or remove from the inviter"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'inviteroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['inviteroles'] = {}
    if len(db[interaction.guild.id]['inviteroles']) == 0:
        await interaction.response.send_message('No invite-roles found', ephemeral=True)
    else:
        embed = discord.Embed(title='Invite-roles', color=0x00ff00)
        for role in db[interaction.guild.id]['inviteroles']:
            currentrolemessage=''
            for invites in db[interaction.guild.id]['inviteroles'][role]:
                if db[interaction.guild.id]['inviteroles'][role][invites]['reverse']:
                    for rolx in interaction.guild.roles:
                        if rolx.id == role:
                            currentrolemessage += 'Remove '+rolx.name+' with '+str(invites)+' invites\n'
                else:
                    for rolx in interaction.guild.roles:
                        if rolx.id == role:
                            currentrolemessage += 'Give '+rolx.name+' with '+str(invites)+' invites\n'
            for rolx in interaction.guild.roles:
                if rolx.id == role:
                    embed.add_field(name=rolx.name, value=currentrolemessage, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def qa(interaction: discord.Interaction, question:str):
    """Reply to a question with an answer"""
    await interaction.response.defer(ephemeral=True)
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    request = await AsyncClient.get('https://api.udit.tk/api/chatbot?message='+question+'&name=SplitticHost Bot&user='+str(interaction.user.id))
    await interaction.followup.send(request.json()['message'])

def random_string():
    N = random.randint(5, 10)
    s = string.ascii_letters + string.digits
    return ''.join(random.choices(s, k=N))


# Setcaptcha command
async def setcaptcha(interaction: discord.Interaction, enabled:bool = True):
    """Enable or disable captcha"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command.')
        return
    if enabled:
        class VerifyModal(ui.Modal, title = "Enter the text on the captcha"):
                captcha_text = ui.TextInput(label = 'Captcha', placeholder="Enter the rules", style = discord.TextStyle.long)
                async def on_submit(self, interaction:discord.Interaction):
                    db[interaction.guild.id]['captcha_msg'] = self.captcha_text.value
                    await interaction.response.send_message("Successfully setted rules.\nCaptcha enabled", ephemeral=True)
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    db[interaction.guild.id]['captcha'] = enabled
    saveDb()
    if enabled:
        await interaction.response.send_modal(VerifyModal())
    else:
        await interaction.response.send_message('Captcha is now disabled in this server.', ephemeral=True)

# Multiple Ban
@client.event
async def on_member_ban(guild, user):
    if guild.id not in allowed_bots:
        allowed_bots[guild.id] = []
    # Check if member was banned by a bot
    audit = guild.audit_logs(limit=1, action=discord.AuditLogAction.ban)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[guild.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Check if member was banned by the same bot
            if audits[0].user.id in allowed_bots[guild.id]:
                return
            # Check if member was banned by the same bot multiple times
            audit = guild.audit_logs(limit=2, action=discord.AuditLogAction.ban)
            # Remove first audit log
            audits2 = []
            async for i in audit:
                audits2.append(i)
            audits2.pop(0)
            # Check if member was banned by the same bot multiple times
            if audits2[0].user.id == audits[0].user.id:
                # Mute user
                endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(guild.id, audits[0].user.id)
                headers = {
                    'Authorization': 'Bot ' + TOKEN,
                }
                data = {
                    'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
                }
                req = await AsyncClient.patch(endpoint, headers=headers, json=data)
                if req.status_code != 200:
                    member = guild.get_member(audits[0].user.id)
                    await member.kick(reason="Anti-nuke")
    except:
        pass

# Multiple Unban
@client.event
async def on_member_unban(server, user):
    if server.id not in allowed_bots:
        allowed_bots[server.id] = []
    # Check if member was unbanned by a bot
    audit = server.audit_logs(limit=1, action=discord.AuditLogAction.unban)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[server.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Check if member was unbanned by the same bot
            if audits[0].user.id in allowed_bots[server.id]:
                return
            # Check if member was unbanned by the same bot multiple times
            audit = server.audit_logs(limit=2, action=discord.AuditLogAction.unban)
            # Remove first audit log
            audits2 = []
            async for i in audit:
                audits2.append(i)
            audits2.pop(0)
            # Check if member was unbanned by the same bot multiple times
            if audits2[0].user.id == audits[0].user.id:
                # Mute user
                endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(server.id, audits[0].user.id)
                headers = {
                    'Authorization': 'Bot ' + TOKEN,
                }
                data = {
                    'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
                }
                req = await AsyncClient.patch(endpoint, headers=headers, json=data)
                if req.status_code != 200:
                    member = server.get_member(audits[0].user.id)
                    await member.kick(reason="Anti-nuke")
    except:
        pass

# Join/Leave event - when a user joins/leaves the server
@client.event
async def on_member_join(member: discord.Member):
    if not member.guild.id in db:
        db[member.guild.id] = {}
    if 'autoping' in db[member.guild.id]:
        for channelx in db[member.guild.id]['autoping']:
            channel = client.get_channel(channelx)
            await channel.send(f'{member.mention}', delete_after=0.1)
    # Check account age
    timestamp = member.created_at
    timestampnow = datetime.datetime.timestamp(datetime.datetime.now())
    seven_days = 604800
    if timestampnow - timestamp.timestamp() < seven_days:
        # Mute user
        endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(member.guild.id, member.id)
        headers = {
            'Authorization': 'Bot ' + TOKEN,
        }
        data = {
            'communication_disabled_until': timestampnow + seven_days
        }
        await AsyncClient.patch(endpoint, headers=headers, json=data)
        # Send message to user
        await member.send(f"Your account is too new to join this server.")
        await member.kick()
    currentinvites = oldinvites[member.guild.id]
    try:
        currentinvites = await member.guild.invites()
    except:
        pass
    if not member.guild.id in db:
        db[member.guild.id] = {}
    if not 'captcha' in db[member.guild.id]:
        db[member.guild.id]['captcha'] = False
    if db[member.guild.id]['captcha']:
        getit = lambda : (random.randrange(5, 85),random.randrange(5, 55))
        colors = ["black", "red", "blue", "green", (64, 107, 76), (0, 87, 128), (0, 3, 82)]
        fill_color = [(64, 107, 76),(0, 87, 128),(0, 3, 82),(191, 0, 255),(72, 189, 0),(189, 107, 0),(189, 41, 0)]
        img = Image.new('RGB', (90, 60), color="white")
        draw = ImageDraw.Draw(img)
        captcha_str = random_string()
        text_colors = random.choice(colors)
        for i in range(5,random.randrange(6, 10)):
            draw.line((getit(), getit()), fill=random.choice(fill_color), width=random.randrange(1,3))
        for i in range(10,random.randrange(11, 20)):
            draw.point((getit(), getit(), getit(), getit(), getit(), getit(), getit(), getit(), getit(), getit()), fill=random.choice(colors))
        draw.text((19,20), captcha_str, fill="white")
        draw.text((21,20), captcha_str, fill="white")
        draw.text((20,19), captcha_str, fill="white")
        draw.text((20,21), captcha_str, fill="white")
        draw.text((20,20), captcha_str, fill=text_colors)
        img = img.resize((900,600))
        img.save("captcha_img/"+ captcha_str +".png")
        embed = discord.Embed(title="Verify yourself", description="Please solve the following captcha:", color=0x00ff00)
        embed.set_footer(text="Captcha expires in 10 minutes")
        class VerifyModal(ui.Modal, title = "Enter the text on the captcha"):
            entered_text = ui.TextInput(label = 'Captcha', placeholder="Enter the text on the captcha")
            async def on_submit(self, interaction:discord.Interaction):
                if self.entered_text.value.lower() == captcha_str.lower():
                    await interaction.response.send_message("You have been verified.", ephemeral=True)
                    await continueMemberJoin(member,currentinvites)
                    await msg.delete()
                else:
                    for x in range(len(member.guild.channels)):
                        try:
                            serverinvite = await member.guild.channels[x].create_invite(max_age=600, max_uses=1)
                            break
                        except:
                            pass
                    await interaction.response.send_message("You did not solve the captcha right.\nRejoin the server to try again.\n"+str(serverinvite), ephemeral=True)
                    await member.kick()
                    await msg.delete()
        class VerifyView(ui.View):
            @ui.button(label="Solve")
            async def solve(self, interaction:discord.Interaction, button):
                await interaction.response.send_modal(VerifyModal())
        if 'captcha_msg' in db[member.guild.id]:
            msg = await member.send(content = '__Rules__\n```' + db[member.guild.id]['captcha_msg']+'```',file=discord.File("captcha_img/"+ captcha_str +".png"),embed=embed, view = VerifyView())
        else:
            msg = await member.send(file=discord.File("captcha_img/"+ captcha_str +".png"),embed=embed, view = VerifyView())
        await asyncio.sleep(600)
        await msg.delete()
    else:
        await continueMemberJoin(member,currentinvites)

async def continueMemberJoin(member,currentinvites):
    if 'autoroles' in db[member.guild.id]:
        for role in db[member.guild.id]['autoroles']:
            try:
                await member.add_roles(member.guild.get_role(role))
            except Exception as es:
                print(es)
    # Get the inviter of the joined user and increase their invites
    try:
        for inv in range(len(currentinvites)):
            if currentinvites[inv].uses > oldinvites[member.guild.id][inv].uses:
                theinviter = member.guild.get_member(currentinvites[inv].inviter.id)
        try:
            oldinvites[member.guild.id] = currentinvites
            if theinviter.id == member.id:
                if 'joinChannel' in db[member.guild.id]:
                    for channel in member.guild.channels:
                        if channel.id == db[member.guild.id]['joinChannel']:
                            await channel.send(member.mention+' tried to invite themselves!\nNo invites for you!')
                            return
            if not 'invites' in db[member.guild.id]:
                db[member.guild.id]['invites'] = {}
            if not theinviter.id in db[member.guild.id]['invites']:
                db[member.guild.id]['invites'][theinviter.id] = 0
            db[member.guild.id]['invites'][theinviter.id] += 1
            if not 'joins' in db[member.guild.id]:
                db[member.guild.id]['joins'] = {}
            if not theinviter.id in db[member.guild.id]['joins']:
                db[member.guild.id]['joins'][theinviter.id] = 0
            db[member.guild.id]['joins'][theinviter.id] += 1
            if not 'invitedby' in db[member.guild.id]:
                db[member.guild.id]['invitedby'] = {}
            db[member.guild.id]['invitedby'][member.id] = theinviter.id
            saveDb()
            try:
                if 'joinChannel' in db[member.guild.id] and db[member.guild.id]['joinChannel'] != '':
                    if 'joinMessage' in db[member.guild.id] and 'joinMessageIsEmbed' in db[member.guild.id]:
                        if db[member.guild.id]['joinMessageIsEmbed']:
                            embed = discord.Embed(title=db[member.guild.id]['joinMessageEmbed']['title'], description=db[member.guild.id]['joinMessageEmbed']['description'].format(user=member, inviter=theinviter, invites=db[member.guild.id]['invites'][theinviter.id]), color=int(db[member.guild.id]['joinMessageEmbed']['color']))
                            embed.set_author(name=member.name, icon_url=member.avatar)
                            embed.set_thumbnail(url=member.avatar)
                            embed.set_footer(text=db[member.guild.id]['joinMessageEmbed']['footer'].format(user=member, inviter=theinviter, invites=db[member.guild.id]['invites'][theinviter.id]))
                            embed.set_image(url=db[member.guild.id]['joinMessageEmbed']['image'])
                            await member.guild.get_channel(db[member.guild.id]['joinChannel']).send(embed=embed)
                        else:
                            await member.guild.get_channel(db[member.guild.id]['joinChannel']).send(db[member.guild.id]['joinMessage'].format(user=member, inviter=theinviter, invites=db[member.guild.id]['invites'][theinviter.id]))
                    else:
                        await member.guild.get_channel(db[member.guild.id]['joinChannel']).send(member.mention+' has joined the server!')
            except Exception as es:
                print(es)
            if 'inviteroles' in db[member.guild.id]:
                for role in db[member.guild.id]['inviteroles']:
                    for invites in db[member.guild.id]['inviteroles'][role]:
                        if db[member.guild.id]['inviteroles'][role][invites]['reverse']:
                            if db[member.guild.id]['invites'][theinviter.id] >= invites:
                                await theinviter.remove_roles(member.guild.get_role(role))
                        else:
                            if db[member.guild.id]['invites'][theinviter.id] >= invites:
                                await theinviter.add_roles(member.guild.get_role(role))
        except:
            if 'joinChannel' in db[member.guild.id] and db[member.guild.id]['joinChannel'] != '':
                await member.guild.get_channel(db[member.guild.id]['joinChannel']).send(member.mention+' has joined the server!')
    except:
        #try:
            if 'joinChannel' in db[member.guild.id] and db[member.guild.id]['joinChannel'] != '':
                # If the user joined using a vanity URL, make a button to a modal to enter the inviter's ID
                class InviterId(ui.Modal, title='Who invited you?'):
                    inviterinfo = ui.TextInput(label = 'Inviter Name', placeholder='Enter the ID or Name#1234 of the inviter of this user.')

                    async def on_submit(self, interaction:discord.Interaction):
                        if self.inviterinfo.value.isdigit():
                            inviter = interaction.guild.get_member(int(self.inviterinfo.value))
                            if inviter is None:
                                raise ValueError('Invalid ID')
                        else:
                            # Get ID from user by name
                            inviter = interaction.guild.get_member_named(self.inviterinfo.value)
                            if inviter is None:
                                raise ValueError('Invalid Name')
                        if not 'invites' in db[member.guild.id]:
                            db[member.guild.id]['invites'] = {}
                        if not inviter.id in db[member.guild.id]['invites']:
                            db[member.guild.id]['invites'][inviter.id] = 0
                        db[member.guild.id]['invites'][inviter.id] += 1
                        if not 'joins' in db[member.guild.id]:
                            db[member.guild.id]['joins'] = {}
                        if not member.id in db[member.guild.id]['joins']:
                            db[member.guild.id]['joins'][member.id] = 0
                        db[member.guild.id]['joins'][member.id] += 1
                        if not 'invitedby' in db[member.guild.id]:
                            db[member.guild.id]['invitedby'] = {}
                        db[member.guild.id]['invitedby'][member.id] = inviter.id
                        saveDb()
                        try:
                            if 'joinChannel' in db[member.guild.id] and db[member.guild.id]['joinChannel'] != '':
                                if 'joinMessage' in db[member.guild.id] and 'joinMessageIsEmbed' in db[member.guild.id]:
                                    if db[member.guild.id]['joinMessageIsEmbed']:
                                        embed = discord.Embed(title=db[member.guild.id]['joinMessageEmbed']['title'], description=db[member.guild.id]['joinMessageEmbed']['description'].format(user=member, inviter=inviter, invites=db[member.guild.id]['invites'][inviter.id]), color=int(db[member.guild.id]['joinMessageEmbed']['color']))
                                        embed.set_author(name=member.name, icon_url=member.avatar)
                                        embed.set_thumbnail(url=member.avatar)
                                        embed.set_footer(text=db[member.guild.id]['joinMessageEmbed']['footer'].format(user=member, inviter=inviter, invites=db[member.guild.id]['invites'][inviter.id]))
                                        embed.set_image(url=db[member.guild.id]['joinMessageEmbed']['image'])
                                        await member.guild.get_channel(db[member.guild.id]['joinChannel']).send(embed=embed)
                                    else:
                                        await member.guild.get_channel(db[member.guild.id]['joinChannel']).send(db[member.guild.id]['joinMessage'].format(user=member, inviter=inviter, invites=db[member.guild.id]['invites'][inviter.id]))
                                else:
                                    await member.guild.get_channel(db[member.guild.id]['joinChannel']).send(member.mention+' has joined the server!')
                            await msg.delete()
                        except:
                            pass
                        if 'inviteroles' in db[member.guild.id]:
                            for role in db[member.guild.id]['inviteroles']:
                                for invites in db[member.guild.id]['inviteroles'][role]:
                                    if db[member.guild.id]['inviteroles'][role][invites]['reverse']:
                                        if db[member.guild.id]['invites'][inviter.id] >= invites:
                                            await theinviter.remove_roles(member.guild.get_role(role))
                                    else:
                                        if db[member.guild.id]['invites'][inviter.id] >= invites:
                                            await theinviter.add_roles(member.guild.get_role(role))
                class View(ui.View):
                    timeout=None
                    def __init__(self):
                        super().__init__()
                    @discord.ui.button(label='Set Inviter')
                    async def setInviter(self, interaction:discord.Interaction, button: discord.ui.Button):
                        if interaction.user.id == member.id:
                            await interaction.response.send_modal(InviterId())
                            # Disable the button
                            button.enabled = False
                msg = await member.guild.get_channel(db[member.guild.id]['joinChannel']).send(member.mention+' has joined the server using a vanity invite!', embed=discord.Embed(title='Set Inviter', description='Click the button below to set the inviter of this user.', color=0x00ff00), view=View())
    # theinviter or inviter
    if is_premium(member.guild.id):
        try:
            # drawWelcomeImage(guild, user, invites, inviter)
            image = drawWelcomeImage(member.guild, member, db[member.guild.id]['invites'][inviter.id], inviter)
            # db[interaction.guild.id]['welcomeChannel']
            await member.guild.get_channel(db[member.guild.id]['welcomeChannel']).send(file=discord.File(image, 'welcome.png'))
        except:
            # drawWelcomeImage(guild, user, invites, inviter)
            image = drawWelcomeImage(member.guild, member, db[member.guild.id]['invites'][theinviter.id], theinviter)
            # db[interaction.guild.id]['welcomeChannel']
            await member.guild.get_channel(db[member.guild.id]['welcomeChannel']).send(file=discord.File(image, 'welcome.png'))

                    



# Join/Leave event - when a user joins/leaves the server
@client.event
async def on_member_remove(member: discord.Member):
    if member.guild.id not in allowed_bots:
        allowed_bots[member.guild.id] = []
    # Check if member was kicked by a bot
    audit = member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[member.guild.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Check if member was kicked by the same bot
            if audits[0].user.id in allowed_bots[member.guild.id]:
                return
            # Check if member was kicked by the same bot multiple times
            audit = member.guild.audit_logs(limit=2, action=discord.AuditLogAction.kick)
            # Remove first audit log
            audits2 = []
            async for i in audit:
                audits2.append(i)
            audits2.pop(0)
            # Check if member was kicked by the same bot multiple times
            if audits2[0].user.id == audits[0].user.id:
                # Mute user
                endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(member.guild.id, audits[0].user.id)
                headers = {
                    'Authorization': 'Bot ' + TOKEN,
                }
                data = {
                    'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
                }
                req = await AsyncClient.patch(endpoint, headers=headers, json=data)
                if req.status_code != 200:
                    member = member.guild.get_member(audits[0].user.id)
                    await member.kick(reason="Anti-nuke")
    except:
        pass
    if not member.guild.id in db:
        db[member.guild.id] = {}
    if 'invitedby' in db[member.guild.id]:
        if member.id in db[member.guild.id]['invitedby']:
            theinviter = member.guild.get_member(db[member.guild.id]['invitedby'][member.id])
            if not 'invites' in db[member.guild.id]:
                db[member.guild.id]['invites'] = {}
            if not theinviter.id in db[member.guild.id]['invites']:
                db[member.guild.id]['invites'][theinviter.id] = 0
            db[member.guild.id]['invites'][theinviter.id] -= 1
            if not 'leaves' in db[member.guild.id]:
                db[member.guild.id]['leaves'] = {}
            if not theinviter.id in db[member.guild.id]['leaves']:
                db[member.guild.id]['leaves'][theinviter.id] = 0
            db[member.guild.id]['leaves'][theinviter.id] += 1
            saveDb()
            try:
                if 'leaveChannel' in db[member.guild.id] and db[member.guild.id]['leaveChannel'] != '':
                    if 'leaveMessage' in db[member.guild.id] and 'leaveMessageIsEmbed' in db[member.guild.id]:
                        if db[member.guild.id]['leaveMessageIsEmbed']:
                            embed = discord.Embed(title=db[member.guild.id]['leaveMessageEmbed']['title'], description=db[member.guild.id]['leaveMessageEmbed']['description'].format(user=member, inviter=theinviter, invites=db[member.guild.id]['invites'][theinviter.id]), color=db[member.guild.id]['leaveMessageEmbed']['color'])
                            await member.guild.get_channel(db[member.guild.id]['leaveChannel']).send(embed=embed)
                            embed.set_author(name=member.name, icon_url=member.avatar)
                            await member.guild.get_channel(db[member.guild.id]['leaveChannel']).send(embed=embed)
                        else:
                            await member.guild.get_channel(db[member.guild.id]['leaveChannel']).send(db[member.guild.id]['leaveMessage'].format(user=member, inviter=theinviter, invites=db[member.guild.id]['invites'][theinviter.id]))
                    else:
                        await member.guild.get_channel(db[member.guild.id]['leaveChannel']).send(member.mention+' has left the server!')
            except:
                pass
            if 'inviteroles' in db[member.guild.id]:
                for role in db[member.guild.id]['inviteroles']:
                    for invites in db[member.guild.id]['inviteroles'][role]:
                        if db[member.guild.id]['inviteroles'][role][invites]['reverse']:
                            if db[member.guild.id]['invites'][theinviter.id] >= invites:
                                try:
                                    await theinviter.remove_roles(member.guild.get_role(role))
                                except Exception as es:
                                    print(es)
                        else:
                            if db[member.guild.id]['invites'][theinviter.id] >= invites:
                                try:
                                    await theinviter.add_roles(member.guild.get_role(role))
                                except Exception as es:
                                    print(es)
    else:
        if 'leaveChannel' in db[member.guild.id] and db[member.guild.id]['leaveChannel'] != '':
            await member.guild.get_channel(db[member.guild.id]['leaveChannel']).send(member.mention+' has left the server!')


# On invite create/delete - when a user creates/deletes an invite
@client.event
async def on_invite_create(invite: discord.Invite):
    oldinvites[invite.guild.id] = await invite.guild.invites()


@client.event
async def on_invite_delete(invite: discord.Invite):
    oldinvites[invite.guild.id] = await invite.guild.invites()


# On guild join - when the bot joins a server
@client.event
async def on_guild_join(guild: discord.Guild):
    oldinvites[guild.id] = await guild.invites()

# Guild Update
@client.event
async def on_guild_update(before, after):
    if before.id not in allowed_bots:
        allowed_bots[before.id] = []
    # Check if guild was updated by a bot
    audit = before.audit_logs(limit=1, action=discord.AuditLogAction.guild_update)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[before.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Undo guild update
            await after.edit(name=before.name, region=before.region, icon=before.icon, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, verification_level=before.verification_level, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, rules_channel=before.rules_channel, public_updates_channel=before.public_updates_channel, preferred_locale=before.preferred_locale, reason='Anti-nuke')
            # Mute user
            endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(before.id, audits[0].user.id)
            headers = {
                'Authorization': 'Bot ' + TOKEN,
            }
            data = {
                'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
            }
            req = await AsyncClient.patch(endpoint, headers=headers, json=data)
            if req.status_code != 200:
                member = before.get_member(audits[0].user.id)
                await member.kick(reason="Anti-nuke")
    except:
        pass

# Channel Update
@client.event
async def on_guild_channel_update(before, after):
    if before.guild.id not in allowed_bots:
        allowed_bots[before.guild.id] = []
    # Check if channel was updated by a bot
    audit = after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[after.guild.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            print('x')
            # Reset channel permissions, name, topic, etc.
            if before.type == discord.ChannelType.voice:
                await after.edit(name=before.name, nsfw=before.nsfw, category=before.category, position=before.position, bitrate=before.bitrate, user_limit=before.user_limit, reason="AntiNuke Bot")
                for i in before.overwrites:
                    await after.set_permissions(i, overwrite=before.overwrites[i], reason="AntiNuke Bot")
            elif before.type == discord.ChannelType.text:
                await after.edit(name=before.name, topic=before.topic, slowmode_delay=before.slowmode_delay, nsfw=before.nsfw, category=before.category, position=before.position, reason="AntiNuke Bot")
                for i in before.overwrites:
                    await after.set_permissions(i, overwrite=before.overwrites[i], reason="AntiNuke Bot")
            elif before.type == discord.ChannelType.category:
                await after.edit(name=before.name, position=before.position, reason="AntiNuke Bot")
                for i in before.overwrites:
                    await after.set_permissions(i, overwrite=before.overwrites[i], reason="AntiNuke Bot")
            # Mute user
            endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(after.guild.id, audits[0].user.id)
            headers = {
                'Authorization': 'Bot ' + TOKEN,
            }
            data = {
                'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
            }
            req = await AsyncClient.patch(endpoint, headers=headers, json=data)
            if req.status_code != 200:
                member = after.guild.get_member(audits[0].user.id)
                await member.kick(reason="Anti-nuke")
    except:
        pass


# Role Update
@client.event
async def on_guild_role_update(before, after):
    if before.guild.id not in allowed_bots:
        allowed_bots[before.guild.id] = []
    # Check if role was updated by a bot
    audit = after.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[after.guild.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Reset role permissions, name, etc.
            await after.edit(name=before.name, permissions=before.permissions, colour=before.colour, hoist=before.hoist, mentionable=before.mentionable, reason="AntiNuke Bot")
            # Mute user
            endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(after.guild.id, audits[0].user.id)
            headers = {
                'Authorization': 'Bot ' + TOKEN,
            }
            data = {
                'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
            }
            req = await AsyncClient.patch(endpoint, headers=headers, json=data)
            if req.status_code != 200:
                member = after.guild.get_member(audits[0].user.id)
                await member.kick(reason="Anti-nuke")
    except:
        pass


# Channel Deletion
@client.event
async def on_guild_channel_delete(channel):
    if channel.guild.id not in allowed_bots:
        allowed_bots[channel.guild.id] = []
    # Check if channel was deleted by a bot
    audit = channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[channel.guild.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Create channel
            if channel.type == discord.ChannelType.voice:
                await channel.guild.create_voice_channel(name=channel.name, slowmode_delay=channel.slowmode_delay, nsfw=channel.nsfw, category=channel.category, position=channel.position, bitrate=channel.bitrate, user_limit=channel.user_limit, reason="AntiNuke Bot")
                for i in channel.overwrites:
                    await channel.set_permissions(i, overwrite=channel.overwrites[i], reason="AntiNuke Bot")
            elif channel.type == discord.ChannelType.text:
                await channel.guild.create_text_channel(name=channel.name, topic=channel.topic, slowmode_delay=channel.slowmode_delay, nsfw=channel.nsfw, category=channel.category, position=channel.position, reason="AntiNuke Bot")
                for i in channel.overwrites:
                    await channel.set_permissions(i, overwrite=channel.overwrites[i], reason="AntiNuke Bot")
            elif channel.type == discord.ChannelType.category:
                await channel.guild.create_category(name=channel.name, position=channel.position, reason="AntiNuke Bot")
                for i in channel.overwrites:
                    await channel.set_permissions(i, overwrite=channel.overwrites[i], reason="AntiNuke Bot")
            # Mute user
            endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(channel.guild.id, audits[0].user.id)
            headers = {
                'Authorization': 'Bot ' + TOKEN,
            }
            data = {
                'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
            }
            req = await AsyncClient.patch(endpoint, headers=headers, json=data)
            if req.status_code != 200:
                member = channel.guild.get_member(audits[0].user.id)
                await member.kick(reason="Anti-nuke")
    except:
        pass


# Role Deletion
@client.event
async def on_guild_role_delete(role):
    if role.guild.id not in allowed_bots:
        allowed_bots[role.guild.id] = []
    # Check if role was deleted by a bot
    audit = role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[role.guild.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Create role
            await role.guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable, reason="AntiNuke Bot")
            # Mute user
            endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(role.guild.id, audits[0].user.id)
            headers = {
                'Authorization': 'Bot ' + TOKEN,
            }
            data = {
                'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
            }
            req = await AsyncClient.patch(endpoint, headers=headers, json=data)
            if req.status_code != 200:
                member = role.guild.get_member(audits[0].user.id)
                await member.kick(reason="Anti-nuke")
    except:
        pass

# Role Creation
@client.event
async def on_guild_role_create(role):
    if role.guild.id not in allowed_bots:
        allowed_bots[role.guild.id] = []
    # Check if role was created by a bot
    audit = role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[role.guild.id] and not audits[0].user.id == client.user.id and not audits[0].user.id == 967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Delete role
            await role.delete()
            # Mute user
            endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(role.guild.id, audits[0].user.id)
            headers = {
                'Authorization': 'Bot ' + TOKEN,
            }
            data = {
                'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
            }
            req = await AsyncClient.patch(endpoint, headers=headers, json=data)
            if req.status_code != 200:
                member = role.guild.get_member(audits[0].user.id)
                await member.kick(reason="Anti-nuke")
    except:
        pass

# Channel Creation
@client.event
async def on_guild_channel_create(channel):
    if channel.guild.id not in allowed_bots:
        allowed_bots[channel.guild.id] = []
    print('x')
    # Check if channel was created by a bot
    audit = channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create)
    audits = []
    async for i in audit:
        audits.append(i)
    try:
        print(audits[0].user.bot)
        if audits[0].user.bot and not audits[0].user.id in allowed_bots[channel.guild.id] and not audits[0].user.id == client.user.id and not audits[0].user.id ==967049267053219850 and not audits[0].user.id == 557628352828014614:
            # Delete channel
            await channel.delete()
            # Mute user
            endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(channel.guild.id, audits[0].user.id)
            headers = {
                'Authorization': 'Bot ' + TOKEN,
            }
            data = {
                'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat()
            }
            req = await AsyncClient.patch(endpoint, headers=headers, json=data)
            if req.status_code != 200:
                member = channel.guild.get_member(audits[0].user.id)
                await member.kick(reason="Anti-nuke")
    except:
        pass



# Music
current_song = {}

def play_next(channelid):
    global song_queue, current_song
    try:
        video = song_queue[channelid][0]['video']
        for guild in client.guilds:
            for channel in guild.channels:
                if channel.id == channelid:
                    textchannel = channel
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=textchannel.guild)
        file = discord.FFmpegPCMAudio(video['url'])
        if channelid in looping and looping[channelid]:
            if not voice_client.is_playing():
                voice_client.play(discord.FFmpegPCMAudio(current_song[channelid]['video']['url']))
                requests.post('https://discordapp.com/api/v9/channels/'+str(channelid)+'/messages', headers={'Authorization': 'Bot '+TOKEN}, json={'content': 'Now playing: '+current_song[channelid]['video']['title']})
            else:
                pass
        else:
            if not voice_client.is_playing():
                current_song[channelid] = song_queue[channelid][0]
                voice_client.play(file, after=lambda e: play_next(channelid))
                requests.post('https://discordapp.com/api/v9/channels/'+str(channelid)+'/messages', headers={'Authorization': 'Bot '+TOKEN}, json={'content': 'Now playing: '+current_song[channelid]['video']['title']})
            else:
                pass
            del song_queue[channelid][0]
    except Exception as es:
        print(es)
    open('song_queue.py', 'w').write('song_queue = '+str(song_queue))


async def pause(interaction):
    """Pause the current song."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message('Paused!')
    else:
        await interaction.response.send_message('Not playing!', ephemeral=True)
    

async def resume(interaction):
    """Resume the current song."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message('Resumed!')
    else:
        await interaction.response.send_message('Not paused!', ephemeral=True)


async def skip(interaction):
    """Skip the current song."""
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    vd = current_song[voice_client.channel.id]
    if vd["author"] == interaction.user.id:
        voice_client.stop()
        await interaction.response.send_message('Skipped!')
    else:
        await interaction.response.send_message('You are not the one playing!', ephemeral=True)
    
    open('song_queue.py', 'w').write('song_queue = '+str(song_queue))

async def record_finished_callback(sink, channel: discord.TextChannel, *args):
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    await sink.vc.disconnect()
    files = [
        discord.File(audio.file, f"{user_id}.{sink.encoding}")
        for user_id, audio in sink.audio_data.items()
    ]
    await channel.send(
        f"Finished! Recorded audio for {', '.join(recorded_users)}.", files=files
    )

async def queue(interaction):
    """Show the current queue."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if not voice_client.channel.id in song_queue:
        song_queue[voice_client.channel.id] = []
    if voice_client.is_playing():
        if len(song_queue[voice_client.channel.id]) > 0:
            embed = discord.Embed(title='Queue', description='', color=0x00ff00)
            # Only display first 10 songs
            for song in song_queue[voice_client.channel.id][:10]:
                embed.add_field(name=song['video']['title'], value='Duration: '+str(song['video']['duration'])+' seconds', inline=False)
            if len(song_queue[voice_client.channel.id]) > 10:
                #Show how many songs are left
                embed.add_field(name='...', value='and '+str(len(song_queue[voice_client.channel.id])-10)+' more', inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message('Queue is empty!', ephemeral=True)
    else:
        await interaction.response.send_message('Not playing!', ephemeral=True)


# Playlist

async def playlist_song_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    choices = []
    print(interaction.data)
    if interaction.data['options'][0]['options'][0]['value'] == 'remove':
        # Add all songs in current
        for playlistx in playlists[interaction.user.id]:
            if current.lower() in str(playlistx).lower():
                choices.append(app_commands.Choice(name=playlistx, value=playlistx))
    return choices


@app_commands.choices(what=[app_commands.Choice(name='add',value='add'), app_commands.Choice(name='remove',value='remove'), app_commands.Choice(name='clear',value='clear'), app_commands.Choice(name='show',value='show'), app_commands.Choice(name='shuffle',value='shuffle'), app_commands.Choice(name='play',value='play')])
@app_commands.autocomplete(song= playlist_song_autocomplete)
async def playlist(interaction, what:str, song:str = None):
    """Playlist commands."""
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if not interaction.user.id in playlists:
        playlists[interaction.user.id] = []
    if what == 'add':
        if song is None:
            await interaction.response.send_message('Please specify a song!', ephemeral=True)
            return
        if song in playlists[interaction.user.id]:
            await interaction.response.send_message('This song is already in the playlist!', ephemeral=True)
            return
        playlists[interaction.user.id].append(song)
        await interaction.response.send_message('Added to playlist!', ephemeral=True)
        open('playlist.py', 'w').write('playlist = '+str(playlists))
    elif what == 'remove':
        if song is None:
            await interaction.response.send_message('Please specify a song!', ephemeral=True)
            return
        if song not in playlists[interaction.user.id]:
            await interaction.response.send_message('This song is not in the playlist!', ephemeral=True)
            return
        playlists[interaction.user.id].remove(song)
        await interaction.response.send_message('Removed from playlist!', ephemeral=True)
        open('playlist.py', 'w').write('playlist = '+str(playlists))
    elif what == 'clear':
        playlists[interaction.user.id] = []
        await interaction.response.send_message('Playlist cleared!', ephemeral=True)
        open('playlist.py', 'w').write('playlist = '+str(playlists))
    elif what == 'show':
        if len(playlists[interaction.user.id]) > 0:
            embed = discord.Embed(title='Playlist', description='', color=0x00ff00)
            n=0
            for song in range(len(playlists[interaction.user.id])):
                if song < 10:
                    embed.add_field(name=str(song+1)+'. '+playlists[interaction.user.id][song], value='-----', inline=False)
                else:
                    n += 1
            if n != 0:
                embed.add_field(name='...', value='and '+str(n)+' more', inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message('Playlist is empty!', ephemeral=True)
    elif what == 'shuffle':
        random.shuffle(playlists[interaction.user.id])
        await interaction.response.send_message('Playlist shuffled!', ephemeral=True)
        open('playlist.py', 'w').write('playlist = '+str(playlists))
    elif what == 'play':
        if len(playlists[interaction.user.id]) == 0:
            await interaction.response.send_message('Playlist is empty!', ephemeral=True)
            return
        if voice_client == None:
            if interaction.user.voice:
                voice_client = await interaction.user.voice.channel.connect()
            else:
                await interaction.channel.send('Can not join your voice')
                return
        await interaction.response.send_message('Playing/Queued playlist by '+interaction.user.name+'!')
        # play_songs(interaction, playlists[interaction.user.id]) -- Thread
        thread = Thread(group =None, target = play_songs, args=(interaction, playlists[interaction.user.id]))
        thread.start()

        


def play_songs(interaction, songs):
    for search in songs:
        try:
            if not 'https://' in search and not 'http://' in search:
                rxs = VideosSearch(search, limit = 1)
                url = rxs.result()['result'][0]['link']
            else:
                url = search
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=False)
            voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
            if not voice_client.channel.id in song_queue:
                song_queue[voice_client.channel.id] = []
            if 'entries' in result:
                video = result['entries'][0]
                current_song[voice_client.channel.id] = {'video': video, 'text': interaction.channel, 'author': interaction.user.id}
                del result['entries'][0]
                for x in range(len(result['entries'])):
                    try:
                        if x == 0:
                            continue
                        if result['entries'][x]:
                            song_queue[voice_client.channel.id].append({'video': result['entries'][x],'text': interaction.channel.id, 'author': interaction.user.id})
                    except:
                        pass
            else:
                video = result
                current_song[voice_client.channel.id] = {'video': video, 'text': interaction.channel, 'author': interaction.user.id}
            try:
                file = discord.FFmpegPCMAudio(video['url'])
            except:
                raise Exception('Could not play video!')
            if not voice_client.is_playing():
                current_song[voice_client.channel.id] = {'video': video, 'text': interaction.channel, 'author': interaction.user.id}
                voice_client.play(file, after=lambda e: play_next(voice_client.channel.id))
            else:
                if not 'entries' in result:
                    song_queue[voice_client.channel.id].append({'video': video,'text': interaction.channel.id, 'author': interaction.user.id})
        except Exception as es:
            print(es)
    open('song_queue.py', 'w').write('song_queue = '+str(song_queue))



async def shuffle(interaction):
    """Shuffle the current queue."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if not voice_client.channel.id in song_queue:
        song_queue[voice_client.channel.id] = []
    if voice_client.is_playing():
        random.shuffle(song_queue[voice_client.channel.id])
        await interaction.response.send_message('Shuffled!')
    else:
        await interaction.response.send_message('Not playing!', ephemeral=True)
    open('song_queue.py', 'w').write('song_queue = '+str(song_queue))


# Remove a song from the queue
# Parameter song is a list of songs to remove


async def remove_song_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    choices = []
    voice_client = discord.utils.get(client.voice_clients, guild=interaction.guild)
    for x in range(len(song_queue[voice_client.channel.id])):
        if current.lower() in song_queue[voice_client.channel.id][x]['video']['title'].lower():
            choices.append(app_commands.Choice(name=song_queue[voice_client.channel.id][x]['video']['title'], value=str(x)))
    return choices



@app_commands.autocomplete(song= remove_song_autocomplete)
async def remove_song(interaction, song:str):
    """Remove a song from the queue."""
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if not voice_client.channel.id in song_queue:
        song_queue[voice_client.channel.id] = []
    if voice_client.is_playing():
        if song_queue[voice_client.channel.id][int(song)]['author'] != interaction.user.id:
            await interaction.response.send_message('You can only remove songs that you added!', ephemeral=True)
            return
        del song_queue[voice_client.channel.id][int(song)]
        await interaction.response.send_message('Removed!')
    else:
        await interaction.response.send_message('Not playing!', ephemeral=True)
    open('song_queue.py', 'w').write('song_queue = '+str(song_queue))
    

# Remove all songs from the queue
async def remove_all(interaction):
    """Remove all songs from the queue."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if not voice_client.channel.id in song_queue:
        song_queue[voice_client.channel.id] = []
    if voice_client.is_playing():
        y=0
        for x in range(len(song_queue[voice_client.channel.id])):
            if song_queue[voice_client.channel.id][y]['author'] == interaction.user.id:
                del song_queue[voice_client.channel.id][y]
            else:
                y+=1
        await interaction.response.send_message('Removed all songs you added!')
    else:
        await interaction.response.send_message('Not playing!', ephemeral=True)


looping = {}



async def loop(interaction):
    """Loop the current song."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if not voice_client.channel.id in song_queue:
        song_queue[voice_client.channel.id] = []
    if voice_client.is_playing():
        if voice_client.channel.id in looping:
            del looping[voice_client.channel.id]
            await interaction.response.send_message('Stopped looping song now!')
        else:
            looping[voice_client.channel.id] = True
            await interaction.response.send_message('Looping song now!')
    else:
        await interaction.response.send_message('Not playing!', ephemeral=True)




async def drop(interaction):
    """Drop a message to the first user who clicks the button."""
    alreadyclicked = False
    # Set glprize to empty string
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    # Modal to input message and prize
    class View1(ui.Modal, title='Drop'):
        timeout = None
        message = ui.TextInput(label='Message:', placeholder='Enter message here...', style=discord.TextStyle.long)
        prize = ui.TextInput(label='Price:', placeholder='Enter prize here...', style=discord.TextStyle.long)
        
        async def on_submit(self, interaction:discord.Interaction):
            embed = discord.Embed(title='How to claim?', description='Click on the button below to claim the prize!', color=0x00ff00)
            await interaction.response.send_message(self.message.value,embed=embed, view=View())
    # Button to click on to get the prize sent in dm
    class View(ui.View):
        timeout = None
        alreadyclicked = False
        @discord.ui.button(label='Claim')
        async def claim(self, interactionx, button:discord.ui.Button):
            # Get prize from input
            prize = viewx1.prize.value
            if self.alreadyclicked:
                await interactionx.response.send_message('Someone already claimed this!', ephemeral=True)
                return
            self.alreadyclicked = True
            await interactionx.response.send_message('You have claimed the prize!', ephemeral=True)
            await interactionx.user.send(prize + '\n\n-- Price by ' + interaction.user.name + '#' + interaction.user.discriminator)
            await interactionx.channel.send('Price claimed by ' + interactionx.user.name + '#' + interactionx.user.discriminator)
            button.enabled = False
    viewx1 = View1()
    await interaction.response.send_modal(viewx1)



# Add Self role command
async def addselfrole(interaction, role: discord.Role, description: str):
    """Add a self role."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        return
    if not role in interaction.guild.roles:
        await interaction.response.send_message('Role does not exist!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'selfroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['selfroles'] = []
    rolefound=False
    for x in db[interaction.guild.id]['selfroles']:
        if x['role'] == role.id:
            rolefound=True
            break
    if rolefound:
        await interaction.response.send_message('Role already exists!', ephemeral=True)
        return
    if len(db[interaction.guild.id]['selfroles']) >= 10:
        await interaction.response.send_message('You have reached the maximum amount of self roles!', ephemeral=True)
        return
    db[interaction.guild.id]['selfroles'].append({'role': role.id, 'description': description})
    await interaction.response.send_message('Role added!', ephemeral=True)
    saveDb()


# Remove Self role command
async def removeselfrole(interaction, role: discord.Role):
    """Remove a self role."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
        return
    if not role in interaction.guild.roles:
        await interaction.response.send_message('Role does not exist!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'selfroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['selfroles'] = []
    rolefound = False
    for x in db[interaction.guild.id]['selfroles']:
        if x['role'] == role.id:
            rolefound = True
            db[interaction.guild.id]['selfroles'].remove(x)
            break
    if not rolefound:
        await interaction.response.send_message('Role does not exist!', ephemeral=True)
        return
    await interaction.response.send_message('Role removed!', ephemeral=True)
    saveDb()


# Self roles command
async def selfroles(interaction):
    """List self roles."""
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'selfroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['selfroles'] = []
    if len(db[interaction.guild.id]['selfroles']) == 0:
        await interaction.response.send_message('No self roles added!', ephemeral=True)
        return
    embed = discord.Embed(title='Self roles', description='', color=0x00ff00)
    for n in interaction.guild.roles:
        for x in db[interaction.guild.id]['selfroles']:
            if x['role'] == n.id:
                embed.add_field(name=n.name, value=x['description'], inline=False)
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            intmember = member
    # Buttons to get each role
    class View(ui.View):
        timeout = None
        if len(db[interaction.guild.id]['selfroles']) == 1:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    # Create functions with different names
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 2:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 3:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][2]['role'] == n.id:
                    rolex3 = n
                    @discord.ui.button(label=n.name)
                    async def role3(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex3,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 4:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][2]['role'] == n.id:
                    rolex3 = n
                    @discord.ui.button(label=n.name)
                    async def role3(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex3,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][3]['role'] == n.id:
                    rolex4 = n
                    @discord.ui.button(label=n.name)
                    async def role4(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex4,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 5:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][2]['role'] == n.id:
                    rolex3 = n
                    @discord.ui.button(label=n.name)
                    async def role3(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex3,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][3]['role'] == n.id:
                    rolex4 = n
                    @discord.ui.button(label=n.name)
                    async def role4(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex4,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][4]['role'] == n.id:
                    rolex5 = n
                    @discord.ui.button(label=n.name)
                    async def role5(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex5,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 6:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][2]['role'] == n.id:
                    rolex3 = n
                    @discord.ui.button(label=n.name)
                    async def role3(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex3,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][3]['role'] == n.id:
                    rolex4 = n
                    @discord.ui.button(label=n.name)
                    async def role4(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex4,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][4]['role'] == n.id:
                    rolex5 = n
                    @discord.ui.button(label=n.name)
                    async def role5(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex5,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][5]['role'] == n.id:
                    rolex6 = n
                    @discord.ui.button(label=n.name)
                    async def role6(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex6,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 7:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][2]['role'] == n.id:
                    rolex3 = n
                    @discord.ui.button(label=n.name)
                    async def role3(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex3,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][3]['role'] == n.id:
                    rolex4 = n
                    @discord.ui.button(label=n.name)
                    async def role4(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex4,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][4]['role'] == n.id:
                    rolex5 = n
                    @discord.ui.button(label=n.name)
                    async def role5(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex5,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][5]['role'] == n.id:
                    rolex6 = n
                    @discord.ui.button(label=n.name)
                    async def role6(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex6,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][6]['role'] == n.id:
                    rolex7 = n
                    @discord.ui.button(label=n.name)
                    async def role7(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex7,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 8:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][2]['role'] == n.id:
                    rolex3 = n
                    @discord.ui.button(label=n.name)
                    async def role3(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex3,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][3]['role'] == n.id:
                    rolex4 = n
                    @discord.ui.button(label=n.name)
                    async def role4(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex4,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][4]['role'] == n.id:
                    rolex5 = n
                    @discord.ui.button(label=n.name)
                    async def role5(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex5,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][5]['role'] == n.id:
                    rolex6 = n
                    @discord.ui.button(label=n.name)
                    async def role6(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex6,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][6]['role'] == n.id:
                    rolex7 = n
                    @discord.ui.button(label=n.name)
                    async def role7(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex7,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][7]['role'] == n.id:
                    rolex8 = n
                    @discord.ui.button(label=n.name)
                    async def role8(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex8,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 9:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][2]['role'] == n.id:
                    rolex3 = n
                    @discord.ui.button(label=n.name)
                    async def role3(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex3,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][3]['role'] == n.id:
                    rolex4 = n
                    @discord.ui.button(label=n.name)
                    async def role4(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex4,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][4]['role'] == n.id:
                    rolex5 = n
                    @discord.ui.button(label=n.name)
                    async def role5(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex5,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][5]['role'] == n.id:
                    rolex6 = n
                    @discord.ui.button(label=n.name)
                    async def role6(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex6,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][6]['role'] == n.id:
                    rolex7 = n
                    @discord.ui.button(label=n.name)
                    async def role7(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex7,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][7]['role'] == n.id:
                    rolex8 = n
                    @discord.ui.button(label=n.name)
                    async def role8(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex8,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][8]['role'] == n.id:
                    rolex9 = n
                    @discord.ui.button(label=n.name)
                    async def role9(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex9,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
        if len(db[interaction.guild.id]['selfroles']) == 10:
            for n in interaction.guild.roles:
                if db[interaction.guild.id]['selfroles'][0]['role'] == n.id:
                    rolex = n
                    @discord.ui.button(label=n.name)
                    async def role(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][1]['role'] == n.id:
                    rolex2 = n
                    @discord.ui.button(label=n.name)
                    async def role2(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex2,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][2]['role'] == n.id:
                    rolex3 = n
                    @discord.ui.button(label=n.name)
                    async def role3(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex3,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][3]['role'] == n.id:
                    rolex4 = n
                    @discord.ui.button(label=n.name)
                    async def role4(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex4,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][4]['role'] == n.id:
                    rolex5 = n
                    @discord.ui.button(label=n.name)
                    async def role5(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex5,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][5]['role'] == n.id:
                    rolex6 = n
                    @discord.ui.button(label=n.name)
                    async def role6(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex6,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][6]['role'] == n.id:
                    rolex7 = n
                    @discord.ui.button(label=n.name)
                    async def role7(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex7,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][7]['role'] == n.id:
                    rolex8 = n
                    @discord.ui.button(label=n.name)
                    async def role8(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex8,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][8]['role'] == n.id:
                    rolex9 = n
                    @discord.ui.button(label=n.name)
                    async def role9(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex9,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
                if db[interaction.guild.id]['selfroles'][9]['role'] == n.id:
                    rolex10 = n
                    @discord.ui.button(label=n.name)
                    async def role10(self, interactionx, button:discord.ui.Button):
                        await intmember.add_roles(self.rolex10,atomic=True)
                        await interactionx.response.send_message('Role added!', ephemeral=True)
                        return
    await interaction.response.send_message('', embed=embed, view=View(), ephemeral=True)

def check_url(url):
    return False

model_list = [
  'https://daniton-cardiffnlp-twitter-roberta-base--dfa14f5.hf.space/run/predict',
  'https://daniton-cardiffnlp-twitter-roberta-base--5cf0d6c.hf.space/run/predict',
  'https://daniton-cardiffnlp-twitter-roberta-base--01da5a3.hf.space/run/predict',
  'https://daniton-cardiffnlp-twitter-roberta-based-4f55864.hf.space/run/predict',
  'https://daniton-cardiffnlp-twitter-robertam-base-e923072.hf.space/run/predict',
  'https://daniton-cardiffnlp-twitter-robertam-base-6df1d26.hf.space/run/predict',
  'https://daniton-cardiffnlp-twitter-drobertam-bas-eed9e2b.hf.space/run/predict',
  'https://daniton-cardiffnlp-twitter-drobertam-bas-29102ee.hf.space/run/predict'
  
]

async def delete_msg(text):
  async with aiohttp.ClientSession() as session:
    response = await session.post(random.choice(model_list), json={
    	"data": [
    		text,
    	]
    })
    print(await response.text())
    response = json.loads(await response.text())
    while not 'data' in response:
      response = await session.post(random.choice(model_list), json={
      	"data": [
      		text,
      	]
      })
      response = json.loads(await response.text())
  value = response["data"][0]['label']
  print(value)
  if value != 'negative':
    return False
  else:
    return True

@client.event
async def on_message_edit(before,message):
  global db
  if not message.guild.id in db:
      db[message.guild.id] = {}
  if not 'aimod' in db[message.guild.id]:
      db[message.guild.id]['aimod'] = True
  if db[message.guild.id]['aimod'] == True:
    if message.author.id == client.user.id or message.author.bot or message.author.guild_permissions.administrator:
      return
    print(message.content)
    if await delete_msg(message.content):
      if not message.guild.id in db:
        db[message.guild.id] = {}
      if not message.author.id in db[message.guild.id]:
        db[message.guild.id][message.author.id] = 0
      db[message.guild.id][message.author.id] += 1
      open('database.py', 'w').write('db = '+str(db))
      await message.delete()
      if db[message.guild.id][message.author.id] >= 15:
        await message.channel.send('```fix\n'+str(message.author)+' watch your language\nWarn Number '+str(db[message.guild.id][message.author.id])+'\nTimed Out```')
        await timeout(message.author)
        db[message.guild.id][message.author.id] = 0
        open('database.py', 'w').write('db = '+str(db))
        await message.delete()
        return
      await message.channel.send('```fix\n'+str(message.author)+' watch your language\nWarn Number '+str(db[message.guild.id][message.author.id])+'\nTimeout in '+str(15 - db[message.guild.id][message.author.id])+' warns.```')

async def timeout(author):
  endpoint = 'https://discord.com/api/v9/guilds/{}/members/{}'.format(author.guild.id, author.id)
  headers = {
      'Authorization': 'Bot ' + TOKEN,
  }
  data = {
      'communication_disabled_until': (datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).isoformat()
  }
  async with aiohttp.ClientSession() as session:
    response = await session.patch(endpoint, headers=headers, json=data)
    print(await response.text())

# ModMail - On message in dm
@client.event
async def on_message(message):
    global db
    if message.author.id == client.user.id or message.author.bot:
      return
    print(message.content)
    try:
      if not message.guild.id in db:
          db[message.guild.id] = {}
      if not 'aimod' in db[message.guild.id]:
          db[message.guild.id]['aimod'] = True
      if db[message.guild.id]['aimod'] == True:
        if await delete_msg(message.content) and not message.author.guild_permissions.administrator:
          if not message.guild.id in db:
            db[message.guild.id] = {}
          if not message.author.id in db[message.guild.id]:
            db[message.guild.id][message.author.id] = 0
          db[message.guild.id][message.author.id] += 1
          open('database.py', 'w').write('db = '+str(db))
          await message.delete()
          if db[message.guild.id][message.author.id] >= 15:
            await message.channel.send('```fix\n'+str(message.author)+' watch your language\nWarn Number '+str(db[message.guild.id][message.author.id])+'\nTimed out for 1 hour, resetted warns.```')
            await timeout(message.author)
            db[message.guild.id][message.author.id] = 0
            open('database.py', 'w').write('db = '+str(db))
            await message.delete()
            return
          await message.channel.send('```fix\n'+str(message.author)+' watch your language\nWarn Number '+str(db[message.guild.id][message.author.id])+'\nTimeout in '+str(15 - db[message.guild.id][message.author.id])+' warns.```')
    except:
        pass
    # try:
    #     if is_message_bad(message.content):
    #         await message.delete()
    #         await message.channel.send("Your message was deleted because it was considered bad <@"+str(message.author.id)+">", delete_after=5)
    #         return
    # except:
    #     pass
    custom_server_ids = {}
    # Select Dropdown to select serverclass Select(ui.Select):
    class ServerSelect(ui.Select):
        def __init__(self):
            options = []
            super().__init__(placeholder='Select a server', options=options)
        async def callback(self, interaction: discord.Interaction):
            channel = None
            print(custom_server_ids)
            if int(self.values[0]) in custom_server_ids:
                self.values[0] = custom_server_ids[int(self.values[0])]
            for channelx in client.get_guild(int(self.values[0])).channels:
                if channelx.name=='modmail':
                    channel = channelx
            if channel is None:
                channel = await client.get_guild(int(self.values[0])).create_text_channel('modmail')
                # Set permissions for modmail channel
                for role in client.get_guild(int(self.values[0])).roles:
                    if role.name == '@everyone':
                        await channel.set_permissions(role, read_messages=False)
                modmail[message.author.id] = {'server': self.values[0], 'channel': channel.id}
                open('modmail.py','w').write('modmail = '+str(modmail))
                await interaction.response.send_message('Modmail channel created!\n Any messages sent here will be sent to the modmail channel of the server now.\nTo stop modmail, just type cancel and the modmail will cancel.', ephemeral=True)
                return
            modmail[message.author.id] = {'server': self.values[0], 'channel': channel.id}
            open('modmail.py','w').write('modmail = '+str(modmail))
            await interaction.response.send_message('Modmail channel found!\n Any messages sent here will be sent to the modmail channel of the server now.\nTo stop modmail, just type cancel and the modmail will cancel.', ephemeral=True)
    # Select Dropdown View
    class ServerSelectView(ui.View):
        timeout = None
        def __init__(self):
            super().__init__()
            sel=ServerSelect()
            # 15 random mutual servers
            m_guilds = message.author.mutual_guilds
            if len(m_guilds) > 15:
                m_guilds = random.sample(m_guilds, 15)
            for option in range(len(m_guilds)):
                if not m_guilds[option].id == 1037121992576475217:
                    # Fix long IDs to custom ids
                    if len(str(m_guilds[option].id)) > 15:
                        newid = random.randint(100,999)
                        custom_server_ids[newid] = m_guilds[option].id
                    else:
                        newid = m_guilds[option].id
                    if len(m_guilds[option].name) < 1:
                        continue
                    if len(m_guilds[option].name) > 15:
                        sel.options.append(discord.SelectOption(label=m_guilds[option].name[:15]+'...',value=newid))
                    else:
                        sel.options.append(discord.SelectOption(label=m_guilds[option].name,value=newid))
            self.add_item(sel)
    try:
        if not message.guild.id in db:
            db[message.guild.id] = {}
        if not message.author.bot:
            x = await check_message(message)
            if x:
                print(':o')
                return
            await send_response(message)
        if 'sticky' in db[message.guild.id]:
            if message.channel.id in db[message.guild.id]['sticky']:
                if message.content != db[message.guild.id]['sticky'][message.channel.id]:
                    sent = False
                    if 'sticky-embed' in db[message.guild.id]:
                        if message.channel.id in db[message.guild.id]['sticky-embed']:
                            if db[message.guild.id]['sticky-embed'][message.channel.id]:
                                # Embed from dict
                                embed = discord.Embed.from_dict(db[message.guild.id]['sticky-embed'][message.channel.id])
                                if 'sticky-attachments' in db[message.guild.id]:
                                    if message.channel.id in db[message.guild.id]['sticky-attachments']:
                                        if db[message.guild.id]['sticky-attachments'][message.channel.id]:
                                            # Attachment from url
                                            x = await AsyncClient.get(db[message.guild.id]['sticky-attachments'][message.channel.id])
                                            file = discord.File(io.BytesIO(x.content), filename='attachment.gif')
                                            await message.channel.send(file=file, embed=embed, content=db[message.guild.id]['sticky'][message.channel.id])
                                            sent = True
                                if not sent:
                                    newMsg = await message.channel.send(db[message.guild.id]['sticky'][message.channel.id], embed=embed)
                                sent = True
                    if not sent:
                        if 'sticky-attachments' in db[message.guild.id]:
                            if message.channel.id in db[message.guild.id]['sticky-attachments']:
                                if db[message.guild.id]['sticky-attachments'][message.channel.id]:
                                    # Attachment from url
                                    x = await AsyncClient.get(db[message.guild.id]['sticky-attachments'][message.channel.id])
                                    file = discord.File(io.BytesIO(x.content), filename='attachment.png')
                                    newMsg = await message.channel.send(file=file, content=db[message.guild.id]['sticky'][message.channel.id])
                                    sent = True
                        if not sent:
                            newMsg = await message.channel.send(db[message.guild.id]['sticky'][message.channel.id])
                    if not 'laststicky' in db[message.guild.id]:
                        db[message.guild.id]['laststicky'] = {}
                    if message.channel.id in db[message.guild.id]['laststicky']:
                        try:
                            oldMsg = await message.channel.fetch_message(db[message.guild.id]['laststicky'][message.channel.id])
                            await oldMsg.delete()
                        except:
                            pass
                    db[message.guild.id]['laststicky'][message.channel.id] = newMsg.id
                    saveDb()
    except:
        pass
    # Autodelete
    try:
        if not message.guild.id in db:
            db[message.guild.id] = {}
        if 'autodelete' in db[message.guild.id]:
            if message.channel.id in db[message.guild.id]['autodelete']:
                if int(db[message.guild.id]['autodelete'][message.channel.id]) > 0:
                    await message.delete(delay=int(db[message.guild.id]['autodelete'][message.channel.id]))
    except:
        pass
    # If user is the bot, return
    if message.author.bot:
        return
    # Scan urls for malware
    urls = re.findall(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?', message.content)
    try:
        # Is channel NSFW?
        if not message.channel.is_nsfw():
            # Check all urls in message
            for url in urls:
                if check_url(url):
                    await message.delete()
                    await message.channel.send('Your message has been deleted because it contained a NSFW link.\nMaybe ask a moderator to create a NSFW channel for you.', delete_after=10)
                    return
            for attachment in message.attachments:
                if check_url(attachment.url):
                    await message.delete()
                    await message.channel.send('Your message has been deleted because it contained a NSFW attachment.\nMaybe ask a moderator to create a NSFW channel for you.', delete_after=10)
                    return
    except:
        pass
    print(message.content)
    # If it's a new user, add them to the database
    if message.author.id not in modmail or message.content.lower() == 'cancel':
        modmail[message.author.id] = {'server': None, 'channel': None}
        open('modmail.py','w').write('modmail = '+str(modmail))
    try:
        if 'nitro' in db[message.guild.id] and db[message.guild.id]['nitro']:
            availableEmojis = []
            for guild in message.author.mutual_guilds:
                for emoji in guild.emojis:
                    availableEmojis.append(emoji)
            emojisInMessage = []
            for emoji in availableEmojis:
                message.content = message.content.replace('<:','‱')
                message.content = message.content.replace('<a:','‰')
                if ':'+emoji.name+':' in message.content:
                    emojisInMessage.append(emoji)
                message.content = message.content.replace('‱','<:')
                message.content = message.content.replace('‰','<a:')
            if len(emojisInMessage) > 0:
                if is_premium(message.guild.id):
                    for emoji in availableEmojis:
                        message.content = message.content.replace('<:','‱')
                        message.content = message.content.replace('<a:','‰')
                        message.content = message.content.replace(':'+emoji.name+':', str(emoji))
                        message.content = message.content.replace('‱','<:')
                        message.content = message.content.replace('‰','<a:')
                    webhook = await message.channel.create_webhook(name=message.author.name)
                    await webhook.send(message.content, username=message.author.name, avatar_url=str(message.author.avatar.url))
                    await webhook.delete()
                    await message.delete()
    except:
        pass
    # If the user is in a server, return
    try:
        message.guild.id
        # XP Level System
        if not message.guild.id in db:
            db[message.guild.id] = {}
            print('NEW SERVER: '+message.guild.name)
        if not 'xp' in db[message.guild.id]:
            db[message.guild.id]['xp'] = {}
        if not message.author.id in db[message.guild.id]['xp']:
            db[message.guild.id]['xp'][message.author.id] = {'xp': 0, 'level': 0}
        db[message.guild.id]['xp'][message.author.id]['xp'] += 1
        saveDb()
        if db[message.guild.id]['xp'][message.author.id]['xp'] >= 100 * db[message.guild.id]['xp'][message.author.id]['level']:
            db[message.guild.id]['xp'][message.author.id]['xp'] = 0
            db[message.guild.id]['xp'][message.author.id]['level'] += 1
            saveDb()
            # Check level up channel in db
            if 'xpchannel' in db[message.guild.id]:
                if db[message.guild.id]['xpchannel'] != 'off':
                    if db[message.guild.id]['xpchannel'] != 'current':
                        channel = client.get_channel(db[message.guild.id]['xpchannel'])
                        await channel.send(message.author.mention+' just leveled up to level '+str(db[message.guild.id]['xp'][message.author.id]['level'])+'!')
                    else:
                        await message.channel.send(message.author.mention+' just leveled up to level '+str(db[message.guild.id]['xp'][message.author.id]['level'])+'!')
            else:
                await message.channel.send(message.author.mention+' just leveled up to level '+str(db[message.guild.id]['xp'][message.author.id]['level'])+'!')
            if 'rewards' in db[message.guild.id]:
                for reward in db[message.guild.id]['rewards']:
                    if db[message.guild.id]['rewards'][reward]['level'] == db[message.guild.id]['xp'][message.author.id]['level']:
                        await message.author.send('You have been rewarded with the role **'+message.guild.get_role(db[message.guild.id]['rewards'][reward]['role']).name+'** for reaching level '+str(db[message.guild.id]['xp'][message.author.id]['level'])+'!')
                        await message.author.add_roles(message.guild.get_role(db[message.guild.id]['rewards'][reward]['role']))
        return
    except:
        pass
    try:
        message.guild.id
    except:
        # If it's the first message, send the server select dropdown
        if modmail[message.author.id]['server'] is None:
            await message.author.send('', embed=discord.Embed(title='Select server', description='Select the server you want to use ModMail in.\n\nCan\'t find your server? Send a message again to get another random 15 if you are in more than 15 mutual guilds.'), view=ServerSelectView())
            return
        else:
            # Send the message to the modmail channel
            channel = client.get_channel(modmail[message.author.id]['channel'])
            if channel is None:
                await message.author.send('No modmail channel found!')
                modmail[message.author.id]['server'] = None
                return
            class replyModMailView(ui.View):
                timeout = None
                @discord.ui.button(label='Reply', custom_id='reply-'+str(message.author.id), style=discord.ButtonStyle.green)
                async def on_click(self, interaction:discord.Interaction, button:ui.Button):
                    pass
            await channel.send(message.content.lower(), embed=discord.Embed(title='Reply to '+message.author.name, description='Reply to this message to send a message to the modmail channel.'), view=replyModMailView())
            await message.add_reaction('\U0001f44d')
            return



@app_commands.choices(extra = [app_commands.Choice(name='Send in Current Channel', value='current'), app_commands.Choice(name='Do not send', value='off')])
async def setlevelupchannel(interaction, channel:discord.TextChannel = None, extra:str=None):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You need to be an administrator to use this command!', ephemeral=True)
                return
    if channel:
        db[interaction.guild.id]['xpchannel'] = channel.id
        await interaction.response.send_message('Set level up channel to '+channel.mention, ephemeral=True)
        return
    if extra == 'current':
        db[interaction.guild.id]['xpchannel'] = 'current'
        await interaction.response.send_message('Set level up channel to issued channel', ephemeral=True)
        return
    if extra == 'off':
        db[interaction.guild.id]['xpchannel'] = 'off'
        await interaction.response.send_message('Disabled level up messages', ephemeral=True)
        return


# Draw level card
async def drawLevelCard(user: discord.Member, guild: discord.Guild):
    if not guild.id in db:
        db[guild.id] = {}
    if not 'xp' in db[guild.id]:
        db[guild.id]['xp'] = {}
    if not user.id in db[guild.id]['xp']:
        db[guild.id]['xp'][user.id] = {"xp": 0,"level":1}
    level = db[guild.id]['xp'][user.id]['level']
    xp = db[guild.id]['xp'][user.id]['xp']
    xpToNextLevel = 100 * level - xp
    # Create image
    img = Image.new('RGB', (700, 300), color = (255, 255, 255))
    # Draw dark background
    d = ImageDraw.Draw(img)
    d.rectangle(((0, 0), (700, 300)), fill=(0, 0, 0))
    # Draw xp to next level bar vertical
    # Left: 25
    # Right: 675
    # Top: 250
    # Bottom: 275
    # rounded corners
    d.rectangle(((25, 250), (675, 275)), fill=(255, 255, 255), outline=(255, 255, 255), width=5)
    # Fill in xp (green)
    d.rectangle(((25, 250), (25 + (600 * (xp / (100 * level))), 275)), fill=(0, 255, 0), outline=(0, 255, 0), width=5)
    # Draw avatar 
    # Left: 25
    # Right: 175
    # Top: 25
    # Bottom: 225
    avatarx =  requests.get(user.avatar.url, stream=True)
    avatar = Image.open(avatarx.raw)
    avatar = avatar.resize((200, 200))
    img.paste(avatar, (25, 25))
    # Draw username in Rubik
    font = ImageFont.truetype('Rubik.ttf', 50)
    # Auto-Size username
    username = user.name
    while font.getlength(username) > 400:
        font = ImageFont.truetype('Rubik.ttf', font.size - 1)
    d.text((250, 25), username, font=font, fill=(255, 255, 255))
    # Draw level in Rubik
    font = ImageFont.truetype('Rubik.ttf', 75)
    d.text((250, 100), 'Level '+str(level), font=font, fill=(255, 255, 255))


    # Save
    img.save('level'+str(user.id)+'.png')


# /level
async def level(interaction, user: discord.Member = None):
    """Shows your xp level"""
    await interaction.response.defer()
    if user is None:
        user = interaction.user
    await drawLevelCard(user, interaction.guild)
    await interaction.followup.send(file=discord.File('level'+str(user.id)+'.png'))


# Add XP Reward Role Command
async def addreward(interaction, level:int, role:discord.Role):
    """Adds a role to be given when a user reaches a certain level"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'rewards' in db[interaction.guild.id]:
        db[interaction.guild.id]['rewards'] = {}
    db[interaction.guild.id]['rewards'][role.id] = {'level': level, 'role': role.id}
    saveDb()
    await interaction.response.send_message('Added reward role **'+role.name+'** for level '+str(level)+'!')

# Remove XP Reward Role Command
async def removereward(interaction, level:int, role:discord.Role):
    """Removes a role to be given when a user reaches a certain level"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'rewards' in db[interaction.guild.id]:
        db[interaction.guild.id]['rewards'] = {}
    del db[interaction.guild.id]['rewards'][role.id]
    saveDb()
    await interaction.response.send_message('Removed reward role **'+role.name+'** for level '+str(level)+'!')

# Rewards Command
async def xp_rewards(interaction):
    """Shows all rewards"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'rewards' in db[interaction.guild.id]:
        db[interaction.guild.id]['rewards'] = {}
    embed = discord.Embed(title='Rewards', color = 0x00ff00)
    for reward in db[interaction.guild.id]['rewards']:
        embed.add_field(name=interaction.guild.get_role(db[interaction.guild.id]['rewards'][reward]['role']).name, value='Level '+str(db[interaction.guild.id]['rewards'][reward]['level']), inline=False)
    await interaction.response.send_message(embed=embed)

# Add XP Command
async def addxp(interaction, user: discord.Member, xp:int):
    """Adds xp to a user"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'xp' in db[interaction.guild.id]:
        db[interaction.guild.id]['xp'] = {}
    if not user.id in db[interaction.guild.id]['xp']:
        db[interaction.guild.id]['xp'][user.id] = {"xp": 0,"level":0}
    db[interaction.guild.id]['xp'][user.id]['xp'] += xp
    saveDb()
    await interaction.response.send_message('Added '+str(xp)+' xp to '+user.name+'!')

# Remove XP Command
async def removexp(interaction, user: discord.Member, xp:int):
    """Removes xp from a user"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'xp' in db[interaction.guild.id]:
        db[interaction.guild.id]['xp'] = {}
    if not user.id in db[interaction.guild.id]['xp']:
        db[interaction.guild.id]['xp'][user.id] = {"xp": 0,"level":0}
    db[interaction.guild.id]['xp'][user.id]['xp'] -= xp
    saveDb()
    await interaction.response.send_message('Removed '+str(xp)+' xp from '+user.name+'!')

# Leaderboard
async def xp_leaderboard(interaction):
    """Shows the xp leaderboard"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'xp' in db[interaction.guild.id]:
        db[interaction.guild.id]['xp'] = {}
    leaderboard = []
    for user in db[interaction.guild.id]['xp']:
        leaderboard.append({'id': user, 'xp': db[interaction.guild.id]['xp'][user]['xp'], 'level': db[interaction.guild.id]['xp'][user]['level']})
    leaderboard = sorted(leaderboard, key=lambda k: k['level'], reverse=True)
    embed = discord.Embed(title='XP Leaderboard', color = 0x00ff00)
    for i in range(0, min(10, len(leaderboard))):
        userxy = await client.fetch_user(leaderboard[i]['id'])
        embed.add_field(name=str(i+1)+'. '+userxy.name, value='Level '+str(leaderboard[i]['level'])+' ('+str(leaderboard[i]['xp'])+' xp)', inline=True)
    await interaction.response.send_message(embed=embed)


# Allow Free Nitro Command
@client.tree.command(name='allowfree', description='Allow free nitro for this server')
async def allowfree(interaction:discord.Interaction, allow:bool = True):
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    db[interaction.guild.id]['nitro'] = allow
    saveDb()
    await interaction.response.send_message('Free nitro has been '+('enabled' if allow else 'disabled')+' for this server!', ephemeral=True)





async def hideinvites(interaction:discord.Interaction, *, message:str):
    """Hide Discord invites in a message"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    webhook = await interaction.channel.create_webhook(name=interaction.user.name)
    # Turn off @everyone and @here
    message = message.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')
    # Find all Discord Invites
    invites = re.findall(r'(?:https?:\/\/)?(?:www\.)?(?:discord\.(?:gg|io|me|li)|discord(?:app)?\.com\/invite)\/([\w-]{2,255})', message)
    print(invites)
    # Replace all invite links with [name](invite link)
    for invite in invites:
        fetch_invite = await client.fetch_invite(invite)
        name = fetch_invite.guild.name
        oldmessage = message
        message = oldmessage.replace('http://discord.gg/'+invite, '['+name+'](https://discord.gg/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('http://discord.io/'+invite, '['+name+'](https://discord.io/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('http://discord.me/'+invite, '['+name+'](https://discord.me/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('http://discord.li/'+invite, '['+name+'](https://discord.li/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('http://discord.com/invite/'+invite, '['+name+'](https://discord.com/invite/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('http://discordapp.com/invite/'+invite, '['+name+'](https://discordapp.com/invite/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('https://discord.gg/'+invite, '['+name+'](https://discord.gg/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('https://discord.io/'+invite, '['+name+'](https://discord.io/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('https://discord.me/'+invite, '['+name+'](https://discord.me/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('https://discord.li/'+invite, '['+name+'](https://discord.li/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('https://discord.com/invite/'+invite, '['+name+'](https://discord.com/invite/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('https://discordapp.com/invite/'+invite, '['+name+'](https://discordapp.com/invite/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('discord.gg/'+invite, '['+name+'](https://discord.gg/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('discord.io/'+invite, '['+name+'](https://discord.io/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('discord.me/'+invite, '['+name+'](https://discord.me/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('discord.li/'+invite, '['+name+'](https://discord.li/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('discord.com/invite/'+invite, '['+name+'](https://discord.com/invite/'+invite+')')
        if message != oldmessage:
            continue
        message = oldmessage.replace('discordapp.com/invite/'+invite, '['+name+'](https://discordapp.com/invite/'+invite+')')
        if message != oldmessage:
            continue
    await webhook.send(message, username=interaction.user.name, avatar_url=str(interaction.user.avatar.url))
    await webhook.delete()
    await interaction.response.send_message('Message sent!', ephemeral=True)

async def get_message_from_link(link):
    # Get the message ID
    message_id = link.split('/')[-1]
    # Get the channel ID
    channel_id = link.split('/')[-2]
    # Get the guild ID
    guild_id = link.split('/')[-3]
    # Get the message
    message = await client.get_channel(int(channel_id)).fetch_message(int(message_id))
    return message

# Account Stock Generator
@app_commands.choices(account_type=[app_commands.Choice(name= 'disney', value = 'Disney+'), # Hulu
    app_commands.Choice(name= 'hulu', value = 'Hulu'), # Netflix
    app_commands.Choice(name= 'netflix', value = 'Netflix'), # Spotify
    app_commands.Choice(name= 'spotify', value = 'Spotify'), # Steam
    app_commands.Choice(name= 'steam', value = 'Steam'), # Onlyfans
    app_commands.Choice(name='onlyfans', value='Onlyfans'), # Minecraft
    app_commands.Choice(name='minecraft', value='Minecraft'), # Crunchyroll
    app_commands.Choice(name='crunchyroll', value='Crunchyroll'), # NordVPN
    app_commands.Choice(name='nordvpn', value='NordVPN'), # Pornhub
    app_commands.Choice(name='pornhub', value='Pornhub'), # Brazzers
    app_commands.Choice(name='brazzers', value='Brazzers'), # Pornhub Premium
    app_commands.Choice(name='pornhubpremium', value='Pornhub Premium'), # Brazzers Premium
    app_commands.Choice(name='brazzerspremium', value='Brazzers Premium'), # Fortnite
    app_commands.Choice(name='fortnite', value='Fortnite'), # Uplay
    app_commands.Choice(name='uplay', value='Uplay'), # Origin
    app_commands.Choice(name='origin', value='Origin'), # Battle.net
    app_commands.Choice(name='battlenet', value='Battle.net'), # Epic Games
    app_commands.Choice(name='epicgames', value='Epic Games'), # Roblox
    app_commands.Choice(name='roblox', value='Roblox'), # Amazon Prime
    app_commands.Choice(name='amazonprime', value='Amazon Prime'), # Valorant
    app_commands.Choice(name='valorant', value='Valorant'), # League of Legends
    app_commands.Choice(name='leagueoflegends', value='League of Legends'), # Apex Legends
    app_commands.Choice(name='apexlegends', value='Apex Legends'), # Call of Duty
])
async def upload_stock(interaction:discord.Interaction, account_type:str, file:discord.Attachment):
    """Upload accounts to your server stock"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    await interaction.response.defer(ephemeral=True)
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.followup.send('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'stock' in db[interaction.guild.id]:
        db[interaction.guild.id]['stock'] = {'enabled': False, 'roles': {}, 'invites': 0}
    if not db[interaction.guild.id]['stock']['enabled']:
        await interaction.followup.send('Stock is not enabled for this server!\nAsk an admin to enable it with /allowstock', ephemeral=True)
        return
    # Use serverstock list
    stockfile = open('serverstock-'+str(interaction.guild.id)+'.json', 'r')
    serverstock = json.loads(stockfile.read())
    stockfile.close()
    fileo = await file.read()
    fileo = fileo.decode('utf-8')
    acclist = fileo.splitlines()
    fixedacclist = []
    for x in acclist:
        if not ':' in x:
            continue
        fixedacclist.append(x)
    if not account_type in serverstock:
        serverstock[account_type] = fileo.splitlines()
    else:
        serverstock[account_type].extend(fileo.splitlines())
    # Replace Duplicate Accounts
    serverstock[account_type] = list(dict.fromkeys(serverstock[account_type]))
    # Save the file
    stockfile = open('serverstock-'+str(interaction.guild.id)+'.json', 'w')
    stockfile.write(json.dumps(serverstock))
    stockfile.close()
    await interaction.followup.send('Stock uploaded!', ephemeral=True)

# Set Stock Delay
async def set_stock_delay(interaction:discord.Interaction, delay:int):
    """Set the stock delay"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    await interaction.response.defer(ephemeral=True)
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.followup.send('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'stock' in db[interaction.guild.id]:
        db[interaction.guild.id]['stock'] = {'enabled': False, 'roles': {}, 'invites': 0}
    if not db[interaction.guild.id]['stock']['enabled']:
        await interaction.followup.send('Stock is not enabled for this server!\nAsk an admin to enable it with /allowstock', ephemeral=True)
        return
    db[interaction.guild.id]['stock']['delay'] = delay
    await interaction.followup.send('Stock delay set to '+str(delay)+' seconds!', ephemeral=True)

async def allowstock(interaction:discord.Interaction, allow:bool = True):
    """Allow server stock for this server"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'stock' in db[interaction.guild.id]:
        db[interaction.guild.id]['stock'] = {'enabled': False, 'roles': {}, 'invites': 0}
    db[interaction.guild.id]['stock']['enabled'] = allow
    saveDb()
    open('serverstock-'+str(interaction.guild.id)+'.json', 'w').write('{}')
    await interaction.response.send_message('Server stock has been '+('enabled' if allow else 'disabled')+' for this server!', ephemeral=True)

lastGenerated = {

}

# Generate Account

@app_commands.choices(account_type=[app_commands.Choice(name= 'disney', value = 'Disney+'), # Hulu
    app_commands.Choice(name= 'hulu', value = 'Hulu'), # Netflix
    app_commands.Choice(name= 'netflix', value = 'Netflix'), # Spotify
    app_commands.Choice(name= 'spotify', value = 'Spotify'), # Steam
    app_commands.Choice(name= 'steam', value = 'Steam'), # Onlyfans
    app_commands.Choice(name='onlyfans', value='Onlyfans'), # Minecraft
    app_commands.Choice(name='minecraft', value='Minecraft'), # Crunchyroll
    app_commands.Choice(name='crunchyroll', value='Crunchyroll'), # NordVPN
    app_commands.Choice(name='nordvpn', value='NordVPN'), # Pornhub
    app_commands.Choice(name='pornhub', value='Pornhub'), # Brazzers
    app_commands.Choice(name='brazzers', value='Brazzers'), # Pornhub Premium
    app_commands.Choice(name='pornhubpremium', value='Pornhub Premium'), # Brazzers Premium
    app_commands.Choice(name='brazzerspremium', value='Brazzers Premium'), # Fortnite
    app_commands.Choice(name='fortnite', value='Fortnite'), # Uplay
    app_commands.Choice(name='uplay', value='Uplay'), # Origin
    app_commands.Choice(name='origin', value='Origin'), # Battle.net
    app_commands.Choice(name='battlenet', value='Battle.net'), # Epic Games
    app_commands.Choice(name='epicgames', value='Epic Games'), # Roblox
    app_commands.Choice(name='roblox', value='Roblox'), # Amazon Prime
    app_commands.Choice(name='amazonprime', value='Amazon Prime'), # Valorant
    app_commands.Choice(name='valorant', value='Valorant'), # League of Legends
    app_commands.Choice(name='leagueoflegends', value='League of Legends'), # Apex Legends
    app_commands.Choice(name='apexlegends', value='Apex Legends'), # Call of Duty
])
async def generate(interaction:discord.Interaction, account_type:str):
    """Generate an account"""
    # Cooldown
    if not interaction.guild.id in lastGenerated:
        lastGenerated[interaction.guild.id] = {}
    if not interaction.user.id in lastGenerated[interaction.guild.id]:
        lastGenerated[interaction.guild.id][interaction.user.id] = 0
    if not 'delay' in db[interaction.guild.id]['stock']:
        db[interaction.guild.id]['stock']['delay'] = 0
    if time.time() - lastGenerated[interaction.guild.id][interaction.user.id] < db[interaction.guild.id]['stock']['delay']:
        await interaction.response.send_message('You are on cooldown! Please wait '+str(round(db[interaction.guild.id]['stock']['delay'] - (time.time() - lastGenerated[interaction.guild.id][interaction.user.id]), 2))+' seconds before generating again!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'stock' in db[interaction.guild.id]:
        db[interaction.guild.id]['stock'] = {'enabled': False, 'roles': {}, 'invites': 0}
    if not db[interaction.guild.id]['stock']['enabled']:
        await interaction.response.send_message('Stock is not enabled for this server!\nAsk an admin to enable it with /allowstock', ephemeral=True)
        return
    hasRequiredRole = False
    if not account_type in db[interaction.guild.id]['stock']['roles']:
        hasRequiredRole = True
    else:
        for member in interaction.guild.members:
            if member.id == interaction.user.id:
                for role in member.roles:
                    if role.id == db[interaction.guild.id]['stock']['roles'][account_type]:
                        hasRequiredRole = True
                        break
    if not hasRequiredRole:
        await interaction.response.send_message('You need the role '+interaction.guild.get_role(db[interaction.guild.id]['stock']['roles'][account_type]).mention+' to generate this account!', ephemeral=True)
        return
    # Use serverstock list
    stockfile = open('serverstock-'+str(interaction.guild.id)+'.json', 'r')
    serverstock = json.loads(stockfile.read())
    stockfile.close()
    if not account_type in serverstock:
        await interaction.response.send_message('No stock for this account type!', ephemeral=True)
        return
    if len(serverstock[account_type]) == 0:
        await interaction.response.send_message('No stock for this account type!', ephemeral=True)
        return
    account = random.choice(serverstock[account_type])
    serverstock[account_type].remove(account)
    stockfile = open('serverstock-'+str(interaction.guild.id)+'.json', 'w')
    stockfile.write(json.dumps(serverstock))
    stockfile.close()
    email = account.split(':')[0]
    password = account.split(':')[1].split('|')[0]
    info = ''
    if len(account.split(':')[1].split('|')) > 1:
        info = account.split(':')[1].split('|')[1]
    embed = discord.Embed(title=account_type+' Account Generator', description = 'Here is your account!', color=0x00ff00)
    embed.add_field(name='Email', value=email, inline=False)
    embed.add_field(name='Password', value=password, inline=False)
    if info != '':
        embed.add_field(name='Info', value=info, inline=False)
    await interaction.response.send_message('Generated '+account_type+' account for '+interaction.user.mention)
    await interaction.followup.send(embed=embed, ephemeral=True)
    lastGenerated[interaction.guild.id][interaction.user.id] = time.time()

# Stock info
async def showstock(interaction:discord.Interaction):
    """Get stock info"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'stock' in db[interaction.guild.id]:
        db[interaction.guild.id]['stock'] = {'enabled': False, 'roles': {}, 'invites': 0}
    if not db[interaction.guild.id]['stock']['enabled']:
        await interaction.response.send_message('Stock is not enabled for this server!\nAsk an admin to enable it with /allowstock', ephemeral=True)
        return
    # Use serverstock list
    stockfile = open('serverstock-'+str(interaction.guild.id)+'.json', 'r')
    serverstock = json.loads(stockfile.read())
    stockfile.close()
    embed = discord.Embed(title='Stock Info', description = 'Here is your stock info!', color=0x00ff00)
    for account_type in serverstock:
        embed.add_field(name=account_type, value=str(len(serverstock[account_type])) + ' accounts', inline=True)
    await interaction.response.send_message(embed=embed)

# Set stock role
@app_commands.choices(account_type=[app_commands.Choice(name= 'disney', value = 'Disney+'), # Hulu
    app_commands.Choice(name= 'hulu', value = 'Hulu'), # Netflix
    app_commands.Choice(name= 'netflix', value = 'Netflix'), # Spotify
    app_commands.Choice(name= 'spotify', value = 'Spotify'), # Steam
    app_commands.Choice(name= 'steam', value = 'Steam'), # Onlyfans
    app_commands.Choice(name='onlyfans', value='Onlyfans'), # Minecraft
    app_commands.Choice(name='minecraft', value='Minecraft'), # Crunchyroll
    app_commands.Choice(name='crunchyroll', value='Crunchyroll'), # NordVPN
    app_commands.Choice(name='nordvpn', value='NordVPN'), # Pornhub
    app_commands.Choice(name='pornhub', value='Pornhub'), # Brazzers
    app_commands.Choice(name='brazzers', value='Brazzers'), # Pornhub Premium
    app_commands.Choice(name='pornhubpremium', value='Pornhub Premium'), # Brazzers Premium
    app_commands.Choice(name='brazzerspremium', value='Brazzers Premium'), # Fortnite
    app_commands.Choice(name='fortnite', value='Fortnite'), # Uplay
    app_commands.Choice(name='uplay', value='Uplay'), # Origin
    app_commands.Choice(name='origin', value='Origin'), # Battle.net
    app_commands.Choice(name='battlenet', value='Battle.net'), # Epic Games
    app_commands.Choice(name='epicgames', value='Epic Games'), # Roblox
    app_commands.Choice(name='roblox', value='Roblox'), # Amazon Prime
    app_commands.Choice(name='amazonprime', value='Amazon Prime'), # Valorant
    app_commands.Choice(name='valorant', value='Valorant'), # League of Legends
    app_commands.Choice(name='leagueoflegends', value='League of Legends'), # Apex Legends
    app_commands.Choice(name='apexlegends', value='Apex Legends'), # Call of Duty
])
async def setstockrole(interaction:discord.Interaction, account_type:str, role:discord.Role):
    """Set stock role"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'stock' in db[interaction.guild.id]:
        db[interaction.guild.id]['stock'] = {'enabled': False, 'roles': {}, 'invites': 0}
    if not db[interaction.guild.id]['stock']['enabled']:
        await interaction.response.send_message('Stock is not enabled for this server!\nAsk an admin to enable it with /allowstock', ephemeral=True)
        return
    db[interaction.guild.id]['stock']['roles'][account_type] = role.id
    saveDb()
    await interaction.response.send_message('Stock role set!', ephemeral=True)

# Remove stock role
@app_commands.choices(account_type=[app_commands.Choice(name= 'disney', value = 'Disney+'), # Hulu
    app_commands.Choice(name= 'hulu', value = 'Hulu'), # Netflix
    app_commands.Choice(name= 'netflix', value = 'Netflix'), # Spotify
    app_commands.Choice(name= 'spotify', value = 'Spotify'), # Steam
    app_commands.Choice(name= 'steam', value = 'Steam'), # Onlyfans
    app_commands.Choice(name='onlyfans', value='Onlyfans'), # Minecraft
    app_commands.Choice(name='minecraft', value='Minecraft'), # Crunchyroll
    app_commands.Choice(name='crunchyroll', value='Crunchyroll'), # NordVPN
    app_commands.Choice(name='nordvpn', value='NordVPN'), # Pornhub
    app_commands.Choice(name='pornhub', value='Pornhub'), # Brazzers
    app_commands.Choice(name='brazzers', value='Brazzers'), # Pornhub Premium
    app_commands.Choice(name='pornhubpremium', value='Pornhub Premium'), # Brazzers Premium
    app_commands.Choice(name='brazzerspremium', value='Brazzers Premium'), # Fortnite
    app_commands.Choice(name='fortnite', value='Fortnite'), # Uplay
    app_commands.Choice(name='uplay', value='Uplay'), # Origin
    app_commands.Choice(name='origin', value='Origin'), # Battle.net
    app_commands.Choice(name='battlenet', value='Battle.net'), # Epic Games
    app_commands.Choice(name='epicgames', value='Epic Games'), # Roblox
    app_commands.Choice(name='roblox', value='Roblox'), # Amazon Prime
])
async def removestockrole(interaction:discord.Interaction, account_type:str):
    """Remove stock role"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'stock' in db[interaction.guild.id]:
        db[interaction.guild.id]['stock'] = {'enabled': False, 'roles': {}, 'invites': 0}
    if not db[interaction.guild.id]['stock']['enabled']:
        await interaction.response.send_message('Stock is not enabled for this server!\nAsk an admin to enable it with /allowstock', ephemeral=True)
        return
    if not account_type in db[interaction.guild.id]['stock']['roles']:
        await interaction.response.send_message('No stock role set for this account type!', ephemeral=True)
        return
    del db[interaction.guild.id]['stock']['roles'][account_type]
    saveDb()
    await interaction.response.send_message('Stock role removed!', ephemeral=True)




# Reaction Roles
async def addreactionrole(interaction:discord.Interaction, message_link:str, emoji:str, role:discord.Role):
    """Add a reaction role to a message"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.manage_roles:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    try:
        message = await get_message_from_link(message_link)
    except:
        await interaction.response.send_message('Invalid message link!', ephemeral=True)
        return
    if not emojilib.is_emoji(emoji):
        await interaction.response.send_message('Invalid emoji!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'reactionroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['reactionroles'] = {}
    if not message.id in db[interaction.guild.id]['reactionroles']:
        db[interaction.guild.id]['reactionroles'][message.id] = {}
    db[interaction.guild.id]['reactionroles'][message.id][emoji] = role.id
    saveDb()
    await message.add_reaction(emoji)
    await interaction.response.send_message('Reaction role added!', ephemeral=True)

# Reaction Roles
async def removereactionrole(interaction:discord.Interaction, message_link:str, emoji:str):
    """Remove a reaction role from a message"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.manage_roles:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    try:
        message = await get_message_from_link(message_link)
    except:
        await interaction.response.send_message('Invalid message link!', ephemeral=True)
        return
    if not emojilib.is_emoji(emoji):
        await interaction.response.send_message('Invalid emoji!', ephemeral=True)
        return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    if not 'reactionroles' in db[interaction.guild.id]:
        db[interaction.guild.id]['reactionroles'] = {}
    if not message.id in db[interaction.guild.id]['reactionroles']:
        db[interaction.guild.id]['reactionroles'][message.id] = {}
    if not emoji in db[interaction.guild.id]['reactionroles'][message.id]:
        await interaction.response.send_message('This reaction role does not exist!', ephemeral=True)
        return
    del db[interaction.guild.id]['reactionroles'][message.id][emoji]
    saveDb()
    await message.remove_reaction(emoji, client.user)
    await interaction.response.send_message('Reaction role removed!', ephemeral=True)

# Button Roles


# Reaction Roles - on_raw_reaction_add
@client.event
async def on_raw_reaction_add(payload:discord.RawReactionActionEvent):
    if not payload.guild_id in db:
        return
    if not is_premium(payload.guild_id):
        return
    if not 'reactionroles' in db[payload.guild_id]:
        return
    if not payload.message_id in db[payload.guild_id]['reactionroles']:
        return
    if not str(payload.emoji) in db[payload.guild_id]['reactionroles'][payload.message_id]:
        return
    guild = client.get_guild(payload.guild_id)
    role = guild.get_role(db[payload.guild_id]['reactionroles'][payload.message_id][str(payload.emoji)])
    member = guild.get_member(payload.user_id)
    await member.add_roles(role)

# Reaction Roles - on_raw_reaction_remove
@client.event
async def on_raw_reaction_remove(payload:discord.RawReactionActionEvent):
    if not payload.guild_id in db:
        return
    if not is_premium(payload.guild_id):
        return
    if not 'reactionroles' in db[payload.guild_id]:
        return
    if not payload.message_id in db[payload.guild_id]['reactionroles']:
        return
    if not str(payload.emoji) in db[payload.guild_id]['reactionroles'][payload.message_id]:
        return
    guild = client.get_guild(payload.guild_id)
    role = guild.get_role(db[payload.guild_id]['reactionroles'][payload.message_id][str(payload.emoji)])
    member = guild.get_member(payload.user_id)
    await member.remove_roles(role)

@app_commands.choices(typeof=[app_commands.Choice(name = 'Anime', value='anime'),app_commands.Choice(name = 'Manga', value='manga'),app_commands.Choice(name = 'Pokemon', value='pokemon'),app_commands.Choice(name = 'Urban', value='urban')])
async def search(interaction:discord.Interaction, *, query:str, typeof:str = 'urban'):
    if typeof == 'urban':
        base_url = 'http://api.urbandictionary.com/v0/define?term='
        url = base_url + query
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if not data['list']:
                    await interaction.response.send_message('No results found!', ephemeral=True)
                    return
                choice = random.choice(data['list'])
                embed = discord.Embed(title=choice['word'], description=choice['definition'].replace('[','').replace(']',''), color=0x00ff00)
                embed.add_field(name='Example', value=choice['example'].replace('[','').replace(']',''))
                embed.add_field(name='Author', value=choice['author'].replace('[','').replace(']',''))
                embed.add_field(name='Rating', value=choice['thumbs_up'])
                embed.set_footer(text='Powered by Urban Dictionary')
                await interaction.response.send_message(embed=embed)
    elif typeof == 'anime':
        base_url = 'https://kitsu.io/api/edge/anime?filter[text]='
        url = base_url + query
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if not data['data']:
                    await interaction.response.send_message('No results found!', ephemeral=True)
                    return
                choice = random.choice(data['data'])
                embed = discord.Embed(title=choice['attributes']['canonicalTitle'], description=choice['attributes']['synopsis'], color=0x00ff00)
                embed.add_field(name='Rating', value=choice['attributes']['averageRating'])
                embed.add_field(name='Status', value=choice['attributes']['status'])
                embed.add_field(name='Episodes', value=choice['attributes']['episodeCount'])
                embed.set_image(url=choice['attributes']['posterImage']['original'])
                embed.set_footer(text='Powered by Kitsu')
                await interaction.response.send_message(embed=embed)
    elif typeof == 'manga':
        base_url = 'https://kitsu.io/api/edge/manga?filter[text]='
        url = base_url + query
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if not data['data']:
                    await interaction.response.send_message('No results found!', ephemeral=True)
                    return
                choice = random.choice(data['data'])
                embed = discord.Embed(title=choice['attributes']['canonicalTitle'], description=choice['attributes']['synopsis'], color=0x00ff00)
                embed.add_field(name='Rating', value=choice['attributes']['averageRating'])
                embed.add_field(name='Status', value=choice['attributes']['status'])
                embed.add_field(name='Episodes', value=choice['attributes']['chapterCount'])
                embed.set_image(url=choice['attributes']['posterImage']['original'])
                embed.set_footer(text='Powered by Kitsu')
                await interaction.response.send_message(embed=embed)
    elif typeof == 'pokemon':
        base_url = 'https://pokeapi.co/api/v2/pokemon/'
        url = base_url + query
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                try:
                    data = await response.json()
                except:
                    await interaction.response.send_message('No results found!', ephemeral=True)
                    return
                if not data:
                    await interaction.response.send_message('No results found!', ephemeral=True)
                    return
                embed = discord.Embed(title=data['name'], color=0x00ff00)
                embed.add_field(name='Height', value=data['height'])
                embed.add_field(name='Weight', value=data['weight'])
                embed.add_field(name='Base Experience', value=data['base_experience'])
                embed.set_image(url=data['sprites']['front_default'])
                embed.set_footer(text='Powered by PokeAPI')
                await interaction.response.send_message(embed=embed)

# Message on boost
@client.event
async def on_member_update(before, after):
    if before.premium_since == after.premium_since:
        return
    if not after.premium_since:
        return
    if not is_premium(after.guild.id):
        return
    if not 'boostmessage' in db[after.guild.id]:
        return
    channel = client.get_channel(db[after.guild.id]['boostmessage']['channel'])
    await channel.send(db[after.guild.id]['boostmessage']['message'].replace('{user}', after.mention))


async def setboostchance(interaction:discord.Interaction, chance:int):
    # Check if premium
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.manage_guild:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    # Check if chance is valid
    if chance < 1 or chance > 100:
        await interaction.response.send_message('The chance must be between 1 and 100!', ephemeral=True)
        return
    # Set chance
    db[interaction.guild.id]['booster_chance'] = chance
    saveDb()
    await interaction.response.send_message('Successfully set the booster chance to '+str(chance)+'x!', ephemeral=True)

# Set boost message
async def setboostmessage(interaction:discord.Interaction, channel:discord.TextChannel, *, message:str):
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        return
    db[interaction.guild.id]['boostmessage'] = {'channel':channel.id, 'message':message}
    await interaction.response.send_message('Successfully set the boost message!', ephemeral=True)
    saveDb()


async def img(interaction:discord.Interaction, *, text:str):
    try:
        # https://lexica.art/api/v1/search?q=an%20epic%20fantasy%20comic%20book%20style%20portrait%20painting%20of%20an%20extremely%20cute%20and%20adorable%20very%20beautiful%20furby,%20unreal%205,%20daz,%20hyperrealistic,%20octane%20render,%20cosplay,%20rpg%20portrait,%20dynamic%20lighting,%20intricate%20detail,%20summer%20vibrancy,%20cinematic
        # Response: images: [{id: "10947e41-9ae6-4800-8b18-94f24ea85ae6",…}, {id: "135f96c7-97f9-4178-b594-a7843ca195c2",…},…]
        # https://lexica-serve-encoded-images.sharif.workers.dev/md/10947e41-9ae6-4800-8b18-94f24ea85ae6
        await interaction.response.defer(thinking=True)
        headers = {
            'authority': 'lexica.art',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,it;q=0.8',
            'origin': 'https://www.craiyon.com',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        }
        params = (
            ('q', text),
        )
        req = await AsyncClient.get('https://lexica.art/api/v1/search', headers=headers, params=params)
        print('x')
        im64 = req.json()['images'][random.randint(0, len(req.json()['images'])-1)]['id']
        req = await AsyncClient.get('https://lexica-serve-encoded-images.sharif.workers.dev/md/'+im64)
        print('y')
        d = Image.open(BytesIO(req.content))
        d.save('image-'+str(interaction.user.id)+'.png', 'PNG')
        webhook = interaction.followup
        # Check nsfw
        url = "https://nsfw-images-detection-and-classification.p.rapidapi.com/adult-content"
        payload = {"url": "https://lexica-serve-encoded-images.sharif.workers.dev/md/"+im64}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "4a0f1502c4msh6d8597e31d37664p1ce430jsn50123a1b9045",
            "X-RapidAPI-Host": "nsfw-images-detection-and-classification.p.rapidapi.com"
        }
        response = await AsyncClient.request("POST", url, json=payload, headers=headers)
        print(response.text)
        if response.json()['unsafe'] and not interaction.channel.id == 1076238910293807134:
            # blur image
            d = d.filter(ImageFilter.GaussianBlur(radius=15))
            # Add caption to the bottom
            caption_text = "Not safe for work"
            caption_font = ImageFont.truetype("Rubik.ttf", 50)
            caption_width, caption_height = caption_font.getsize(caption_text)
            caption = Image.new('RGBA', (caption_width, caption_height), (0, 0, 0, 0))
            caption_draw = ImageDraw.Draw(caption)
            caption_draw.text((0, 0), caption_text, font=caption_font, fill=(255, 255, 255, 255))
            d.paste(caption, (0, d.height - caption_height), caption)
            d.save('image-'+str(interaction.user.id)+'.png', 'PNG')
        x = True
        await webhook.send(file = discord.File('image-'+str(interaction.user.id)+'.png'))
    except Exception as es:
        print(es)
        await interaction.followup.send('Error, please try again later')

async def face(interaction:discord.Interaction):
    '''Generate a random human face'''
    await interaction.response.defer(thinking=True)
    # using this-person-does-not-exist.com
    url = "https://this-person-does-not-exist.com/en?new=1669210012142"
    req = await AsyncClient.get('https://this-person-does-not-exist.com/en?new=1669210012142')
    if req.status_code == 200:
        data = req.json()
        print(data)
        name = data['name']
        # https://this-person-does-not-exist.com/img/ + name
        url = "https://this-person-does-not-exist.com/img/" + name
        # Download + send
        req = await AsyncClient.get(url)
        #save to file
        with open('image-'+str(interaction.user.id)+'.png', 'wb') as f:
            f.write(req.content)
        #send
        await interaction.followup.send(file = discord.File('image-'+str(interaction.user.id)+'.png'))
        




        return
    else:
        await interaction.followup.send('Error, please try again later')


# MEME
async def random_meme(interaction:discord.Interaction):
    '''Get a random meme'''
    # Using the randommeme api: https://meme-api.herokuapp.com/gimme
    await interaction.response.defer()
    meme_context = await AsyncClient.get('https://meme-api.herokuapp.com/gimme')
    meme_data = meme_context.json()
    meme_image_url = meme_data['url']
    meme_title = meme_data['title']
    meme_author = meme_data['author']
    meme_link = meme_data['postLink']
    # Build embed
    embed = discord.Embed(title=meme_title, description=meme_author, color=discord.Color.random())
    embed.set_image(url=meme_image_url)
    embed.url = meme_link
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
    await interaction.followup.send(embed=embed)

async def create_meme(interaction:discord.Interaction, top_text:str, bottom_text: str, img_url: str):
    '''
    Creates a meme
    
    Parameters
    ----------
    top_text:str
        Text to display on the top of the meme
    bottom_text:str
        Text to display on the bottom of the meme
    img_url:str
        Url of the meme background image
    '''
    # Using Memebuild
    await interaction.response.defer()

    json = {
        'imgUrl': img_url,
        'topText': top_text,
        'bottomText': bottom_text
    }
    x = await AsyncClient.post('https://memebuild.com/api/1.0/generateMeme?api-key=ae6c84212074062f125424c11ff3e7', data=json)
    x = x.json()
    # get 'url' from json as image_url
    image_url = x['url']
    # build embed
    embed = discord.Embed(title='Here is your meme', color=discord.Color.random())
    embed.set_image(url=image_url)
    embed.url = image_url
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    await interaction.followup.send(embed=embed)
    

async def review(interaction:discord.Interaction, website_url:str):
    await interaction.response.defer(thinking=True)
    # webscore.ai
    # Check for url regex https://, otherwhise make it the regex
    if not re.match(r'^https?://', website_url):
        website_url = 'https://'+website_url
    try:
        cookies = {
            '__ddg1_': '6nDaMmCDmDN3Fe0lHy0r',
            '_ga': 'GA1.2.198196475.1661012071',
            '_ym_uid': '166101207184810433',
            '_ym_d': '1661012071',
            '_hjSessionUser_841384': 'eyJpZCI6ImRkMTJjYzFjLTVhODktNWExNC04NzIzLTIyMmUyZjE5OWI5MyIsImNyZWF0ZWQiOjE2NjEwMTIwNzEzNDksImV4aXN0aW5nIjp0cnVlfQ==',
            '_gid': 'GA1.2.1643910168.1665510571',
            '_ym_isad': '2',
            '_gat_UA-113701760-1': '1',
            '_ym_visorc': 'w',
            '_hjIncludedInSessionSample': '1',
            '_hjSession_841384': 'eyJpZCI6IjY3Yzg1Yzg2LTFjN2ItNDBkYi05ZDU3LWMxYjg3NTU2MmQ5ZiIsImNyZWF0ZWQiOjE2NjU1MTMyMDYyMTIsImluU2FtcGxlIjp0cnVlfQ==',
            '_hjIncludedInPageviewSample': '1',
            '_hjAbsoluteSessionInProgress': '0',
        }

        headers = {
            'authority': 'webscore.ai',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,it;q=0.8',
            # Already added when you pass json=
            # 'content-type': 'application/json',
            # requests sorts cookies= alphabetically
            # 'cookie': '__ddg1_=6nDaMmCDmDN3Fe0lHy0r; _ga=GA1.2.198196475.1661012071; _ym_uid=166101207184810433; _ym_d=1661012071; _hjSessionUser_841384=eyJpZCI6ImRkMTJjYzFjLTVhODktNWExNC04NzIzLTIyMmUyZjE5OWI5MyIsImNyZWF0ZWQiOjE2NjEwMTIwNzEzNDksImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1643910168.1665510571; _ym_isad=2; _gat_UA-113701760-1=1; _ym_visorc=w; _hjIncludedInSessionSample=1; _hjSession_841384=eyJpZCI6IjY3Yzg1Yzg2LTFjN2ItNDBkYi05ZDU3LWMxYjg3NTU2MmQ5ZiIsImNyZWF0ZWQiOjE2NjU1MTMyMDYyMTIsImluU2FtcGxlIjp0cnVlfQ==; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0',
            'origin': 'https://webscore.ai',
            'referer': 'https://webscore.ai/history',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }

        params = {
            'uuid': str(random.randint(1000000000,99999999999)),
        }

        json_data = {
            'url': website_url,
            'locale': 'en',
        }

        response = await AsyncClient.post('https://webscore.ai/api/parse', params=params, cookies=cookies, headers=headers, json=json_data)
        print(response.json())
        webid = response.json()[1]['id']
        webstatus = response.json()[1]['status']
        while webstatus == 'pending':
            req = await AsyncClient.get('https://webscore.ai/api/task/'+webid, params=params, cookies=cookies, headers=headers)
            print(response.json())
            webstatus = req.json()[1]['status']
            await asyncio.sleep(1)
        if webstatus == 'fulfilled':
            rate = req.json()[1]['rate']
            if rate >=8:
                await interaction.followup.send('This website is really great, most can\'t do better than this!')
            elif rate >=6:
                await interaction.followup.send('This website is good, but it can be better!')
            elif rate >=4:
                await interaction.followup.send('This website is not bad, but it can be better!')
            elif rate >=2:
                await interaction.followup.send('This website is not that good it could be!')
            elif rate >=0:
                await interaction.followup.send('This website is really bad, it needs to be improved!')
            else:
                await interaction.followup.send('This website is really bad, it needs to be improved!')
        else:
            await interaction.followup.send('Error, please try again later!')

    except Exception as es:
        print(es)
        await interaction.followup.send('Error, please try again later')



# Allow Bypass Bot Command
@app_commands.guild_only()
async def allowbypass(interaction:discord.Interaction, user: discord.Member):
    """Allow bot to bypass anti-nuke system"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
    if not interaction.guild.id in allowed_bots:
        allowed_bots[interaction.guild.id] = []
    if user.id in allowed_bots[interaction.guild.id]:
        await interaction.response.send_message("This bot is already allowed to bypass the anti-nuke system", ephemeral=True)
    else:
        allowed_bots[interaction.guild.id].append(client.id)
        await interaction.response.send_message("This bot is now allowed to bypass the anti-nuke system", ephemeral=True)
    open("allowed_bots.py", "w").write(f"allowed_bots = {allowed_bots}")

# Disallow Bypass Bot Command
@app_commands.guild_only()
async def disallowbypass(interaction:discord.Interaction, bot: discord.Member):
    """Disallow bot to bypass anti-nuke system"""
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
    if client.bot:
        if not interaction.guild.id in allowed_bots:
            allowed_bots[interaction.guild.id] = []
        if client.id in allowed_bots[interaction.guild.id]:
            allowed_bots[interaction.guild.id].remove(client.id)
            await interaction.response.send_message("This bot is now disallowed to bypass the anti-nuke system", ephemeral=True)
        else:
            await interaction.response.send_message("This bot is already disallowed to bypass the anti-nuke system", ephemeral=True)
    else:
        await interaction.response.send_message("This is not a bot", ephemeral=True)
    open("allowed_bots.py", "w").write(f"allowed_bots = {allowed_bots}")

# Check Shop Website if its legit
async def checkshop(interaction:discord.Interaction, website_url:str):
    """Check if the shop website is legit
    
    Parameters
    ----------
    website_url : str
        The website url to check"""
    website_domain = website_url.split('/')[2]
    req = await AsyncClient.get('https://scamdetector.net/check/'+website_domain)
    # h1 - class: text-center
    soup = BeautifulSoup(req.text, 'html.parser')
    h1 = soup.find('h1', {'class': 'text-center'})
    # Is the word scam in the h1?
    if 'scam' in h1.text.lower():
        await interaction.response.send_message('This shopping website seems to be a scam, if it is a shop.\nChecked using scamdetector.net', ephemeral=True)
    else:
        await interaction.response.send_message('This shopping website seems to be legit, if it is a shop.\nChecked using scamdetector.net', ephemeral=True)

# Send message as another user

@app_commands.guild_only()
async def sendas(interaction:discord.Interaction, user: discord.Member, message: str):
    """Send a message as another user

    Parameters
    ----------
    user : discord.Member
        The user to send the message as
    message : str
        The message to send"""
    # defer
    await interaction.response.defer(ephemeral=True)
    if not is_premium(interaction.guild.id):
        await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(user.id, interaction.guild.id), ephemeral=True)
        return
    # Don't allow send as themselves
    if user.id == interaction.user.id:
        await interaction.response.send_message("Just send the message normally :facepalm:", ephemeral=True)
        return
    
    # Create webhook in channel
    webhook = await interaction.channel.create_webhook(name=user.display_name)
    # Send message + file
    await webhook.send(content=message, username=user.display_name, avatar_url=user.display_avatar.url)





def scan_url(website_url):
    print(website_url)
    headers = {
        'authority': 'sitecheck.sucuri.net',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,it;q=0.8',
        # requests sorts cookies= alphabetically
        # 'cookie': f"CONSENTMGR=c1:1%7Cc2:1%7Cc3:1%7Cc4:1%7Cc5:1%7Cc6:1%7Cc7:1%7Cc8:1%7Cc9:1%7Cc10:1%7Cc11:1%7Cc12:1%7Cc13:1%7Cc14:1%7Cc15:1%7Cts:1663660983347%7Cconsent:true; _fbp=fb.1.1663660983596.925159774; _ga=GA1.2.2043274442.1663660984; _gid=GA1.2.1504979093.1663660984; IR_gbd=sucuri.net; _gat_gtag_UA_4077922_18=1; wcsid=4iotHUac1hz5eDOe179Br0NAo6BraA0j; hblid=aV98SQ5d8mU1Rt8T179Br0No6B6aboAA; IR_PI=a7369d0b-38ba-11ed-a9bd-6518b0927617%7C1663747383709; olfsk=olfsk9405428007746601; _ok=5005-531-10-9691; _okbk=cd5%3Davailable%2Ccd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1663660985039%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; __hstc=166519265.146a5f87d26a04ef1e3e9b37b633ba46.1663660985207.1663660985207.1663660985207.1; hubspotutk=146a5f87d26a04ef1e3e9b37b633ba46; __hssrc=1; _gat=1; utag_main=v_id:018359ec0435005b6b1c4bb0cf340506f003806700bd0{_sn:1$_ss:0$_st:1663662836823$ses_id:1663660983351%3Bexp-session$_pn:2%3Bexp-session;} mp_c59343135653bd9019d29f1db79e348b_mixpanel=%7B%22distinct_id%22%3A%20%2218359ec049366-0bb99a7b3cecb4-26021c51-1fa400-18359ec0494806%22%2C%22%24device_id%22%3A%20%2218359ec049366-0bb99a7b3cecb4-26021c51-1fa400-18359ec0494806%22%2C%22%24search_engine%22%3A%20%22bing%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.bing.com%22%7D; IR_3713=1663661036933%7C1304864%7C1663660983709%7C%7C; _oklv=1663661037053%2C4iotHUac1hz5eDOe179Br0NAo6BraA0j; _okdetect=%7B%22token%22%3A%2216636610372470%22%2C%22proto%22%3A%22about%3A%22%2C%22host%22%3A%22%22%7D; __hssc=166519265.2.1663660985208; _ga=GA1.3.2043274442.1663660984; _gid=GA1.3.1504979093.1663660984; _okgid=45391cb1f368baf79eea4d5fb81dba58",
        'referer': 'https://sitecheck.sucuri.net/',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }

    params = {
        'scan': website_url,
    }

    response = requests.get('https://sitecheck.sucuri.net/api/v3/', params=params, headers=headers)
    print(response.json())
    return response.json()['ratings']['total']['rating']

# Scan malware on website
@client.tree.command(name="scan", description="Scan for malware on a website")
async def scan(interaction:discord.Interaction, website_url:str):
    """Scan for malware on a website"""
    await interaction.response.defer(thinking=True)
    webstatus = scan_url(website_url)
    if webstatus == 'A':
        await interaction.followup.send('This website seems to be safe. (Minimal Risk)', ephemeral=True)
    elif webstatus == 'B':
        await interaction.followup.send('This website seems to be safe. (Low Risk)', ephemeral=True)
    elif webstatus == 'C':
        await interaction.followup.send('This website seems to be safe. (Medium Risk)', ephemeral=True)
    elif webstatus == 'D':
        await interaction.followup.send('This website seems to be unsafe. (High Risk)', ephemeral=True)
    elif webstatus == 'E':
        await interaction.followup.send('This website seems to be unsafe. (Very High Risk)', ephemeral=True)

# Server Stats

async def setmembers(interaction, name:str = None):
    """Set the member count to a voice channel"""
    await interaction.response.defer(ephemeral=True)
    if name is None:
        name = 'Members: {count}'
    # Create private voice channel
    members = await interaction.guild.chunk()
    channel = await interaction.guild.create_voice_channel(name.replace('{count}', str(len(members))), category=interaction.channel.category)
    await channel.set_permissions(interaction.guild.default_role, connect=False)
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'stats' in db[interaction.guild.id]:
        db[interaction.guild.id]['stats'] = {}
    if not 'members' in db[interaction.guild.id]['stats']:
        db[interaction.guild.id]['stats']['members'] = {}
    db[interaction.guild.id]['stats']['members']['channel'] = channel.id
    db[interaction.guild.id]['stats']['members']['name'] = name
    saveDb()
    await interaction.followup.send('Check the channel ' + channel.mention + ' for the member count.', ephemeral=True)

async def setbots(interaction, name:str = None):
    """Set the bot count to a voice channel"""
    await interaction.response.defer(ephemeral=True)
    if name is None:
        name = 'Bots: {count}'
    # Create private voice channel
    members = await interaction.guild.chunk()
    channel = await interaction.guild.create_voice_channel(name, category=interaction.channel.category)
    await channel.set_permissions(interaction.guild.default_role, connect=False)
    await channel.edit(name=name.replace('{count}', str(len([m for m in members if m.bot]))))
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'stats' in db[interaction.guild.id]:
        db[interaction.guild.id]['stats'] = {}
    if not 'bots' in db[interaction.guild.id]['stats']:
        db[interaction.guild.id]['stats']['bots'] = {}
    db[interaction.guild.id]['stats']['bots']['channel'] = channel.id
    db[interaction.guild.id]['stats']['bots']['name'] = name
    saveDb()
    await interaction.followup.send('Check the channel ' + channel.mention + ' for the bot count.', ephemeral=True)

async def setonline(interaction, name:str = None):
    """Set the online count to a voice channel"""
    await interaction.response.defer(ephemeral=True)
    if name is None:
        name = 'Online: {count}'
    members = await interaction.guild.chunk()
    # Create private voice channel
    channel = await interaction.guild.create_voice_channel(name, category=interaction.channel.category)
    await channel.set_permissions(interaction.guild.default_role, connect=False)
    await channel.edit(name=name.replace('{count}', str(len([m for m in members if m.status != discord.Status.offline]))))
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'stats' in db[interaction.guild.id]:
        db[interaction.guild.id]['stats'] = {}
    if not 'online' in db[interaction.guild.id]['stats']:
        db[interaction.guild.id]['stats']['online'] = {}
    db[interaction.guild.id]['stats']['online']['channel'] = channel.id
    db[interaction.guild.id]['stats']['online']['name'] = name
    saveDb()
    await interaction.followup.send('Check the channel ' + channel.mention + ' for the online count.', ephemeral=True)

async def setoffline(interaction, name:str = None):
    """Set the offline count to a voice channel"""
    await interaction.response.defer(ephemeral=True)
    if name is None:
        name = 'Offline: {count}'
    # Create private voice channel
    members = await interaction.guild.chunk()
    channel = await interaction.guild.create_voice_channel(name, category=interaction.channel.category)
    await channel.set_permissions(interaction.guild.default_role, connect=False)
    await channel.edit(name=name.replace('{count}', str(len([m for m in members if m.status == discord.Status.offline]))))
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'stats' in db[interaction.guild.id]:
        db[interaction.guild.id]['stats'] = {}
    if not 'offline' in db[interaction.guild.id]['stats']:
        db[interaction.guild.id]['stats']['offline'] = {}
    db[interaction.guild.id]['stats']['offline']['channel'] = channel.id
    db[interaction.guild.id]['stats']['offline']['name'] = name
    saveDb()
    await interaction.followup.send('Check the channel ' + channel.mention + ' for the offline count.', ephemeral=True)

async def setboosters(interaction, name:str = None):
    """Set the booster count to a voice channel"""
    await interaction.response.defer(ephemeral=True)
    if name is None:
        name = 'Boosters: {count}'
    # Create private voice channel
    members = await interaction.guild.chunk()
    channel = await interaction.guild.create_voice_channel(name, category=interaction.channel.category)
    await channel.set_permissions(interaction.guild.default_role, connect=False)
    await channel.edit(name=name.replace('{count}', str(len([m for m in members if m.premium_since is not None]))))
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'stats' in db[interaction.guild.id]:
        db[interaction.guild.id]['stats'] = {}
    if not 'boosters' in db[interaction.guild.id]['stats']:
        db[interaction.guild.id]['stats']['boosters'] = {}
    db[interaction.guild.id]['stats']['boosters']['channel'] = channel.id
    db[interaction.guild.id]['stats']['boosters']['name'] = name
    saveDb()
    await interaction.followup.send('Check the channel ' + channel.mention + ' for the booster count.', ephemeral=True)

async def setboostlevel(interaction, name:str = None):
    """Set the boost level to a voice channel"""
    await interaction.response.defer(ephemeral=True)
    if name is None:
        name = 'Boost Level: {count}'
    # Create private voice channel
    channel = await interaction.guild.create_voice_channel(name, category=interaction.channel.category)
    await channel.set_permissions(interaction.guild.default_role, connect=False)
    await channel.edit(name=name.replace('{count}', str(interaction.guild.premium_tier)))
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'stats' in db[interaction.guild.id]:
        db[interaction.guild.id]['stats'] = {}
    if not 'boostlevel' in db[interaction.guild.id]['stats']:
        db[interaction.guild.id]['stats']['boostlevel'] = {}
    db[interaction.guild.id]['stats']['boostlevel']['channel'] = channel.id
    db[interaction.guild.id]['stats']['boostlevel']['name'] = name
    saveDb()
    await interaction.followup.send('Check the channel ' + channel.mention + ' for the boost level.', ephemeral=True)

async def setboosttiers(interaction, name:str = None):
    """Set the boost tiers to a voice channel"""
    await interaction.response.defer(ephemeral=True)
    if name is None:
        name = 'Boost Tier: {count}'
    # Create private voice channel
    channel = await interaction.guild.create_voice_channel(name, category=interaction.channel.category)
    await channel.set_permissions(interaction.guild.default_role, connect=False)
    await channel.edit(name=name.replace('{count}', str(interaction.guild.premium_subscription_count)))
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'stats' in db[interaction.guild.id]:
        db[interaction.guild.id]['stats'] = {}
    if not 'boosttiers' in db[interaction.guild.id]['stats']:
        db[interaction.guild.id]['stats']['boosttiers'] = {}
    db[interaction.guild.id]['stats']['boosttiers']['channel'] = channel.id
    db[interaction.guild.id]['stats']['boosttiers']['name'] = name
    saveDb()
    await interaction.followup.send('Check the channel ' + channel.mention + ' for the boost tiers.', ephemeral=True)

async def setadmins(interaction, name:str = None):
    """Set the admin count to a voice channel"""
    await interaction.response.defer(ephemeral=True)
    if name is None:
        name = 'Admins: {count}'
    # Create private voice channel
    members = await interaction.guild.chunk()
    channel = await interaction.guild.create_voice_channel(name, category=interaction.channel.category)
    await channel.set_permissions(interaction.guild.default_role, connect=False)
    await channel.edit(name=name.replace('{count}', str(len([m for m in members if m.guild_permissions.administrator]))))
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'stats' in db[interaction.guild.id]:
        db[interaction.guild.id]['stats'] = {}
    if not 'admins' in db[interaction.guild.id]['stats']:
        db[interaction.guild.id]['stats']['admins'] = {}
    db[interaction.guild.id]['stats']['admins']['channel'] = channel.id
    db[interaction.guild.id]['stats']['admins']['name'] = name
    saveDb()
    await interaction.followup.send('Check the channel ' + channel.mention + ' for the admin count.', ephemeral=True)

# update stats
async def updateStats():
    while True:
        for guild in client.guilds:
            if guild.id in db and 'stats' in db[guild.id]:
                try:
                    if 'members' in db[guild.id]['stats']:
                        channel = client.get_channel(db[guild.id]['stats']['members']['channel'])
                        if channel is not None:
                            await channel.edit(name=db[guild.id]['stats']['members']['name'].replace('{count}', str(guild.member_count)))
                    if 'bots' in db[guild.id]['stats']:
                        channel = client.get_channel(db[guild.id]['stats']['bots']['channel'])
                        if channel is not None:
                            await channel.edit(name=db[guild.id]['stats']['bots']['name'].replace('{count}', str(len([m for m in guild.members if m.bot]))))
                    if 'online' in db[guild.id]['stats']:
                        channel = client.get_channel(db[guild.id]['stats']['online']['channel'])
                        if channel is not None:
                            await channel.edit(name=db[guild.id]['stats']['online']['name'].replace('{count}', str(len([m for m in guild.members if m.status is not discord.Status.offline]))))
                    if 'offline' in db[guild.id]['stats']:
                        channel = client.get_channel(db[guild.id]['stats']['offline']['channel'])
                        if channel is not None:
                            await channel.edit(name=db[guild.id]['stats']['offline']['name'].replace('{count}', str(len([m for m in guild.members if m.status is discord.Status.offline]))))
                    if 'boosters' in db[guild.id]['stats']:
                        channel = client.get_channel(db[guild.id]['stats']['boosters']['channel'])
                        if channel is not None:
                            await channel.edit(name=db[guild.id]['stats']['boosters']['name'].replace('{count}', str(len([m for m in guild.members if m.premium_since is not None]))))
                    if 'boostlevel' in db[guild.id]['stats']:
                        channel = client.get_channel(db[guild.id]['stats']['boostlevel']['channel'])
                        if channel is not None:
                            await channel.edit(name=db[guild.id]['stats']['boostlevel']['name'].replace('{count}', str(guild.premium_tier)))
                    if 'boosttiers' in db[guild.id]['stats']:
                        channel = client.get_channel(db[guild.id]['stats']['boosttiers']['channel'])
                        if channel is not None:
                            await channel.edit(name=db[guild.id]['stats']['boosttiers']['name'].replace('{count}', str(guild.premium_subscription_count)))
                    if 'admins' in db[guild.id]['stats']:
                        channel = client.get_channel(db[guild.id]['stats']['admins']['channel'])
                        if channel is not None:
                            await channel.edit(name=db[guild.id]['stats']['admins']['name'].replace('{count}', str(len([m for m in guild.members if m.guild_permissions.administrator]))))
                except:
                    pass
        await asyncio.sleep(1)
    await updateStats()

# Get stream info
def getStreamInfo_Twitch(channelname):
    client_id = 'uaw3vx1k0ttq74u9b2zfvt768eebh1'
    # Get id from channelname
    url = 'https://api.twitch.tv/helix/users?login=' + channelname
    headers = {'Client-ID': client_id}
    r = requests.get(url, headers=headers, timeout=5)
    if r.status_code == 200:
        data = r.json()
        if len(data['data']) > 0:
            id = data['data'][0]['id']
            # Get stream info
            url = 'https://api.twitch.tv/helix/streams?user_id=' + id
            headers = {'Client-ID': client_id}
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if len(data['data']) > 0:
                    streaminfo = {}
                    streaminfo['title'] = data['data'][0]['title']
                    streaminfo['game'] = data['data'][0]['game_name']
                    streaminfo['image'] = data['data'][0]['thumbnail_url'].replace('{width}', '1920').replace('{height}', '1080')
                    streaminfo['thumbnail'] = data['data'][0]['thumbnail_url'].replace('{width}', '320').replace('{height}', '180')
                    streaminfo['viewers'] = data['data'][0]['viewer_count']
                    streaminfo['starttime'] = datetime.datetime.strptime(data['data'][0]['started_at'], '%Y-%m-%dT%H:%M:%SZ')
                    return streaminfo
    return False

async def isLive():
    for guild in client.guilds:
        if guild.id in db and 'livestats' in db[guild.id]:
            try:
                if 'twitch' in db[guild.id]['livestats']:
                    for i in range(len(db[guild.id]['livestats']['twitch'])):
                        channel = client.get_channel(db[guild.id]['livestats']['twitch'][i]['channel'])
                        if channel is not None:
                            channelname = db[guild.id]['livestats']['twitch'][i]['name']
                            # Is user live?
                            if not 'oldstatus' in db[guild.id]['livestats']['twitch'][i]:
                                db[guild.id]['livestats']['twitch'][i]['oldstatus'] = False
                            if not db[guild.id]['livestats']['twitch'][i]['oldstatus']:
                                streaminfo = getStreamInfo_Twitch(channelname)
                                if streaminfo is not False:
                                    db[guild.id]['livestats']['twitch'][i]['oldstatus'] = True
                                    embed = discord.Embed(title=channelname + ' is live!', url='https://twitch.tv/' + channelname, color=0x6441a5)
                                    # Set thumbnail
                                    embed.set_thumbnail(url=streaminfo['thumbnail'])
                                    # Set stream info
                                    embed.add_field(name='Title', value=streaminfo['title'], inline=True)
                                    embed.add_field(name='Game', value=streaminfo['game'], inline=True)
                                    embed.add_field(name='Viewers', value=streaminfo['viewers'], inline=True)
                                    # Set stream start time
                                    embed.timestamp = streaminfo['starttime']
                                    # Set image
                                    embed.set_image(url=streaminfo['image'])
                                    await channel.send('@here', embed=embed)
                            else:
                                streaminfo = getStreamInfo_Twitch(channelname)
                                if streaminfo is False:
                                    db[guild.id]['livestats']['twitch'][i]['oldstatus'] = False
                                    embed = discord.Embed(title=channelname + ' is no longer live!', url='https://twitch.tv/' + channelname, color=0x6441a5)
                                    await channel.send(embed=embed)
            except Exception as e:
                print(e)
        await asyncio.sleep(5)
    await asyncio.sleep(30)
    await isLive()

# Twitch follow
async def follow_twitch(interaction: discord.Interaction, channel: discord.TextChannel, name: str, follow: bool = True):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if follow:
        if not 'livestats' in db[interaction.guild.id]:
            db[interaction.guild.id]['livestats'] = {}
        if not 'twitch' in db[interaction.guild.id]['livestats']:
            db[interaction.guild.id]['livestats']['twitch'] = []
        isFound = False
        for i in range(len(db[interaction.guild.id]['livestats']['twitch'])):
            if db[interaction.guild.id]['livestats']['twitch'][i]['channel'] == channel.id and db[interaction.guild.id]['livestats']['twitch'][i]['name'] == name:
                isFound = True
                break
        if not isFound:
            db[interaction.guild.id]['livestats']['twitch'].append({'channel': channel.id, 'name': name})
            await interaction.response.send_message('You are now following ' + name + ' on Twitch!', ephemeral=True)
        else:
            await interaction.response.send_message('You are already following ' + name + ' on Twitch!', ephemeral=True)
    else:
        if 'livestats' in db[interaction.guild.id] and 'twitch' in db[interaction.guild.id]['livestats']:
            for i in range(len(db[interaction.guild.id]['livestats']['twitch'])):
                if db[interaction.guild.id]['livestats']['twitch'][i]['channel'] == channel.id and db[interaction.guild.id]['livestats']['twitch'][i]['name'] == name:
                    del db[interaction.guild.id]['livestats']['twitch'][i]
                    await interaction.response.send_message('You are no longer following ' + name + ' on Twitch!', ephemeral=True)
                    break
            else:
                await interaction.response.send_message('You are not following ' + name + ' on Twitch!', ephemeral=True)
        else:
            await interaction.response.send_message('You are not following ' + name + ' on Twitch!', ephemeral=True)



# Bump
async def bump_setup(interaction, channel:discord.TextChannel):
    """Setup the bump system"""
    members = interaction.guild.members
    for member in members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.manage_guild:
                await interaction.response.send_message('You need the manage server permission to use this command.', ephemeral=True)
    # Modal
    class BumpModal(ui.Modal, title='Bump Setup'):
        message = ui.TextInput(label='Message', placeholder='Bump message above invite link', style=discord.TextStyle.long)
        async def on_submit(self, interaction: discord.Interaction):
            if not interaction.guild.id in db:
                db[interaction.guild.id] = {}
            if not 'bump' in db[interaction.guild.id]:
                db[interaction.guild.id]['bump'] = {}
            db[interaction.guild.id]['bump']['channel'] = channel.id
            db[interaction.guild.id]['bump']['message'] = self.message.value
            invitex =await channel.create_invite(max_age=0, max_uses=0, unique=True)
            db[interaction.guild.id]['bump']['invite'] = 'https://discord.gg/'+invitex.code
            saveDb()
            await interaction.response.send_message('Bump system setup complete!', ephemeral=True)
    await interaction.response.send_modal(BumpModal())

async def bump(interaction):
    """Bump the server"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'bump' in db[interaction.guild.id]:
        db[interaction.guild.id]['bump'] = {}
    if not 'lastbump' in db[interaction.guild.id]['bump']:
        db[interaction.guild.id]['bump']['lastbump'] = {}
    if not interaction.user.id in db[interaction.guild.id]['bump']['lastbump']:
        db[interaction.guild.id]['bump']['lastbump'][interaction.user.id] = 0
    if not 'bumps' in db[interaction.guild.id]['bump']:
        db[interaction.guild.id]['bump']['bumps'] = {}
    if not interaction.user.id in db[interaction.guild.id]['bump']['bumps']:
        db[interaction.guild.id]['bump']['bumps'][interaction.user.id] = 0
    if not 'channel' in db[interaction.guild.id]['bump']:
        await interaction.response.send_message('Share system not setup. Use /share setup to setup the bump system.', ephemeral=True)
    else:
        channel = client.get_channel(db[interaction.guild.id]['bump']['channel'])
        if channel is None:
            await interaction.response.send_message('Share system not setup. Use /share setup to setup the bump system.', ephemeral=True)
        else:
            if not 'message' in db[interaction.guild.id]['bump']:
                await interaction.response.send_message('Share system not setup. Use /share setup to setup the bump system.', ephemeral=True)
            else:
                if not 'invite' in db[interaction.guild.id]['bump']:
                    await interaction.response.send_message('Share system not setup. Use /share setup to setup the bump system.', ephemeral=True)
                else:
                    if db[interaction.guild.id]['bump']['lastbump'][interaction.user.id] + 7200 < time.time():
                        db[interaction.guild.id]['bump']['lastbump'][interaction.user.id] = time.time()
                        saveDb()
                    else:
                        if db[interaction.guild.id]['bump']['lastbump'][interaction.user.id] + 7200 - time.time() > 3600:
                            await interaction.response.send_message(f'You can bump again in {round((db[interaction.guild.id]["bump"]["lastbump"][interaction.user.id] + 7200 - time.time()) / 3600)} hours.', ephemeral=True)
                        else:
                            await interaction.response.send_message(f'You can bump again in {round((db[interaction.guild.id]["bump"]["lastbump"][interaction.user.id] + 7200 - time.time()) / 60)} minutes.', ephemeral=True)
                        return
                    db[interaction.guild.id]['bump']['bumps'][interaction.user.id] += 1
                    await interaction.response.send_message('Bumping server...', ephemeral=True)
                    if 'rewards' in db[interaction.guild.id]['bump']:
                        for reward in db[interaction.guild.id]['bump']['rewards']:
                            if db[interaction.guild.id]['bump']['bumps'][interaction.user.id] == reward['bumps']:
                                if reward['type'] == 'role':
                                    role = discord.utils.get(interaction.guild.roles, id=reward['role'])
                                    if role is not None:
                                        await interaction.user.add_roles(role)
                                elif reward['type'] == 'eco':
                                    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
                                    ecosystem[interaction.guild.id]['users'][interaction.user.id]['balance'] += reward['amount']
                                    json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
                    for guild in db:
                        if 'bump' in db[guild]:
                            if 'channel' in db[guild]['bump']:
                                channelx = client.get_channel(db[guild]['bump']['channel'])
                                if channelx is not None:
                                    try:
                                        await channelx.send(str(db[interaction.guild.id]['bump']['message'] + '\n\n|| ' + db[interaction.guild.id]['bump']['invite'] + ' ||').replace('@','(AT)'))

                                    except:
                                        pass
                    await interaction.followup.send('Bump sent!', ephemeral=True)

# View / Edit Rewards

async def bump_rewards_auto(
    interaction: discord.Interaction,
    reward: str,
) -> list[app_commands.Choice[str]]:
    """Returns a list of rewards for the bump system"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'bump' in db[interaction.guild.id]:
        db[interaction.guild.id]['bump'] = {}
    if not 'rewards' in db[interaction.guild.id]['bump']:
        db[interaction.guild.id]['bump']['rewards'] = []
    rew = []
    for reward in db[interaction.guild.id]['bump']['rewards']:
        if reward['type'] == 'role':
            role = discord.utils.get(interaction.guild.roles, id=reward['role'])
            if role is not None:
                rew.append(app_commands.Choice(value=str(reward['id']), name=f'{role.name} ({reward["bumps"]} bumps)'))
        elif reward['type'] == 'eco':
            rew.append(app_commands.Choice(value=str(reward['id']), name=f'${reward["amount"]} ({reward["bumps"]} bumps)'))
    rew.append(app_commands.Choice(value='new', name='New Reward'))
    return rew


@app_commands.autocomplete(reward=bump_rewards_auto)
async def bump_rewards(interaction: discord.Interaction, reward: str):
    """View / Edit rewards for the bump system"""
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'bump' in db[interaction.guild.id]:
        db[interaction.guild.id]['bump'] = {}
    if not 'rewards' in db[interaction.guild.id]['bump']:
        db[interaction.guild.id]['bump']['rewards'] = []
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
    if reward == 'new':
        class NewReward(ui.View):
            @ui.button(label='Role', style=discord.ButtonStyle.green)
            async def role(self, interaction: discord.Interaction, button: ui.Button):
                class RoleRewardModal(ui.Modal, title='Role Reward'):
                    role_id = ui.TextInput(label = 'Role ID', placeholder='Role ID', min_length=15, max_length=20)
                    bumps = ui.TextInput(label = 'Bumps', placeholder='Bumps', min_length=1, max_length=5)
                    async def on_submit(self, interaction: discord.Interaction):
                        if not interaction.guild.id in db:
                            db[interaction.guild.id] = {}
                        if not 'bump' in db[interaction.guild.id]:
                            db[interaction.guild.id]['bump'] = {}
                        if not 'rewards' in db[interaction.guild.id]['bump']:
                            db[interaction.guild.id]['bump']['rewards'] = []
                        db[interaction.guild.id]['bump']['rewards'].append({
                            'id': len(db[interaction.guild.id]['bump']['rewards']) + 1,
                            'type': 'role',
                            'role': int(self.role_id.value),
                            'bumps': int(self.bumps.value)
                        })
                        await interaction.response.send_message('Reward added!', ephemeral=True)
                await interaction.response.send_modal(RoleRewardModal())
            @ui.button(label='Economy', style=discord.ButtonStyle.green)
            async def eco(self, interaction: discord.Interaction, button: ui.Button):
                class EcoRewardModal(ui.Modal, title='Economy Reward'):
                    amount = ui.TextInput(label = 'Amount', placeholder='Amount', min_length=1, max_length=5)
                    bumps = ui.TextInput(label = 'Bumps', placeholder='Bumps', min_length=1, max_length=5)
                    async def on_submit(self, interaction: discord.Interaction):
                        if not interaction.guild.id in db:
                            db[interaction.guild.id] = {}
                        if not 'bump' in db[interaction.guild.id]:
                            db[interaction.guild.id]['bump'] = {}
                        if not 'rewards' in db[interaction.guild.id]['bump']:
                            db[interaction.guild.id]['bump']['rewards'] = []
                        db[interaction.guild.id]['bump']['rewards'].append({
                            'id': len(db[interaction.guild.id]['bump']['rewards']) + 1,
                            'type': 'eco',
                            'amount': int(self.amount.value),
                            'bumps': int(self.bumps.value)
                        })
                        await interaction.response.send_message('Reward added!', ephemeral=True)
                await interaction.response.send_modal(EcoRewardModal())
        await interaction.response.send_message('Select a reward type:', view=NewReward())
    else:
        reward = int(reward)
        for rewardx in db[interaction.guild.id]['bump']['rewards']:
            if rewardx['id'] == reward:
                if rewardx['type'] == 'role':
                    class RoleRewards(ui.View):
                        @ui.button(label='Delete', style=discord.ButtonStyle.red)
                        async def delete(self, interaction: discord.Interaction, button: ui.Button):
                            db[interaction.guild.id]['bump']['rewards'].remove(rewardx)
                            await interaction.response.send_message('Reward deleted!', ephemeral=True)
                        @ui.button(label='Edit', style=discord.ButtonStyle.green)
                        async def edit(self, interaction: discord.Interaction, button: ui.Button):
                            class RoleRewardEditModal(ui.Modal, title='Role Reward'):
                                bumps = ui.TextInput(label = 'Bumps', placeholder='Bumps', min_length=1, max_length=5)
                                async def on_submit(self, interaction: discord.Interaction):
                                    rewardx['bumps'] = int(self.bumps.value)
                                    await interaction.response.send_message('Reward edited!', ephemeral=True)
                            await interaction.response.send_modal(RoleRewardEditModal())
                    await interaction.response.send_message(f'Role: {discord.utils.get(interaction.guild.roles, id=rewardx["role"]).name}\nBumps: {rewardx["bumps"]}', view=RoleRewards())
                elif rewardx['type'] == 'eco':
                    class EcoRewards(ui.View):
                        @ui.button(label='Delete', style=discord.ButtonStyle.red)
                        async def delete(self, interaction: discord.Interaction, button: ui.Button):
                            db[interaction.guild.id]['bump']['rewards'].remove(rewardx)
                            await interaction.response.send_message('Reward deleted!', ephemeral=True)
                        @ui.button(label='Edit', style=discord.ButtonStyle.green)
                        async def edit(self, interaction: discord.Interaction, button: ui.Button):
                            class EcoRewardEditModal(ui.Modal, title='Economy Reward'):
                                amount = ui.TextInput(label = 'Amount', placeholder='Amount', min_length=1, max_length=5)
                                bumps = ui.TextInput(label = 'Bumps', placeholder='Bumps', min_length=1, max_length=5)
                                async def on_submit(self, interaction: discord.Interaction):
                                    rewardx['amount'] = int(self.amount.value)
                                    rewardx['bumps'] = int(self.bumps.value)
                                    await interaction.response.send_message('Reward edited!', ephemeral=True)
                            await interaction.response.send_modal(EcoRewardEditModal())
                    await interaction.response.send_message(f'Amount: {rewardx["amount"]}\nBumps: {rewardx["bumps"]}', view=EcoRewards())
                break
        else:
            await interaction.response.send_message('Invalid reward!', ephemeral=True)






        




ticketParameters = {}

# Ticket Modal
class ticketModal(ui.Modal, title = "Create Ticket Panel"):
    desciption = ui.TextInput(label = "Description", placeholder = "Click the button to create a ticket")
    emoji = ui.TextInput(label = "Emoji", placeholder = "🎫")
    buttonTitle = ui.TextInput(label = "Button Title", placeholder = "Create Ticket")
    color = ui.TextInput(label = "Color", placeholder = "0xFFFFFF")
    sendMessage = ui.TextInput(label = "Send Message", placeholder = "Hi {user}, support will be with you shortly")
    async def on_submit(self, interaction: discord.Interaction):
        if interaction.guild.id in tickets:
            if ticketParameters[interaction.guild.id]['name'] in tickets[interaction.guild.id]:
                await interaction.response.send_message("This ticket panel already exists", ephemeral=True)
            else:
                ticketEmbed = discord.Embed(title = ticketParameters[interaction.guild.id]['name'], description = self.desciption.value, color = int(self.color.value, 16))
                ticketEmbed.set_footer(text = ticketParameters[interaction.guild.id]['name'])
                button_view = discord.ui.View()
                button = ui.Button(label = self.emoji.value + '  ' + self.buttonTitle.value, style = discord.ButtonStyle.green, custom_id = f"create_ticket_{interaction.guild.id}_{ticketParameters[interaction.guild.id]['name']}")
                button_view.add_item(button)
                msg = await interaction.channel.send(embed = ticketEmbed, view = button_view)
                tickets[interaction.guild.id][ticketParameters[interaction.guild.id]['name']] = {
                    'channel': interaction.channel.id,
                    'message': msg.id,
                    'description': self.desciption.value,
                    'emoji': self.emoji.value,
                    'buttonTitle': self.buttonTitle.value,
                    'color': self.color.value,
                    'sendMessage': self.sendMessage.value,
                    'category': None
                }
                await interaction.response.send_message("Ticket panel created", ephemeral=True)
        else:
            tickets[interaction.guild.id] = {}
            ticketEmbed = discord.Embed(title = ticketParameters[interaction.guild.id]['name'], description = self.desciption.value, color = int(self.color.value, 16))
            ticketEmbed.set_footer(text = ticketParameters[interaction.guild.id]['name'])
            button_view = discord.ui.View()
            button = ui.Button(label = self.emoji.value + '  ' + self.buttonTitle.value, style = discord.ButtonStyle.green, custom_id = f"create_ticket_{interaction.guild.id}_{ticketParameters[interaction.guild.id]['name']}")
            button_view.add_item(button)
            msg = await interaction.channel.send(embed = ticketEmbed, view = button_view)
            tickets[interaction.guild.id][ticketParameters[interaction.guild.id]['name']] = {
                'channel': interaction.channel.id,
                'message': msg.id,
                'description': self.desciption.value,
                'emoji': self.emoji.value,
                'buttonTitle': self.buttonTitle.value,
                'color': self.color.value,
                'sendMessage': self.sendMessage.value,
                'category': None
            }
            await interaction.response.send_message("Ticket panel created", ephemeral=True)

        saveTickets()

# Ticket Panel 
@client.tree.command(name='tickets')
@app_commands.guild_only()
@app_commands.choices(action=[app_commands.Choice(name = 'Create', value='create'), app_commands.Choice(name='Delete', value = 'delete'), app_commands.Choice(name = 'Help', value = 'help'), app_commands.Choice(name = 'Set Category', value = 'setcategory'), app_commands.Choice(name = 'Set Support Channel', value = 'setchannel'), app_commands.Choice(name = 'Create Form', value = 'createform')])
async def ticket(interaction:discord.Interaction, action: str, name: str, category: discord.CategoryChannel = None, form_questions: int = 3):
    """ Manage Ticket Panels """
    for members in interaction.guild.members:
        if members.id == interaction.user.id:
            if not members.guild_permissions.manage_channels:
                await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
                return
    # If Create, Open Modal
    if action == 'create':
        ticketParameters[interaction.guild.id] = {}
        ticketParameters[interaction.guild.id]['name'] = name
        await interaction.response.send_modal(ticketModal())
    # If Delete, Delete Ticket Panel
    elif action == 'delete':
        if interaction.guild.id in tickets:
            if name in tickets[interaction.guild.id]:
                # Find ticket panel by message id
                ticketx = tickets[interaction.guild.id][name]
                try:
                    ticketmessage = await interaction.guild.get_channel(ticketx['channel']).fetch_message(ticketx['message'])
                    # Delete ticket panel
                    await ticketmessage.delete()
                except:
                    pass
                del tickets[interaction.guild.id][name]
                await interaction.response.send_message("Ticket panel deleted", ephemeral=True)
            else:
                await interaction.response.send_message("This ticket panel doesn't exist", ephemeral=True)
        else:
            await interaction.response.send_message("This ticket panel doesn't exist", ephemeral=True)
        saveTickets()
    elif action == 'setcategory':
        if not is_premium(interaction.guild.id):
            await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        if interaction.guild.id in tickets:
            if name in tickets[interaction.guild.id]:
                try:
                    tickets[interaction.guild.id][name]['category'] = category.id
                    await interaction.response.send_message("Category set", ephemeral=True)
                except:
                    await interaction.response.send_message("You need to mention a category", ephemeral=True)
            else:
                await interaction.response.send_message("This ticket panel doesn't exist", ephemeral=True)
        else:
            await interaction.response.send_message("This ticket panel doesn't exist", ephemeral=True)
        saveTickets()
    # If Help, Send Help Message
    elif action == 'help':
        await interaction.response.send_message("Create a ticket panel by using the create action, delete a ticket panel by using the delete action, set the category of the ticket by using the setcategory action", ephemeral=True)
    elif action == 'setchannel':
        if not is_premium(interaction.guild.id):
            await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        if interaction.guild.id in tickets:
            if name in tickets[interaction.guild.id]:
                tickets[interaction.guild.id][name]['channel'] = interaction.channel.id
                await interaction.response.send_message("Support channel set", ephemeral=True)
            else:
                await interaction.response.send_message("This ticket panel doesn't exist", ephemeral=True)
        else:
            await interaction.response.send_message("This ticket panel doesn't exist", ephemeral=True)
        saveTickets()
    elif action == 'createform':
        if not is_premium(interaction.guild.id):
            await interaction.response.send_message('This server is not premium!\nBuy premium here: '+support_server_url(interaction.user.id, interaction.guild.id), ephemeral=True)
        if interaction.guild.id in tickets:
            if name in tickets[interaction.guild.id]:
                tickets[interaction.guild.id][name]['form'] = []
                if form_questions == 1:
                    class CreateForm(ui.Modal, title='Create Form'):
                        question1 = ui.TextInput(label = f"Question 1", custom_id = f"question_1")
                        async def on_submit(self, interaction:discord.Interaction):
                            for i in range(form_questions):
                                tickets[interaction.guild.id][name]['form'].append(self.children[i].value)
                            await interaction.response.send_message("Form created", ephemeral=True)
                            saveTickets()
                elif form_questions == 2:
                    class CreateForm(ui.Modal, title='Create Form'):
                        question1 = ui.TextInput(label = f"Question 1", custom_id = f"question_1")
                        question2 = ui.TextInput(label = f"Question 2", custom_id = f"question_2")
                        async def on_submit(self, interaction:discord.Interaction):
                            for i in range(form_questions):
                                tickets[interaction.guild.id][name]['form'].append(self.children[i].value)
                            await interaction.response.send_message("Form created", ephemeral=True)
                            saveTickets()
                elif form_questions == 3:
                    class CreateForm(ui.Modal, title='Create Form'):
                        question1 = ui.TextInput(label = f"Question 1", custom_id = f"question_1")
                        question2 = ui.TextInput(label = f"Question 2", custom_id = f"question_2")
                        question3 = ui.TextInput(label = f"Question 3", custom_id = f"question_3")
                        async def on_submit(self, interaction:discord.Interaction):
                            for i in range(form_questions):
                                tickets[interaction.guild.id][name]['form'].append(self.children[i].value)
                            await interaction.response.send_message("Form created", ephemeral=True)
                            saveTickets()
                elif form_questions == 4:
                    class CreateForm(ui.Modal, title='Create Form'):
                        question1 = ui.TextInput(label = f"Question 1", custom_id = f"question_1")
                        question2 = ui.TextInput(label = f"Question 2", custom_id = f"question_2")
                        question3 = ui.TextInput(label = f"Question 3", custom_id = f"question_3")
                        question4 = ui.TextInput(label = f"Question 4", custom_id = f"question_4")
                        async def on_submit(self, interaction:discord.Interaction):
                            for i in range(form_questions):
                                tickets[interaction.guild.id][name]['form'].append(self.children[i].value)
                            await interaction.response.send_message("Form created", ephemeral=True)
                            saveTickets()
                elif form_questions == 5:
                    class CreateForm(ui.Modal, title='Create Form'):
                        question1 = ui.TextInput(label = f"Question 1", custom_id = f"question_1")
                        question2 = ui.TextInput(label = f"Question 2", custom_id = f"question_2")
                        question3 = ui.TextInput(label = f"Question 3", custom_id = f"question_3")
                        question4 = ui.TextInput(label = f"Question 4", custom_id = f"question_4")
                        question5 = ui.TextInput(label = f"Question 5", custom_id = f"question_5")
                        async def on_submit(self, interaction:discord.Interaction):
                            for i in range(form_questions):
                                tickets[interaction.guild.id][name]['form'].append(self.children[i].value)
                            await interaction.response.send_message("Form created", ephemeral=True)
                            saveTickets()
                elif form_questions == 0:
                    await interaction.response.send_message("You need to specify the number of questions", ephemeral=True)
                else:
                    await interaction.response.send_message("You can't create a form with more than 5 questions", ephemeral=True)
                await interaction.response.send_modal(CreateForm())
            else:
                await interaction.response.send_message("This ticket panel doesn't exist", ephemeral=True)
        else:
            await interaction.response.send_message("This ticket panel doesn't exist", ephemeral=True)


# User Backup Command
@app_commands.choices(action = [app_commands.Choice(name='Send Message', value='sendmessage'), app_commands.Choice(name='Restore', value='restore'), app_commands.Choice(name='Ask all to authorize', value='all')])
async def memberbackup(interaction, action:str, message:str = None, role:discord.Role = None):
    """Backup all members of the server"""
    await interaction.response.send_message("Sorry, command currently under maintenance", ephermeral = True)
    if interaction.user.id != 963125433770070096:
        for member in interaction.guild.members:
            if member.id == interaction.user.id:
                if not member.guild_permissions.administrator:
                    await interaction.response.send_message("You need to be an administrator to use this command", ephemeral=True)
                    return
    if role:
        if not interaction.guild.id in db:
            db[interaction.guild.id] = {}
        db[interaction.guild.id]['memberbackup'] = role.id
        saveDb()
    if action == 'sendmessage':
        if not message:
            await interaction.response.send_message("Click the button below to authorize me to make you rejoin if this server gets nuked.", view = discord.ui.View().add_item(ui.Button(label = "Authorize", style = discord.ButtonStyle.green, custom_id = f"verify_{interaction.guild.id}")))
        else:
            await interaction.response.send_message(message, view = discord.ui.View().add_item(ui.Button(label = "Authorize", style = discord.ButtonStyle.green, custom_id = f"verify_{interaction.guild.id}")))
    elif action == 'all':
        await interaction.response.send_message('Sorry, this is disabled until bot is verified')
        counter = 0
        members = await interaction.guild.chunk()
        # 0.1 second each member
        await interaction.response.send_message('Asking '+str(len(members))+' members to authorize now...\nThis will take a bit')
        for member in members:
            try:
                await member.send(f"Click the button below to authorize me to make you rejoin if {interaction.guild.name} gets nuked.", view = discord.ui.View().add_item(ui.Button(label = "Authorize", style = discord.ButtonStyle.green, custom_id = f"verify_{interaction.guild.id}")))
                await asyncio.sleep(0.1)
            except:
                await asyncio.sleep(0.1)
            counter += 1
        await interaction.followup.send(content = f"Asked {counter} members to authorize.")
    elif action == 'restore':
        await interaction.response.defer()
        await AsyncClient.get(f"https://backup.dragonspot.tk/makejoin?oldguild={interaction.guild.id}&newguild={interaction.guild.id}")
        await interaction.followup.send("If you setted all right, all authorized members from this server should rejoin now.")


# Auto respond
async def addresponse(interaction, message:str, response:str):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'autorespond' in db[interaction.guild.id]:
        db[interaction.guild.id]['autorespond'] = {}
    db[interaction.guild.id]['autorespond'][message] = response
    saveDb()
    await interaction.response.send_message("Added auto response", ephemeral=True)



async def remmove_response_auto_message(
    interaction: discord.Interaction,
    message: str,
) -> list[app_commands.Choice[str]]:
    """Returns a list of choices for the auto response message to remove."""
    choices = []
    if interaction.guild.id in db:
        if "autorespond" in db[interaction.guild.id]:
            for key in db[interaction.guild.id]["autorespond"]:
                choices.append(app_commands.Choice(name=key, value=key))
    return choices


@app_commands.autocomplete(message=remmove_response_auto_message)
async def removeresponse(interaction, message:str):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'autorespond' in db[interaction.guild.id]:
        db[interaction.guild.id]['autorespond'] = {}
    if message in db[interaction.guild.id]['autorespond']:
        del db[interaction.guild.id]['autorespond'][message]
        saveDb()
        await interaction.response.send_message("Removed auto response", ephemeral=True)
    else:
        await interaction.response.send_message("This auto response doesn't exist", ephemeral=True)


async def listresponses(interaction):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'autorespond' in db[interaction.guild.id]:
        db[interaction.guild.id]['autorespond'] = {}
    if len(db[interaction.guild.id]['autorespond']) == 0:
        await interaction.response.send_message("There are no auto responses", ephemeral=True)
    else:
        await interaction.response.send_message("Here are all auto responses", ephemeral=True)
        for key in db[interaction.guild.id]['autorespond']:
            await interaction.followup.send(f"**{key}**\n{db[interaction.guild.id]['autorespond'][key]}", ephemeral=True)


async def send_response(message):
    print('x')
    if message.guild.id in db:
        print('ok')
        if 'autorespond' in db[message.guild.id]:
            print('yes')
            print(len(db[message.guild.id]['autorespond']))
            print(db[message.guild.id]['autorespond'])
            for key in db[message.guild.id]['autorespond']:
                # Replaces like {$1} and {$$1} with the corresponding group
                # $$ means all after the match
                # $1 means the first match
                # $2 means the second match
                messages = message.content.split(' ')
                try:
                    respondingmessage = db[message.guild.id]['autorespond'][key]
                    for match in re.finditer(r"\{\$([0-9]+)\}", respondingmessage):
                        # Get from the message
                        respondingmessage = respondingmessage.replace(match.group(0), messages[int(match.group(1))])

                    for match in re.finditer(r"\{\$\$([0-9]+)\}", respondingmessage):
                        # Get from the message
                        respondingmessage = respondingmessage.replace(match.group(0), " ".join(messages[int(match.group(1)):]))
                    if message.content.lower().startswith(key.lower()):
                        try:
                            await message.channel.send(respondingmessage.format(user = message.author, guild = message.guild, channel = message.channel))
                        except Exception as es:
                            print(es)
                        return
                    print(key)
                except Exception as e:
                    print(e)

# Automod - Words / Regex
async def addblock(interaction, word:str):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'automod' in db[interaction.guild.id]:
        db[interaction.guild.id]['automod'] = []
    if not word in db[interaction.guild.id]['automod']:
        db[interaction.guild.id]['automod'].append(word)
        saveDb()
        await interaction.response.send_message("Added word/regex to blocklist", ephemeral=True)
    else:
        await interaction.response.send_message("This word/regex is already in the blocklist", ephemeral=True)

async def activate_automod(interaction):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'aimod' in db[interaction.guild.id]:
        db[interaction.guild.id]['aimod'] = False
    if db[interaction.guild.id]['aimod'] == False:
        db[interaction.guild.id]['aimod'] = True
        saveDb()
        await interaction.response.send_message("Activated Artificial Intelligence", ephemeral=True)
    else:
        await interaction.response.send_message("Artificial Intelligence already activated", ephemeral=True)
        
async def deactivate_automod(interaction):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'aimod' in db[interaction.guild.id]:
        db[interaction.guild.id]['aimod'] = True
    if db[interaction.guild.id]['aimod'] == True:
        db[interaction.guild.id]['aimod'] = False
        saveDb()
        await interaction.response.send_message("Deactivated Artificial Intelligence", ephemeral=True)
    else:
        await interaction.response.send_message("Artificial Intelligence already deactivated", ephemeral=True)

async def remmove_block_auto_message(
    interaction: discord.Interaction,
    word: str,
) -> list[app_commands.Choice[str]]:
    """Returns a list of choices for the blocked word to remove."""
    choices = []
    if interaction.guild.id in db:
        if "automod" in db[interaction.guild.id]:
            for key in db[interaction.guild.id]["automod"]:
                choices.append(app_commands.Choice(name=key, value=key))
    return choices


@app_commands.autocomplete(word=remmove_block_auto_message)
async def removeblock(interaction, word:str):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'automod' in db[interaction.guild.id]:
        db[interaction.guild.id]['automod'] = []
    if word in db[interaction.guild.id]['automod']:
        db[interaction.guild.id]['automod'].remove(word)
        saveDb()
        await interaction.response.send_message("Removed word/regex from blocklist", ephemeral=True)
    else:
        await interaction.response.send_message("This word/regex isn't in the blocklist", ephemeral=True)


async def listblocks(interaction):
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'automod' in db[interaction.guild.id]:
        db[interaction.guild.id]['automod'] = []
    if len(db[interaction.guild.id]['automod']) == 0:
        await interaction.response.send_message("There are no words/regexes in the blocklist", ephemeral=True)
    else:
        await interaction.response.send_message("Here are all words/regexes in the blocklist", ephemeral=True)
        for key in db[interaction.guild.id]['automod']:
            await interaction.followup.send(f"**{key}**", ephemeral=True)


async def check_message(message):
    if message.guild.id in db:
        if 'automod' in db[message.guild.id]:
            for key in db[message.guild.id]['automod']:
                # Check if regex in message
                if re.search(key, message.content):
                    try:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention} Your message was deleted because it contained blocked content", delete_after=5)
                    except Exception as es:
                        print(es)
    return False



# Backup system
# only owner, only guild
@app_commands.guild_only()
async def create_backup(interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id == interaction.guild.owner_id or interaction.user.id == <DEV_ID>:
        # Respond
        await interaction.followup.send("Creating backup...", ephemeral=True)
        backup_count = open('backup-count.txt','r').read()
        backup_count = int(backup_count) +1
        # Save to backup-backupid.json
        # Save guildid to backup-userid.json
        backupfile = open(f'backups/backup-{backup_count}.json','w')
        open('backup-count.txt','w').write(str(backup_count))
        if os.path.exists(f'backups/backup-{interaction.user.id}.json'):
            userbackuplist = open(f'backups/backup-{interaction.user.id}.json','r')
            userbackuplist = json.load(userbackuplist)
            userbackuplist.append({'name':f'{backup_count}','date':f'{datetime.datetime.now()}'})
            json.dump(userbackuplist, open(f'backups/backup-{interaction.user.id}.json','w'))
        else:
            json.dump([{'name':f'{backup_count}','date':f'{datetime.datetime.now()}'}], open(f'backups/backup-{interaction.user.id}.json','w'))
        # Save roles
        roles = []
        for role in interaction.guild.roles:
            roles.append({
                'name': role.name,
                'permissions': role.permissions.value,
                'color': role.color.value,
                'hoist': role.hoist,
                'mentionable': role.mentionable,
                'position': role.position,
                'id': role.id
            })
        # Save channels
        channels = []
        channeloverwrites = []
        for channel in interaction.guild.channels:
            if channel.type == discord.ChannelType.text:
                channels.append({
                    'name': channel.name,
                    'topic': channel.topic,
                    'nsfw': channel.nsfw,
                    'slowmode_delay': channel.slowmode_delay,
                    'category': channel.category_id,
                    'position': channel.position,
                    'id': channel.id,
                    'type': 0
                })
            elif channel.type == discord.ChannelType.voice:
                channels.append({
                    'name': channel.name,
                    'bitrate': channel.bitrate,
                    'user_limit': channel.user_limit,
                    'category': channel.category_id,
                    'position': channel.position,
                    'id': channel.id,
                    'type': 2
                })
            elif channel.type == discord.ChannelType.category:
                channels.append({
                    'name': channel.name,
                    'id': channel.id,
                    'position': channel.position,
                    'type': 4
                })
            elif channel.type == discord.ChannelType.stage_voice:
                channels.append({
                    'name': channel.name,
                    'topic': channel.topic,
                    'nsfw': channel.nsfw,
                    'slowmode_delay': channel.slowmode_delay,
                    'category': channel.category_id,
                    'id': channel.id,
                    'position': channel.position,
                    'type': 13
                })
            elif channel.type == discord.ChannelType.news:
                channels.append({
                    'name': channel.name,
                    'topic': channel.topic,
                    'nsfw': channel.nsfw,
                    'slowmode_delay': channel.slowmode_delay,
                    'category': channel.category_id,
                    'id': channel.id,
                    'position': channel.position,
                    'type': 5
                })
            for overx in channel.overwrites:
                over = channel.overwrites_for(overx)
                channeloverwrites.append({
                    'send_messages': over.send_messages,
                    'manage_messages': over.manage_messages,
                    'manage_channels': over.manage_channels,
                    'mention_everyone': over.mention_everyone,
                    'view_channel': over.view_channel,
                    'read_messages': over.read_messages,
                    'channel': channel.id,
                    'id': overx.id
                })
        # Save emojis
        emojis = []
        for emoji in interaction.guild.emojis:
            emojis.append({
                'name': emoji.name,
                'animated': emoji.animated,
                'id': emoji.id,
                'image': str(emoji.url)
            })
        # Save bans
        bans = []
        async for ban in interaction.guild.bans():
            bans.append({
                'id': ban.user.id,
                'reason': ban.reason
            })
        # Save guild
        guild = {
            'name': interaction.guild.name,
            'icon': str(interaction.guild.icon.url)
        }
        settings = db[interaction.guild.id]
        settings = str(settings)
        settings = settings.replace(str(interaction.guild.id),'👀👀SERVERID👀👀')
        # Save data
        data = {
            'roles': roles,
            'channels': channels,
            'channeloverwrites': channeloverwrites,
            'emojis': emojis,
            'bans': bans,
            'guild': guild,
            'settings': settings
        }
        # Save data
        json.dump(data, open(f'backups/backup-{backup_count}.json','w'))
        # Send backup
        await interaction.followup.send(f'Backup created!.', ephemeral=True)

# list backups
async def list_backups(interaction):
    # Get backups
    backup_list = open('backups/backup-'+str(interaction.user.id)+'.json','r')
    backup_list = json.load(backup_list)
    backup_list.reverse()
    # Create embed
    embed = discord.Embed(
        title = 'Backups',
        description = 'Here are your backups.',
        color = discord.Color.green()
    )
    # Add fields
    for backup in backup_list:
        backupx = open('backups/backup-'+str(backup['name'])+'.json','r')
        backupx = json.load(backupx)
        embed.add_field(
            name = backupx['guild']['name'],
            value = f'Created at: {backup["date"]}',
            inline = True
        )
    # Send embed
    await interaction.response.send_message(embed=embed, ephemeral=True)

# restore

async def backup_command_auto(
    interaction: discord.Interaction,
    backup_id: int,
) -> list[app_commands.Choice[str]]:
    """Returns a list of choices for the restore command."""
    choices = []
    # All backups from user
    backups = open('backups/backup-'+str(interaction.user.id)+'.json','r')
    backups = json.load(backups)
    backups.reverse()
    # Add choices
    for backup in backups:
        # Get guild name
        backupx = open('backups/backup-'+str(backup['name'])+'.json','r')
        backupx = json.load(backupx)
        choices.append(app_commands.Choice(name=backupx['guild']['name'] + ' - ' + backup['date'], value=int(backup['name'])))
    return choices

@app_commands.autocomplete(backup_id=backup_command_auto)
async def restore_backup(interaction, backup_id:int):
    await interaction.response.defer(ephemeral= True)
    # Does backup exist?
    if not os.path.exists(f'backups/backup-{backup_id}.json'):
        await interaction.followup.send('Backup does not exist.', ephemeral=True)
        return
    # Load backup
    backup = open(f'backups/backup-{backup_id}.json','r')
    backup = json.load(backup)
    guild = backup['guild']
    channels = backup['channels']
    channeloverwrites = backup['channeloverwrites']
    roles = backup['roles']
    emojis = backup['emojis']
    bans = backup['bans']
    # Sort channels: First categories, then other channels
    channels.sort(key=lambda x: x['type'])
    channels.reverse()
    # Check perms
    if not interaction.user.id == interaction.guild.owner_id and not interaction.user.id == <DEV_ID>:
        await interaction.followup.send('You do not have permission to restore this backup.', ephemeral=True)
        return
    # Ask for confirm (button)
    await interaction.followup.send('Are you sure you want to restore this backup?\n\nThis will delete all channels, roles, emojis, bans, and messages in this server.', 
        view = ui.View(timeout=None).add_item(ui.Button(label='Confirm', style=discord.ButtonStyle.green, custom_id='confirm'))
    )
    # Wait for confirm
    try:
        interaction = await client.wait_for('interaction', check=lambda i: (i.user.id == interaction.user.id and 'custom_id' in i.data and i.data['custom_id'] == 'confirm'), timeout=60)
        await interaction.response.send_message('Restoring backup...', ephemeral=True)
    except asyncio.TimeoutError:
        await interaction.followup.send('Timed out.', ephemeral=True)
        return
    temp_backup = {
        'roles': {},
        'channels': {},
    }
    # Delete roles
    for role in interaction.guild.roles:
        try:
            if role.name != 'SplitticHost Bot':
                await role.delete()
        except:
            pass
    # Remove role Splittic Bot from roles
    roles = [role for role in roles if role['name'] != 'SplitticHost Bot']
    # Delete channels
    for channel in interaction.guild.channels:
        try:
            await channel.delete()
        except:
            pass
    # Delete emojis
    for emoji in interaction.guild.emojis:
        try:
            await emoji.delete()
        except:
            pass
    # Delete bans
    async for ban in interaction.guild.bans():
        try:
            await interaction.guild.unban(ban.user)
        except:
            pass
    # Create roles
    roles.reverse()
    for role in range(len(roles)):
        try:
            # Check if everyone role
            if roles[role]['name'] == '@everyone':
                # Edit 
                await interaction.guild.default_role.edit(
                    name = roles[role]['name'],
                    permissions = discord.Permissions(roles[role]['permissions']),
                    color = discord.Colour(roles[role]['color']),
                    hoist = roles[role]['hoist'],
                    mentionable = roles[role]['mentionable'],
                    reason = 'Restoring backup'
                )
                temp_backup['roles'][roles[role]['id']] = interaction.guild.default_role.id
            else:
                # Edit
                newrole = await interaction.guild.create_role(
                    name = roles[role]['name'],
                    color = discord.Color(roles[role]['color']),
                    hoist = roles[role]['hoist'],
                    mentionable = roles[role]['mentionable'],
                    reason = 'Restoring backup',
                    permissions = discord.Permissions(roles[role]['permissions'])
                )
                temp_backup['roles'][roles[role]['id']] = newrole.id
        except Exception as e:
            print(e)
    # Create channels
    for channel in range(len(channels)):
        try:
            if channels[channel]['type'] == 0:
                newchannel = await interaction.guild.create_text_channel(
                    name = channels[channel]['name'],
                    topic = channels[channel]['topic'],
                    slowmode_delay = channels[channel]['slowmode_delay'],
                    nsfw = channels[channel]['nsfw'],
                    reason = 'Restoring backup',
                    category = discord.utils.get(interaction.guild.categories, id=temp_backup['channels'][channels[channel]['category']]) if channels[channel]['category'] else None,
                    position = channels[channel]['position']
                )
            elif channels[channel]['type'] == 2:
                newchannel = await interaction.guild.create_voice_channel(
                    name = channels[channel]['name'],
                    bitrate = channels[channel]['bitrate'],
                    user_limit = channels[channel]['user_limit'],
                    reason = 'Restoring backup',
                    category = discord.utils.get(interaction.guild.categories, id=temp_backup['channels'][channels[channel]['category']]) if channels[channel]['category'] else None,
                    position = channels[channel]['position']
                )
            elif channels[channel]['type'] == 4:
                newchannel = await interaction.guild.create_category(
                    name = channels[channel]['name'],
                    reason = 'Restoring backup',
                    position = channels[channel]['position']
                )
            temp_backup['channels'][channels[channel]['id']] = newchannel.id
        except Exception as e:
            print(e)
    # Update overwrites
    for channel in range(len(channeloverwrites)):
        try:
            overchannel = interaction.guild.get_channel(temp_backup['channels'][channeloverwrites[channel]['channel']])
            overrole = interaction.guild.get_role(temp_backup['roles'][channeloverwrites[channel]['id']])
            over = overchannel.overwrites_for(overrole)
            over.send_messages = channeloverwrites[channel]['send_messages']
            over.manage_messages = channeloverwrites[channel]['manage_messages']
            over.manage_channels = channeloverwrites[channel]['manage_channels']
            over.mention_everyone = channeloverwrites[channel]['mention_everyone']
            over.view_channel = channeloverwrites[channel]['view_channel']
            over.read_messages = channeloverwrites[channel]['read_messages']
            
            cx = interaction.guild.get_channel(temp_backup['channels'][channeloverwrites[channel]['channel']])
            await cx.set_permissions(
                interaction.guild.get_role(temp_backup['roles'][channeloverwrites[channel]['id']]),
                reason = 'Restoring backup',
                overwrite = over
            )
        except Exception as e:
            print(e)
    # Create emojis
    for emoji in range(len(emojis)):
        try:
            await interaction.guild.create_custom_emoji(
                name = emojis[emoji]['name'],
                image = emojis[emoji]['image'],
                reason = 'Restoring backup'
            )
        except Exception as e:
            print(e)
    # Create bans
    for ban in range(len(bans)):
        try:
            await interaction.guild.ban(
                user = client.get_user(bans[ban]['id']),
                reason = 'Restoring backup'
            )
        except Exception as e:
            print(e)
    # Update Guild
    await interaction.guild.edit(name = backup['guild']['name'], reason = 'Restoring backup')
    settings = backup['settings']
    # settings => db
    settings = settings.replace('👀👀SERVERID👀👀', str(interaction.guild.id))
    for role in range(len(roles)):
        # replace id from old role to new role
        try:
            settings = settings.replace(str(roles[role]['id']), str(temp_backup['roles'][roles[role]['id']]))
        except:
            pass
    for channel in range(len(channels)):
        # replace id from old channel to new channel
        try:
            settings = settings.replace(str(channels[channel]['id']), str(temp_backup['channels'][channels[channel]['id']]))
        except:
            pass

    # load (not json)
    settings = eval(settings)
    # update
    db[interaction.guild.id] = settings
    # save
    saveDb()







    


        







# Moderation: autodelete
@app_commands.choices(time = [app_commands.Choice(name='Off', value='0'), app_commands.Choice(name='1 Minute', value='60'), app_commands.Choice(name='5 Minutes', value='300'), app_commands.Choice(name='10 Minutes', value='600'), app_commands.Choice(name='30 Minutes', value='1800'), app_commands.Choice(name='1 Hour', value='3600'), app_commands.Choice(name='2 Hours', value='7200'), app_commands.Choice(name='6 Hours', value='21600'), app_commands.Choice(name='12 Hours', value='43200')])
async def autodelete(interaction, channel:discord.TextChannel, time:str):
    """Automatically delete messages in a channel"""
    if interaction.user.id != 963125433770070096:
        for member in interaction.guild.members:
            if member.id == interaction.user.id:
                if not member.guild_permissions.administrator:
                    await interaction.response.send_message("You need to be an administrator to use this command", ephemeral=True)
                    return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'autodelete' in db[interaction.guild.id]:
        db[interaction.guild.id]['autodelete'] = {}
    db[interaction.guild.id]['autodelete'][channel.id] = time
    saveDb()
    await interaction.response.send_message("Successfully set autodelete for channel " + channel.mention, ephemeral=True)

# Moderation: autoping
async def autoping(interaction, channel:discord.TextChannel):
    """Automatically ping a member who joins the server"""
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message("You need to be an administrator to use this command", ephemeral=True)
                return
    if not interaction.guild.id in db:
        db[interaction.guild.id] = {}
    if not 'autoping' in db[interaction.guild.id]:
        db[interaction.guild.id]['autoping'] = []
    if not channel.id in db[interaction.guild.id]['autoping']:
        db[interaction.guild.id]['autoping'].append(channel.id)
        await interaction.response.send_message("Added auto ping to channel", ephemeral=True)
    else:
        db[interaction.guild.id]['autoping'].remove(channel.id)
        await interaction.response.send_message("Removed auto ping from channel", ephemeral=True)

# Button Click
@client.event
async def on_interaction(interaction: discord.Interaction):
    if not 'custom_id' in interaction.data:
        return
    if interaction.data['custom_id'].startswith('reply-'):
        userid = interaction.data['custom_id'].split('-')[1]
        # fetch member
        try:
            member = await interaction.guild.fetch_member(int(userid))
        except:
            await interaction.response.send_message("This member left already", ephemeral=True)
            await interaction.message.edit(view = discord.ui.View().add_item(ui.Button(label = "User left", style = discord.ButtonStyle.grey, disabled = True)))
            return
        if not member:
            await interaction.response.send_message("This member left already", ephemeral=True)
            await interaction.message.edit(view = discord.ui.View().add_item(ui.Button(label = "User left", style = discord.ButtonStyle.grey, disabled = True)))
            return
        class replyModMailModal(ui.Modal,title='Reply to '+member.name):
            messagex = ui.TextInput(label='Message',placeholder='Your message', style=discord.TextStyle.long)
            async def on_submit(self, interaction:discord.Interaction):
                await member.send(embed=discord.Embed(title='Message from '+interaction.guild.name, description=self.messagex.value, color=0x00ff00))
                await interaction.response.send_message('Message sent!', ephemeral=True)
                # Disable button
                await interaction.message.edit(view = discord.ui.View().add_item(ui.Button(label = "Replied", style = discord.ButtonStyle.grey, disabled = True)))
                return
        await interaction.response.send_modal(replyModMailModal())
    if interaction.data['custom_id'].startswith('create_ticket_'):
        # Check if user has an open ticket
        if not interaction.guild.id in tickets:
            tickets[interaction.guild.id] = {}
        if tickets[interaction.guild.id][interaction.data['custom_id'].split('_')[3]]['category']:
            for channel in client.get_channel(tickets[interaction.guild.id][interaction.data['custom_id'].split('_')[3]]['category']).channels:
                if channel.name == f"ticket-{interaction.user.id}":
                    await interaction.response.send_message("You already have an open ticket", ephemeral=True)
                    return
        else:
            for channel in interaction.guild.channels:
                if str(interaction.user.id) in channel.name:
                    await interaction.response.send_message("You already have an open ticket", ephemeral=True)
                    return
        # Get ticket panel data
        ticketx = tickets[interaction.guild.id][interaction.data['custom_id'].split('_')[3]]
        if not 'form' in ticketx:
            # Create ticket channel
            ticketChannel = await interaction.guild.create_text_channel(f"ticket-{interaction.user.id}")
            # Add user to ticket channel
            await ticketChannel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            # Remove everyone from ticket channel
            await ticketChannel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
            for role in ticketChannel.guild.roles:
                if role.name.lower() == 'supporter':
                    await ticketChannel.set_permissions(role, read_messages=True, send_messages=True)
            # Move ticket channel to category
            if ticketx['category'] != None:
                await ticketChannel.edit(category=interaction.guild.get_channel(ticketx['category']))
            # Send ticket message
            ticketEmbed = discord.Embed(title = f"Ticket: {interaction.user.name}", description = ticketx['sendMessage'].replace('{user}', f'<@{interaction.user.id}>'), color = int(ticketx['color'], 16))
            ticketEmbed.set_footer(text = interaction.data['custom_id'].split('_')[3])
            closeButton = ui.Button(label = "Close Ticket", style = discord.ButtonStyle.red, custom_id = f"ask_close_ticket_{interaction.guild.id}_{ticketChannel.id}")
            # Send message in new ticket channel
            view = discord.ui.View()
            view.add_item(closeButton)
            ticketMessage = await ticketChannel.send('<@' + str(interaction.user.id) + '>', embed = ticketEmbed, view = view)
            # Send ticket panel response message
            await interaction.response.send_message("Ticket created (<#"+str(ticketChannel.id)+">)", ephemeral=True)
            if 'channel' in ticketx:
                # Send ticket panel response message in support channel
                joinTicketButton = ui.Button(label = "Join Ticket", style = discord.ButtonStyle.green, custom_id = f"join_ticket_{interaction.guild.id}_{ticketChannel.id}")
                view = discord.ui.View()
                view.add_item(joinTicketButton)
                await interaction.guild.get_channel(ticketx['channel']).send(f"<@{interaction.user.id}> created a {interaction.data['custom_id'].split('_')[3]} ticket", view = view)
        else:
            class CreateTicket(ui.Modal, title='Please answer correctly'):
                if len(ticketx['form']) == 1:
                    answer1 = ui.TextInput(label = ticketx['form'][0], custom_id = f"question_1", style=discord.TextStyle.long)
                elif len(ticketx['form']) == 2:
                    answer1 = ui.TextInput(label = ticketx['form'][0], custom_id = f"question_1", style=discord.TextStyle.long)
                    answer2 = ui.TextInput(label = ticketx['form'][1], custom_id = f"question_2", style=discord.TextStyle.long)
                elif len(ticketx['form']) == 3:
                    answer1 = ui.TextInput(label = ticketx['form'][0], custom_id = f"question_1", style=discord.TextStyle.long)
                    answer2 = ui.TextInput(label = ticketx['form'][1], custom_id = f"question_2", style=discord.TextStyle.long)
                    answer3 = ui.TextInput(label = ticketx['form'][2], custom_id = f"question_3", style=discord.TextStyle.long)
                elif len(ticketx['form']) == 4:
                    answer1 = ui.TextInput(label = ticketx['form'][0], custom_id = f"question_1", style=discord.TextStyle.long)
                    answer2 = ui.TextInput(label = ticketx['form'][1], custom_id = f"question_2", style=discord.TextStyle.long)
                    answer3 = ui.TextInput(label = ticketx['form'][2], custom_id = f"question_3", style=discord.TextStyle.long)
                    answer4 = ui.TextInput(label = ticketx['form'][3], custom_id = f"question_4", style=discord.TextStyle.long)
                elif len(ticketx['form']) == 5:
                    answer1 = ui.TextInput(label = ticketx['form'][0], custom_id = f"question_1", style=discord.TextStyle.long)
                    answer2 = ui.TextInput(label = ticketx['form'][1], custom_id = f"question_2", style=discord.TextStyle.long)
                    answer3 = ui.TextInput(label = ticketx['form'][2], custom_id = f"question_3", style=discord.TextStyle.long)
                    answer4 = ui.TextInput(label = ticketx['form'][3], custom_id = f"question_4", style=discord.TextStyle.long)
                    answer5 = ui.TextInput(label = ticketx['form'][4], custom_id = f"question_5", style=discord.TextStyle.long)
                async def on_submit(self, newinteraction:discord.Interaction):
                    if len(ticketx['form']) == 1:
                        answer1 = self.answer1.value
                    elif len(ticketx['form']) == 2:
                        answer1 = self.answer1.value
                        answer2 = self.answer2.value
                    elif len(ticketx['form']) == 3:
                        answer1 = self.answer1.value
                        answer2 = self.answer2.value
                        answer3 = self.answer3.value
                    elif len(ticketx['form']) == 4:
                        answer1 = self.answer1.value
                        answer2 = self.answer2.value
                        answer3 = self.answer3.value
                        answer4 = self.answer4.value
                    elif len(ticketx['form']) == 5:
                        answer1 = self.answer1.value
                        answer2 = self.answer2.value
                        answer3 = self.answer3.value
                        answer4 = self.answer4.value
                        answer5 = self.answer5.value
                    # Create ticket channel
                    ticketChannel = await interaction.guild.create_text_channel(f"ticket-{interaction.user.id}")
                    # Add user to ticket channel
                    await ticketChannel.set_permissions(interaction.user, read_messages=True, send_messages=True)
                    # Remove everyone from ticket channel
                    await ticketChannel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
                    for role in ticketChannel.guild.roles:
                        if role.name.lower() == 'supporter':
                            await ticketChannel.set_permissions(role, read_messages=True, send_messages=True)
                    # Move ticket channel to category
                    if ticketx['category'] != None:
                        await ticketChannel.edit(category=interaction.guild.get_channel(ticketx['category']))
                    # Send ticket message
                    ticketEmbed = discord.Embed(title = f"Ticket: {interaction.user.name}", color = int(ticketx['color'], 16))
                    for i in range(len(ticketx['form'])):
                        ticketEmbed.add_field(name = ticketx['form'][i], value = eval(f"answer{i+1}"), inline = False)
                    ticketEmbed.set_footer(text = interaction.data['custom_id'].split('_')[3])
                    closeButton = ui.Button(label = "Close Ticket", style = discord.ButtonStyle.red, custom_id = f"ask_close_ticket_{interaction.guild.id}_{ticketChannel.id}")
                    # Send message in new ticket channel
                    view = discord.ui.View()
                    view.add_item(closeButton)
                    ticketMessage = await ticketChannel.send('<@' + str(interaction.user.id) + '>', embed = ticketEmbed, view = view)
                    # Send ticket panel response message
                    await newinteraction.response.send_message("Ticket created (<#"+str(ticketChannel.id)+">)", ephemeral=True)
                    if 'channel' in ticketx:
                        # Send ticket panel response message in support channel
                        joinTicketButton = ui.Button(label = "Join Ticket", style = discord.ButtonStyle.green, custom_id = f"join_ticket_{interaction.guild.id}_{ticketChannel.id}")
                        view = discord.ui.View()
                        view.add_item(joinTicketButton)
                        await interaction.guild.get_channel(ticketx['channel']).send(f"<@{interaction.user.id}> created a {interaction.data['custom_id'].split('_')[3]} ticket", view = view)
            await interaction.response.send_modal(CreateTicket())
    elif interaction.data['custom_id'].startswith('ask_close_ticket_'):
        # Send confirm message
        closeButton = ui.Button(label = "Close Ticket", style = discord.ButtonStyle.red, custom_id = f"close_ticket_{interaction.guild.id}_{interaction.data['custom_id'].split('_')[3]}")
        view = discord.ui.View()
        view.add_item(closeButton)
        await interaction.response.send_message("Are you done with this ticket?", view = view)
    elif interaction.data['custom_id'].startswith('close_ticket_'):
        if interaction.user.id == int(interaction.channel.name.split('-')[1]):
            # Rename Ticket Channel
            await interaction.channel.edit(name = f"closed-{interaction.channel.name}")
            # Remove user from ticket channel
            await interaction.channel.set_permissions(interaction.user, read_messages=False, send_messages=False)
            await interaction.channel.send("Ticket closed by " + interaction.user.name)
            # Create log file
            logFile = open(f"logs/{interaction.channel.id}.txt", "w")
            # Get messages from ticket channel
            async for message in interaction.channel.history(limit=1000):
                # Write message to log file
                logFile.write(f"{message.author.name}: {message.content}\n")
            # Close log file
            logFile.close()
            # Find or create logs channel
            # Reverse the lines
            lines = open(f"logs/{interaction.channel.id}.txt", "r").readlines()
            lines.reverse()
            # Write the lines back to the file
            open(f"logs/{interaction.channel.id}.txt", "w").writelines(lines)
            try:
                logsChannel = discord.utils.get(interaction.guild.channels, name='ticket-logs')
                if logsChannel == None:
                    logsChannel = await interaction.guild.create_text_channel('ticket-logs')
                    # Remove everyone from logs channel
                    await logsChannel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
                # Send log file to logs channel
                await logsChannel.send(file=discord.File(f"logs/{interaction.channel.id}.txt", filename=f"{interaction.channel.name}.txt"))
                # Send log file to ticket owner
            except:
                pass
            try:
                user = await interaction.guild.fetch_member(int(interaction.channel.name.split('-')[1]))
                await user.send(file=discord.File(f"logs/{interaction.channel.id}.txt", filename=f"{interaction.channel.name}.txt"))
            except:
                pass
            # Delete log file
            os.remove(f"logs/{interaction.channel.id}.txt")
            # Delete ticket channel
            await interaction.channel.delete()
            # Edit Join Ticket Button
            for channel in interaction.guild.channels:
                for ticketx in tickets[interaction.guild.id]:
                    if 'channel' in tickets[interaction.guild.id][ticketx]:
                        if channel.id == tickets[interaction.guild.id][ticketx]['channel']:
                            async for message in channel.history(limit=1000):
                                for button in message.components:
                                    try:
                                        if button.children[0].custom_id == f"join_ticket_{interaction.guild.id}_{interaction.channel.id}":
                                            await message.edit(view = None)
                                    except:
                                        pass

        else:
            # Force Close Button
            closeButton = ui.Button(label = "Force Close Ticket", style = discord.ButtonStyle.red, custom_id = f"force_close_ticket_{interaction.guild.id}_{interaction.data['custom_id'].split('_')[3]}")
            view = discord.ui.View()
            view.add_item(closeButton)
            await interaction.response.send_message("You are not the owner of this ticket. Do you want to force the close?", view = view)
    elif interaction.data['custom_id'].startswith('force_close_ticket_'):
        # Rename Ticket Channel
        await interaction.channel.edit(name = f"closed-{interaction.channel.name}")
        # Remove user from ticket channel
        await interaction.channel.set_permissions(interaction.user, read_messages=False, send_messages=False)
        await interaction.channel.send("Ticket closed by " + interaction.user.name)
        # Create log file
        logFile = open(f"logs/{interaction.channel.id}.txt", "w")
        # Get messages from ticket channel
        async for message in interaction.channel.history(limit=1000):
            # Write message to log file
            logFile.write(f"{message.author.name}: {message.content}\n")
        # Close log file
        logFile.close()
        # Find or create logs channel
        logsChannel = discord.utils.get(interaction.guild.channels, name='ticket-logs')
        if logsChannel == None:
            logsChannel = await interaction.guild.create_text_channel('ticket-logs')
            # Remove everyone from logs channel
            await logsChannel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
        # Reverse the lines
        lines = open(f"logs/{interaction.channel.id}.txt", "r").readlines()
        lines.reverse()
        # Write the lines back to the file
        open(f"logs/{interaction.channel.id}.txt", "w").writelines(lines)
        # Send log file to logs channel
        await logsChannel.send(file=discord.File(f"logs/{interaction.channel.id}.txt", filename=f"{interaction.channel.name}.txt"))
        # Send log file to ticket owner
        await interaction.user.send(file=discord.File(f"logs/{interaction.channel.id}.txt", filename=f"{interaction.channel.name}.txt"))
        # Delete log file
        os.remove(f"logs/{interaction.channel.id}.txt")
        # Delete ticket channel
        await interaction.channel.delete()
        # Edit Join Ticket Button
        for channel in interaction.guild.channels:
            for ticketx in tickets[interaction.guild.id]:
                if 'channel' in tickets[interaction.guild.id][ticketx]:
                    if channel.id == tickets[interaction.guild.id][ticketx]['channel']:
                        async for message in channel.history(limit=1000):
                            for button in message.components:
                                try:
                                    if button.children[0].custom_id == f"join_ticket_{interaction.guild.id}_{interaction.channel.id}":
                                        await message.edit(view = None)
                                except:
                                    pass
    elif interaction.data['custom_id'].startswith('join_ticket_'):
        # Get ticket channel
        ticketChannel = interaction.guild.get_channel(int(interaction.data['custom_id'].split('_')[3]))
        # Edit join ticket button
        joinTicketButton = ui.Button(label = "Join Ticket", style = discord.ButtonStyle.green, custom_id = f"join_ticket_{interaction.guild.id}_{ticketChannel.id}", disabled = True)
        view = discord.ui.View()
        view.add_item(joinTicketButton)
        await interaction.response.edit_message(view = view)
        # Add user to ticket channel
        await ticketChannel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        # Send ticket panel message
        await ticketChannel.send(f"{interaction.user.mention} joined the ticket")
    elif interaction.data['custom_id'].startswith('verify_'):
        try:
            await interaction.response.defer(ephemeral=True)
            x = await AsyncClient.get("https://backup.dragonspot.tk/isverified?guild="+str(interaction.data['custom_id'].split('_')[1])+"&user="+str(interaction.user.id))
            if x.text == "true":
                # Get guild
                guild = client.get_guild(int(interaction.data['custom_id'].split('_')[1]))
                # Add role
                for role in guild.roles:
                    if role.id == db[interaction.guild.id]['memberbackup']:
                        for member in guild.members:
                            if member.id == interaction.user.id:
                                await member.add_roles(role)
                                break
                # Send message
                await interaction.followup.send("You are verified.", ephemeral = True)
                return
            guildid = interaction.data['custom_id'].split('_')[1]
            url = 'https://discord.com/api/oauth2/authorize?client_id='+str(client.user.id)+'&redirect_uri=https%3A%2F%2Fbackup.dragonspot.tk%2Fverify&response_type=code&scope=identify%20guilds.join'
            await AsyncClient.get('https://backup.dragonspot.tk/new?guild='+str(guildid)+'&user='+str(interaction.user.id))
            msg =await interaction.user.send(str(interaction.user.mention)+"\nAnother step needed, please verify.\nAfter doing so, you will be verified.\nThe **Join Servers** permission is needed to make you rejoin if the server gets nuked.", view = discord.ui.View().add_item(ui.Button(label = "Verify", style = discord.ButtonStyle.url, url = url)))
            await interaction.followup.send('Verification in progress, please check your dms.', ephemeral = True,view = discord.ui.View().add_item(ui.Button(label = "Go to message", style = discord.ButtonStyle.url, url = 'https://discord.com/channels/@me/'+str(msg.channel.id)+'/'+str(msg.id))))
            guild = client.get_guild(int(guildid))
            if not guild.id in db:
                db[guild.id] = {}
            x = await AsyncClient.get("https://backup.dragonspot.tk/isverified?guild="+str(interaction.data['custom_id'].split('_')[1])+"&user="+str(interaction.user.id))
            while x.text != 'true':
                await asyncio.sleep(3)
            for role in guild.roles:
                if not 'memberbackup' in db[guild.id]:
                    break
                if role.id == db[guild.id]['memberbackup']:
                    for member in guild.members:
                        if member.id == interaction.user.id:
                            await member.add_roles(role)
                            break
            await interaction.user.send('**Verified**')
        except Exception as e:
            print(e)
            await interaction.followup.send('Something went wrong, please try again.', ephemeral = True)
    elif interaction.data['custom_id'].startswith('role_'):
        roleid = interaction.data['custom_id'].split('_')[1]
        role = interaction.guild.get_role(int(roleid))
        member = interaction.guild.get_member(interaction.user.id)
        if role in member.roles:
            await member.remove_roles(role)
        else:
            await member.add_roles(role)
        await interaction.response.send_message('Role updated', ephemeral = True)
    elif interaction.data['custom_id'] == "generate_coin" and interaction.guild.id == 1091737979581648908:
        if interaction.user.id in free_coin_delay:
            return await interaction.response.send_message("You needa wait until the 24 hours passed.", ephemeral=True)
        url = "https://cp.splittichost.net/api/vouchers"
        headers = {"Authorization": "Bearer lscIN_-zoqvuKHz2OkOVa8wrmWQwiGxdRjx-TtJKf-X0UpNN", "Accept": "application/json"}
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=24)
        expiry_str = expires_at.strftime("%d-%m-%Y %H:%M:%S")
        requested_voucher_id = str(interaction.user.id)+str(random.randint(10000000000,99999999999))
        data = {
            "memo": "User Voucher - " + str(interaction.user.id),
            "code": requested_voucher_id,
            "uses": 1,
            "credits": 10,
            "expires_at": expiry_str
        }
        response = requests.post(url, headers=headers, data=data)
        await interaction.response.send_message("Redeem 10 coins with the following voucher\nYou can claim again in 24 hours:", ephemeral=True)
        await interaction.followup.send(requested_voucher_id, ephemeral=True)
        free_coin_delay.append(interaction.user.id)
        await asyncio.sleep(86400)
        free_coin_delay.remove(interaction.user.id)

free_coin_delay = []

async def help_command_auto_category(
    interaction: discord.Interaction,
    category: str
) -> list[app_commands.Choice[str]]:
    """Returns a list of choices for a help command auto category."""
    choices = []
    # command_help
    for categoryx in command_help:
        if category in categoryx:
            choices.append(app_commands.Choice(name = categoryx, value = categoryx))
    return choices

@app_commands.autocomplete(category=help_command_auto_category)
@client.tree.command(name='help')
async def help(interaction, category:str = None, command:str = None):
    """Shows help section"""
    if category and (category == 'buttons' or category == 'button'):
        # Information about button ids
        # verify_guildid for verification
        # role_roleid for role buttons
        # create_ticket_guildid_panelname for tickets
        embed = discord.Embed(title='', color=0x2F3136)
        embed.add_field(name='If you want to use buttons at messagebuilder', value='You can use buttons at messagebuilder, but you need to know the button ids. You can find them below', inline=False)
        embed.add_field(name='Verify that a user is not a bot and give the normal memberbackup role', value='verify_<guildid>', inline=False)
        embed.add_field(name='Give a role to a user if they click on the button', value='role_<roleid>', inline=False)
        embed.add_field(name='Remove a role from a user if they click on the button', value='role_<roleid>', inline=False)
        embed.add_field(name='Create a ticket', value='create\_ticket\_<guildid>\_<panelname>', inline=False)
        await interaction.response.send_message(embed=embed)
        return
    if category:
        if category in command_help:
            if not command:
                embed = discord.Embed(title=command_help[category]['information'], color=0x2F3136)
                for command in command_help[category]['commands']:
                    command_text = f'{command}'
                    for parameter in command_help[category]['commands'][command]['parameters']:
                        command_text += f' <{parameter}>' if command_help[category]['commands'][command]['parameters'][parameter]['required'] else f' [{parameter}]'
                    embed.add_field(name=f'{command}', value=f'{command_help[category]["commands"][command]["description"]}\n\n/help category:{category} command:{command}', inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                if command in command_help[category]['commands']:
                    embed = discord.Embed(title=f'{command} Command', description=command_help[category]['commands'][command]['description'], color=0x2F3136)
                    for parameter in command_help[category]['commands'][command]['parameters']:
                        # if required, send <> - type
                        # if not required, send [] - type
                        if command_help[category]['commands'][command]['parameters'][parameter]['required']:
                            embed.add_field(name=f'<{parameter}> - {command_help[category]["commands"][command]["parameters"][parameter]["type"]}', value=command_help[category]['commands'][command]['parameters'][parameter]['description'], inline=False)
                        else:
                            embed.add_field(name=f'[{parameter}] - {command_help[category]["commands"][command]["parameters"][parameter]["type"]}', value=command_help[category]['commands'][command]['parameters'][parameter]['description'], inline=False)
                    if len(command.split(' ')) == 1:
                        # Get command object
                        command_obj = client.tree.get_command(command)
                        # Add click to embed
                        embed.add_field(name='Click to use command', value='</{command_name}:{command_id}>'.format(command_name=command_obj.name, command_id=client.user.id))
                    elif len(command.split(' ')) == 2:
                        # Get command object
                        command_obj = client.tree.get_command(command.split(' ')[0])
                        # Get subcommand object
                        subcommand_obj = command_obj.get_command(command.split(' ')[1])
                        # Add click to embed
                        embed.add_field(name='Click to use command', value='</{command_name} {subcommand_name}:{command_id}>'.format(command_name=command_obj.name, subcommand_name=subcommand_obj.name, command_id=client.user.id))
                    elif len(command.split(' ')) == 3:
                        # Get command object
                        command_obj = client.tree.get_command(command.split(' ')[0])
                        # Get subcommand object
                        subcommand_obj = command_obj.get_command(command.split(' ')[1])
                        # Get subcommand group object
                        subcommand_group_obj = subcommand_obj.get_command(command.split(' ')[2])
                        # Add click to embed
                        embed.add_field(name='Click to use command', value='</{command_name} {subcommand_name} {subcommand_group_name}:{subcommand_group_id}>'.format(command_name=command_obj.name, subcommand_name=subcommand_obj.name, subcommand_group_name=subcommand_group_obj.name, subcommand_group_id=client.user.id))

                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message('Command not found')
        else:
            await interaction.response.send_message('That category does not exist')
    else:
        embed = discord.Embed(title='Categories', description='Categories of commands', color=0x2F3136)
        for category in command_help:
            embed.add_field(name=f'{command_help[category]["information"]}', value=f'/help category:{category}', inline=False)
        await interaction.response.send_message(embed=embed)


# Discord Game SDK (Chess In The Park)
@app_commands.guild_only()
@app_commands.choices(game = [app_commands.Choice(name = 'YouTube Together', value='755600276941176913'),app_commands.Choice(name = 'Watch Together', value='880218394199220334'),app_commands.Choice(name = 'Poker Night', value='755827207812677713'),app_commands.Choice(name = 'Betrayal.io', value='773336526917861400'),app_commands.Choice(name = 'Fishington.io', value='814288819477020702'),app_commands.Choice(name = 'Chess In The Park', value='832012774040141894'),app_commands.Choice(name = 'Sketch Heads', value='902271654783242291'),app_commands.Choice(name = 'Letter League', value='879863686565621790'),app_commands.Choice(name = 'Word Snacks', value='879863976006127627'),app_commands.Choice(name = 'SpellCast', value='852509694341283871'),app_commands.Choice(name = 'Checkers In The Park', value='832013003968348200'),app_commands.Choice(name = 'Blazing 8s', value='832025144389533716'),app_commands.Choice(name = 'Putt Party', value='945737671223947305'),app_commands.Choice(name = 'Land-io', value='903769130790969345'),app_commands.Choice(name = 'Bobble League', value='947957217959759964'),app_commands.Choice(name = 'Ask Away', value='976052223358406656'),app_commands.Choice(name = 'Know What I Meme', value='950505761862189096'),app_commands.Choice(name = 'Bash Out', value='1006584476094177371')])
async def activity(interaction, game:str = None):
    """Start an activity in a voice channel"""
    try:
        member = interaction.guild.get_member(interaction.user.id)
        voiceChannel = member.voice.channel
        if voiceChannel != None:
            url = f"https://discord.com/api/v9/channels/{voiceChannel.id}/invites"
            body = {
                "max_age": 1800,
                "max_uses": 0,
                "target_application_id": game,
                "target_type": 2,
                "temporary": False,
                "validate": None
            }
            auth = {
                "Authorization": "Bot "+TOKEN,
                "Content-Type": "application/json",
                "X-Ratelimit-Precision": "millisecond"
            }

            obj = json.dumps(body, separators=(',', ':'), ensure_ascii=True)
            code = (await AsyncClient.post(url, data = obj, headers = auth))
            print(code.text)
            code = json.loads(code.text)["code"]
            invite = f"https://discord.gg/{code}"
            await interaction.response.send_message(invite)
        else:
            await interaction.response.send_message("Connect to VC first")
    except:
        await interaction.response.send_message("Connect to VC first")

def load_ecosystem(guild_id, user_id):
    try:
        if os.path.isfile(f'eco-{guild_id}.json'):
            # Load ecosystem[interaction.guild.id]
            ecosystem[guild_id] = json.load(open(f'eco-{guild_id}.json'))
            if not str(user_id) in ecosystem[guild_id]['users']:
                ecosystem[guild_id]['users'][str(user_id)] = {
                    'balance': 0,
                    'bank': 0
                }
                ecosystem[guild_id]['users'][str(user_id)] = {}
                ecosystem[guild_id]['users'][str(user_id)]['balance'] = 0
                ecosystem[guild_id]['users'][str(user_id)]['bank'] = 0
                ecosystem[guild_id]['users'][str(user_id)]['daily'] = 0
                ecosystem[guild_id]['users'][str(user_id)]['inventory'] = {}
                ecosystem[guild_id]['users'][str(user_id)]['inventory']['items'] = {}
            else:
                try:
                    ecosystem[guild_id]['users'][str(user_id)]['inventory']['items'].keys()
                except:
                    ecosystem[guild_id]['users'][str(user_id)]['inventory']['items'] = {}
        else:
            # Create ecosystem[interaction.guild.id]
            ecosystem[guild_id] = {}
            ecosystem[guild_id]['users'] = {}
            ecosystem[guild_id]['users'][str(user_id)] = {}
            ecosystem[guild_id]['users'][str(user_id)]['balance'] = 0
            ecosystem[guild_id]['users'][str(user_id)]['bank'] = 0
            ecosystem[guild_id]['users'][str(user_id)]['daily'] = 0
            ecosystem[guild_id]['users'][str(user_id)]['inventory'] = {}
            ecosystem[guild_id]['users'][str(user_id)]['inventory']['items'] = {}
            ecosystem[guild_id]['settings'] = {}
            ecosystem[guild_id]['settings']['daily'] = 10000
            ecosystem[guild_id]['settings']['items'] = {}
            # Save ecosystem[interaction.guild.id]
            json.dump(ecosystem[guild_id], open(f'eco-{guild_id}.json', 'w'), indent=4)
    except:
        # Create ecosystem[interaction.guild.id]
        ecosystem[guild_id] = {}
        ecosystem[guild_id]['users'] = {}
        ecosystem[guild_id]['users'][str(user_id)] = {}
        ecosystem[guild_id]['users'][str(user_id)]['balance'] = 0
        ecosystem[guild_id]['users'][str(user_id)]['bank'] = 0
        ecosystem[guild_id]['users'][str(user_id)]['daily'] = 0
        ecosystem[guild_id]['users'][str(user_id)]['inventory'] = {}
        ecosystem[guild_id]['users'][str(user_id)]['inventory']['items'] = {}
        ecosystem[guild_id]['settings'] = {}
        ecosystem[guild_id]['settings']['daily'] = 10000
        ecosystem[guild_id]['settings']['items'] = {}
        # Save ecosystem[interaction.guild.id]
        json.dump(ecosystem[guild_id], open(f'eco-{guild_id}.json', 'w'), indent=4)
    return ecosystem[guild_id]

ecosystem = {}

# Economy System

# Eco system command callback function

async def balance(interaction):
    """Check your balance"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
    bank = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['bank']
    embed = discord.Embed(title='Balance', description=f'**{interaction.user.name}**', color=0x00ff00)
    embed.add_field(name='Wallet', value=f'${balance}', inline=True)
    embed.add_field(name='Bank', value=f'${bank}', inline=True)
    embed.set_thumbnail(url=interaction.user.avatar.url)
    await interaction.response.send_message(embed=embed)


async def daily(interaction):
    """Claim your daily reward"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    daily = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['daily']
    if daily < time.time():
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['daily'] = time.time() + 86400
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += ecosystem[interaction.guild.id]['settings']['daily']
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message('You have received your daily reward of $10.000')
    else:
        timeleft = daily - time.time()
        # If hours left, round to hours
        if timeleft > 3600:
            timeleft = round(timeleft / 3600)
            timeleft = f'{timeleft} hours'
        # If minutes left, round to minutes
        elif timeleft > 60:
            timeleft = round(timeleft / 60)
            timeleft = f'{timeleft} minutes'
        # If seconds left, round to seconds
        else:
            timeleft = round(timeleft)
            timeleft = f'{timeleft} seconds'
        await interaction.response.send_message(f'You have to wait {timeleft} before claiming your daily reward again')


async def deposit(interaction, amount:int = None):
    """Deposit money into your bank"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
    if amount == None:
        await interaction.response.send_message('Please specify an amount')
    elif amount > balance:
        await interaction.response.send_message('You do not have enough money')
    else:
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= amount
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['bank'] += amount
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'You have deposited ${amount}')


async def withdraw(interaction, amount:int = None):
    """Withdraw money from your bank"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    bank = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['bank']
    if amount == None:
        await interaction.response.send_message('Please specify an amount')
    elif amount > bank:
        await interaction.response.send_message('You do not have enough money')
    else:
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['bank'] -= amount
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'You have withdrawn ${amount}')


async def pay(interaction, user:discord.Member, amount:int = None):
    """Pay someone money"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    load_ecosystem(interaction.guild.id, user.id)
    balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
    if amount == None:
        await interaction.response.send_message('Please specify an amount')
    elif amount > balance:
        await interaction.response.send_message('You do not have enough money')
    else:
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= amount
        ecosystem[interaction.guild.id]['users'][str(user.id)]['balance'] += amount
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'You have paid ${amount} to {user.name}')


@app_commands.guild_only()
async def shop(interaction):
    """View the shop"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    embed = discord.Embed(title='Shop', color=0x00ff00)
    embed.set_thumbnail(url=interaction.guild.icon.url)
    for item in ecosystem[interaction.guild.id]['settings']['items']:
        if not item.startswith('role-'):
            embed.add_field(name=f'{item}', value=f'${ecosystem[interaction.guild.id]["settings"]["items"][item]}', inline=True)
    await interaction.response.send_message(embed=embed)

# /buy
async def buy_command_auto(
    interaction: discord.Interaction,
    item: str
) -> list[app_commands.Choice[str]]:
    choices = []
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    for item in ecosystem[interaction.guild.id]['settings']['items']:
        if not item.startswith('role-'):
            choices.append(app_commands.Choice(name=item, value=item))
    return choices

@app_commands.autocomplete(item= buy_command_auto)
async def buy(interaction, item:str = None, amount:int = None):
    """Buy an item from the shop"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
    if item == None:
        await interaction.response.send_message('Please specify an item')
    elif item not in ecosystem[interaction.guild.id]['settings']['items']:
        await interaction.response.send_message('That item does not exist')
    elif amount == None:
        if balance < ecosystem[interaction.guild.id]['settings']['items'][item]:
            await interaction.response.send_message('You do not have enough money')
        else:
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= ecosystem[interaction.guild.id]['settings']['items'][item]
            if not item in ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items']:
                ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item] = 0
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item] += 1
            json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
            await interaction.response.send_message(f'You have bought 1 {item}')
            if 'role-' + item in ecosystem[interaction.guild.id]['settings']['items']:
                await interaction.user.add_roles(interaction.guild.get_role(ecosystem[interaction.guild.id]['settings']['items']['role-' + item]))
    else:
        if balance < ecosystem[interaction.guild.id]['settings']['items'][item] * amount:
            await interaction.response.send_message('You do not have enough money')
        else:
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= ecosystem[interaction.guild.id]['settings']['items'][item] * amount
            if not item in ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items']:
                ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item] = 0
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item] += amount
            json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
            await interaction.response.send_message(f'You have bought {amount} {item}s')
            if 'role-' + item in ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['items']:
                await interaction.user.add_roles(interaction.guild.get_role(ecosystem[interaction.guild.id]['settings']['items']['role-' + item]))


async def inventory(interaction):
    """View your inventory"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    embed = discord.Embed(title='Inventory', description=f'**{interaction.user.name}**', color=0x00ff00)
    embed.set_thumbnail(url=interaction.user.avatar.url)
    for item in ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items']:
        amount = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item]
        embed.add_field(name=f'{item}', value=f'${ecosystem[interaction.guild.id]["settings"]["items"][item]} | {amount} times', inline=True)
    await interaction.response.send_message(embed=embed)

# /sell
async def sell_command_auto(
    interaction: discord.Interaction,
    item: str
) -> list[app_commands.Choice[str]]:
    choices = []
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    for item in ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items']:
        choices.append(app_commands.Choice(name=item, value=item))
    return choices


@app_commands.autocomplete(item= sell_command_auto)
async def sell(interaction, item:str = None, amount:int = None):
    """Sell an item from your inventory"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if item == None:
        await interaction.response.send_message('Please specify an item')
    elif item not in ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items']:
        await interaction.response.send_message('You do not have that item')
    elif amount == None:
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += ecosystem[interaction.guild.id]['settings']['items'][item]
        if ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item] == 1:
            del ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item]
        else:
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item] -= 1
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'You have sold {item}')
        if 'role-' + item in ecosystem[interaction.guild.id]['settings']['items']:
            await interaction.user.remove_roles(interaction.guild.get_role(ecosystem[interaction.guild.id]['settings']['items']['role-' + item]))
    else:
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += ecosystem[interaction.guild.id]['settings']['items'][item] * amount
        if ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item] == amount:
            del ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item]
        else:
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'][item] -= amount
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'You have sold {amount} {item}s')
        if 'role-' + item in ecosystem[interaction.guild.id]['settings']['items']:
            await interaction.user.remove_roles(interaction.guild.get_role(ecosystem[interaction.guild.id]['settings']['items']['role-' + item]))


async def eco_leaderboard(interaction):
    """View the economy leaderboard"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    embed = discord.Embed(title='Leaderboard', description=f'**{interaction.guild.name}**', color=0x00ff00)
    embed.set_thumbnail(url=interaction.guild.icon.url)
    # Show top 10
    leaderboard = {}
    for user in ecosystem[interaction.guild.id]['users']:
        leaderboard[user] = ecosystem[interaction.guild.id]['users'][user]['balance']
    leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))
    count = 0
    for user in leaderboard:
        if count < 10:
            try:
                embed.add_field(name=f'{client.get_user(int(user)).name}', value=f'${leaderboard[user]}', inline=True)
            except:
                pass
        count += 1
    await interaction.response.send_message(embed=embed)

cooldown = {}


async def rob(interaction, user:discord.Member = None):
    """Rob a user"""
    # Cooldown
    if interaction.user.id in cooldown:
        if cooldown[interaction.user.id] > time.time():
            await interaction.response.send_message('You are on cooldown')
            return
    cooldown[interaction.user.id] = time.time() + 60
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if user == None:
        await interaction.response.send_message('Please specify a user')
    elif user == interaction.user:
        await interaction.response.send_message('You cannot rob yourself')
    else:
        amount = random.randint(1, ecosystem[interaction.guild.id]['users'][str(user.id)]['balance'])
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount
        ecosystem[interaction.guild.id]['users'][str(user.id)]['balance'] -= amount
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'You have robbed ${amount} from {user.name}')


async def eco_reset(interaction):
    """Reset the economy"""
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to do this')
                return
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    ecosystem[interaction.guild.id]['users'] = {}
    json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
    await interaction.response.send_message('Economy has been reset')



async def eco_set(interaction, user:discord.Member = None, amount:int = None):
    """Set a user's balance"""
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to do this')
                return
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if user == None:
        await interaction.response.send_message('Please specify a user')
    elif amount == None:
        await interaction.response.send_message('Please specify an amount')
    else:
        ecosystem[interaction.guild.id]['users'][str(user.id)]['balance'] = amount
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'{user.name}\'s balance has been set to ${amount}')


async def eco_add(interaction, user:discord.Member = None, amount:int = None):
    """Add to a user's balance"""
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to do this')
                return
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if user == None:
        await interaction.response.send_message('Please specify a user')
    elif amount == None:
        await interaction.response.send_message('Please specify an amount')
    else:
        ecosystem[interaction.guild.id]['users'][str(user.id)]['balance'] += amount
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'${amount} has been added to {user.name}\'s balance')


async def eco_remove(interaction, user:discord.Member = None, amount:int = None):
    """Remove from a user's balance"""
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to do this')
                return
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if user == None:
        await interaction.response.send_message('Please specify a user')
    elif amount == None:
        await interaction.response.send_message('Please specify an amount')
    else:
        ecosystem[interaction.guild.id]['users'][str(user.id)]['balance'] -= amount
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'${amount} has been removed from {user.name}\'s balance')


async def eco_give(interaction, user:discord.Member = None, item:str = None):
    """Give an item to a user"""
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if user == None:
        await interaction.response.send_message('Please specify a user')
    elif item == None:
        await interaction.response.send_message('Please specify an item')
    elif item not in ecosystem[interaction.guild.id]['settings']['items']:
        await interaction.response.send_message('That item does not exist')
    elif item not in ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items']:
        await interaction.response.send_message('You do not have that item')
    else:
        ecosystem[interaction.guild.id]['users'][str(user.id)]['inventory']['items'].append(item)
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['inventory']['items'].remove(item)
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'You have given {item} to {user.name}')


async def eco_add_item(interaction, item:str = None, price:int = None, role:discord.Role = None):
    """Add an item to the economy"""
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to do this')
                return
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if item == None:
        await interaction.response.send_message('Please specify an item')
    elif price == None:
        await interaction.response.send_message('Please specify a price')
    else:
        ecosystem[interaction.guild.id]['settings']['items'][item] = price
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'{item} has been added to the item list')
        if role != None:
            ecosystem[interaction.guild.id]['settings']['items']['role-'+item] = role.id
            json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)


async def eco_remove_item(interaction, item:str = None):
    """Remove an item from the economy"""
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to do this')
                return
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if item == None:
        await interaction.response.send_message('Please specify an item')
    elif item not in ecosystem[interaction.guild.id]['settings']['items']:
        await interaction.response.send_message('That item does not exist')
    else:
        ecosystem[interaction.guild.id]['settings']['items'].pop(item)
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'{item} has been removed from the item list')
        if 'role-'+item in ecosystem[interaction.guild.id]['settings']['items']:
            ecosystem[interaction.guild.id]['settings']['items'].pop('role-'+item)
            json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)


async def eco_set_price(interaction, item:str = None, price:int = None):
    """Set the price of an item"""
    for member in interaction.guild.members:
        if member.id == interaction.user.id:
            if not member.guild_permissions.administrator:
                await interaction.response.send_message('You do not have permission to do this')
                return
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if item == None:
        await interaction.response.send_message('Please specify an item')
    elif price == None:
        await interaction.response.send_message('Please specify a price')
    elif item not in ecosystem[interaction.guild.id]['settings']['items']:
        await interaction.response.send_message('That item does not exist')
    else:
        ecosystem[interaction.guild.id]['settings']['items'][item] = price
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)
        await interaction.response.send_message(f'{item}\'s price has been set to ${price}')


async def gamble(interaction, amount:int = None):
    """Gamble money"""
    if amount < 100:
        await interaction.response.send_message('You must gamble at least $100')
        return
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if amount == None:
        await interaction.response.send_message('Please specify an amount')
    elif amount > ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']:
        await interaction.response.send_message('You do not have enough money')
    else:
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= amount
        if random.randint(0, 1) == 1:
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount * 2
            await interaction.response.defer()
            await asyncio.sleep(1)
            balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
            await interaction.followup.send(f'You won ${amount * 2}\nYour new balance is {balance}')
        else:
            await interaction.response.defer()
            await asyncio.sleep(1)
            balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
            await interaction.followup.send(f'You lost ${amount}\nYour new balance is {balance}')
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)


async def slot(interaction, amount:int = None):
    """Play the slot machine"""
    if amount < 100:
        await interaction.response.send_message('You must gamble at least $100')
        return
    possible_emojis = ['🍇', '🍊', '🍒', '🍋', '🍉', '🍓', '🍍', '🍌', '🍐', '🍎']
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if amount == None:
        await interaction.response.send_message('Please specify an amount')
    elif amount > ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']:
        await interaction.response.send_message('You do not have enough money')
    else:
        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= amount
        emojis = []
        for i in range(3):
            emojis.append(random.choice(possible_emojis))
        if emojis[0] == emojis[1] and emojis[1] == emojis[2]:
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount * 3
            balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
            await interaction.response.defer()
            await asyncio.sleep(1)
            await interaction.followup.send(f'You won ${amount * 3} with {emojis[0]} {emojis[1]} {emojis[2]}\nYour new balance is {balance}')
        elif emojis[0] == emojis[1] or emojis[1] == emojis[2] or emojis[0] == emojis[2]:
            ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount * 2
            balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
            await interaction.response.defer()
            await asyncio.sleep(1)
            await interaction.followup.send(f'You won ${amount * 2} with {emojis[0]} {emojis[1]} {emojis[2]}\nYour new balance is {balance}')
        else:
            await interaction.response.defer()
            await asyncio.sleep(1)
            balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
            await interaction.followup.send(f'You lost ${amount} with {emojis[0]} {emojis[1]} {emojis[2]}\nYour new balance is {balance}')
        json.dump(ecosystem[interaction.guild.id], open(f'eco-{interaction.guild.id}.json', 'w'), indent=4)



async def bj(interaction, amount:int = None):
    """Play blackjack"""
    if amount < 100:
        await interaction.response.send_message('You must gamble at least $100')
        return
    hit_emoji = '🎲'
    stand_emoji = '🛑'
    allcards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    ecosystem[interaction.guild.id] = load_ecosystem(interaction.guild.id, interaction.user.id)
    if amount == None:
        await interaction.response.send_message('Please specify an amount')
    elif amount > ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']:
        await interaction.response.send_message('You do not have enough money')
    else:
        embed = discord.Embed(title='Blackjack', description='You have been dealt 1 card. Do you want to hit or stand?', color=0x00ff00)
        cards = []
        dealer_cards = []
        cards.append(random.choice(allcards))
        dealer_cards.append(random.choice(allcards))
        embed.add_field(name='Your cards', value=' '.join(cards))
        # Hide dealers cards with ?
        embed.add_field(name='Dealers cards', value='? ' + ' '.join(dealer_cards[1:]))
        embed.add_field(name='Your bet', value=f'${amount}')
        embed.set_footer(text='React with 🎲 to hit or 🛑 to stand')
        await interaction.response.send_message('Starting...')
        message = await interaction.followup.send(embed=embed)
        class BJView(discord.ui.View):
            @discord.ui.button(label='Hit', emoji=hit_emoji, custom_id='hit')
            async def hit(self, interaction, button):
                pass
            @discord.ui.button(label='Stand', emoji=stand_emoji, custom_id='stand')
            async def stand(self, interaction, button):
                pass
        await message.edit(view=BJView())
        def check(interactionn):
            print('lul')
            try:
                return interactionn.user == interaction.user and interactionn.message.id == message.id and interactionn.data['custom_id'] in ['hit', 'stand']
            except Exception as es:
                print(es)
                return False
        while True:
            try:
                interactionx = await client.wait_for('interaction', check=check, timeout=60)
            except:
                await interaction.response.send_message('Timed out')
            else:
                await interactionx.response.defer(ephemeral = True)
                # If the user hit, give them another card
                if interactionx.data['custom_id'] == 'hit':
                    cards.append(random.choice(allcards))
                    dealer_cards.append(random.choice(allcards))
                    embed = discord.Embed(title='Blackjack', description='You have been dealt 1 card. Do you want to hit or stand?', color=0x00ff00)
                    embed.add_field(name='Your cards', value=' '.join(cards))
                    # Hide dealers cards with ?
                    embed.add_field(name='Dealers cards', value='? ' + ' '.join(dealer_cards[1:]))
                    embed.add_field(name='Your bet', value=f'${amount}')
                    embed.set_footer(text='React with 🎲 to hit or 🛑 to stand')
                    await message.edit(embed=embed)
                    # Calculate the total value of the cards
                    total = 0
                    for card in cards:
                        if card in ['J', 'Q', 'K']:
                            total += 10
                        elif card == 'A':
                            total += 11
                        else:
                            total += int(card)
                    # If the total is over 21, and there is an ace, make it worth 1
                    if total > 21 and 'A' in cards:
                        total -= 10
                    # If the total is over 21, the user has lost
                    if total > 21:
                        # Remove the bet from the users balance
                        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= amount
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You lost\nYour new balance is {balance}')
                        # Show the dealers cards
                        embed = discord.Embed(title='Blackjack', description='You have been dealt 1 card. Do you want to hit or stand?', color=0x00ff00)
                        embed.add_field(name='Your cards', value=' '.join(cards))
                        embed.add_field(name='Dealers cards', value=' '.join(dealer_cards))
                        embed.add_field(name='Your bet', value=f'${amount}')
                        embed.set_footer(text='React with 🎲 to hit or 🛑 to stand')
                        await message.edit(embed=embed)
                        break
                    # If the total is 21, the user has won
                    elif total == 21:
                        # Add the bet to the users balance
                        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount * 2
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You won\nYour new balance is {balance}')
                        # Show the dealers cards
                        embed = discord.Embed(title='Blackjack', description='You have been dealt 1 card. Do you want to hit or stand?', color=0x00ff00)
                        embed.add_field(name='Your cards', value=' '.join(cards))
                        embed.add_field(name='Dealers cards', value=' '.join(dealer_cards))
                        embed.add_field(name='Your bet', value=f'${amount}')
                        embed.set_footer(text='React with 🎲 to hit or 🛑 to stand')
                        await message.edit(embed=embed)
                        break
                    # Calculate the total value of the dealers cards
                    dealer_total = 0
                    for card in dealer_cards:
                        if card in ['J', 'Q', 'K']:
                            dealer_total += 10
                        elif card == 'A':
                            dealer_total += 11
                        else:
                            dealer_total += int(card)
                    # If the total is over 21, and there is an ace, make it worth 1
                    if dealer_total > 21 and 'A' in dealer_cards:
                        dealer_total -= 10
                    # If the total is over 21, the user has won
                    if dealer_total > 21:
                        # Add the bet to the users balance
                        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You won\nYour new balance is {balance}')
                        # Show the dealers cards
                        embed = discord.Embed(title='Blackjack', description='You have been dealt 1 card. Do you want to hit or stand?', color=0x00ff00)
                        embed.add_field(name='Your cards', value=' '.join(cards))
                        embed.add_field(name='Dealers cards', value=' '.join(dealer_cards))
                        embed.add_field(name='Your bet', value=f'${amount}')
                        embed.set_footer(text='React with 🎲 to hit or 🛑 to stand')
                        await message.edit(embed=embed)
                        break
                    # If the total is 21, the user has lost
                    elif dealer_total == 21:
                        # Remove the bet from the users balance
                        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= amount
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You lost\nYour new balance is {balance}')
                        # Show the dealers cards
                        embed = discord.Embed(title='Blackjack', description='You have been dealt 1 card. Do you want to hit or stand?', color=0x00ff00)
                        embed.add_field(name='Your cards', value=' '.join(cards))
                        embed.add_field(name='Dealers cards', value=' '.join(dealer_cards))
                        embed.add_field(name='Your bet', value=f'${amount}')
                        embed.set_footer(text='React with 🎲 to hit or 🛑 to stand')
                        await message.edit(embed=embed)
                        break
                elif interactionx.data['custom_id'] == 'stand':
                    embed = discord.Embed(title='Blackjack', description='You have been dealt 1 card. Do you want to hit or stand?', color=0x00ff00)
                    embed.add_field(name='Your cards', value=' '.join(cards))
                    # Hide dealers cards with ?
                    embed.add_field(name='Dealers cards', value='? ' + ' '.join(dealer_cards[1:]))
                    embed.add_field(name='Your bet', value=f'${amount}')
                    embed.set_footer(text='React with 🎲 to hit or 🛑 to stand')
                    await message.edit(embed=embed)
                    # Show the dealers cards
                    embed = discord.Embed(title='Blackjack', description='You have been dealt 1 card. Do you want to hit or stand?', color=0x00ff00)
                    embed.add_field(name='Your cards', value=' '.join(cards))
                    embed.add_field(name='Dealers cards', value=' '.join(dealer_cards))
                    embed.add_field(name='Your bet', value=f'${amount}')
                    embed.set_footer(text='React with 🎲 to hit or 🛑 to stand')
                    await message.edit(embed=embed)
                    # Calculate the total value of the cards
                    total = 0
                    for card in cards:
                        if card in ['J', 'Q', 'K']:
                            total += 10
                        elif card == 'A':
                            total += 11
                        else:
                            total += int(card)
                    # If the total is over 21, and there is an ace, make it worth 1
                    if total > 21 and 'A' in cards:
                        total -= 10
                    # Calculate the total value of the dealers cards
                    dealer_total = 0
                    for card in dealer_cards:
                        if card in ['J', 'Q', 'K']:
                            dealer_total += 10
                        elif card == 'A':
                            dealer_total += 11
                        else:
                            dealer_total += int(card)
                    # If the total is over 21, and there is an ace, make it worth 1
                    if dealer_total > 21 and 'A' in dealer_cards:
                        dealer_total -= 10
                    # If the total is over 21, the user has won
                    if dealer_total > 21:
                        # Add the bet to the users balance
                        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You won\nYour new balance is {balance}')
                        break
                    # If the total is 21, the user has lost
                    elif dealer_total == 21:
                        # Remove the bet from the users balance
                        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= amount
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You lost\nYour new balance is {balance}')
                        break
                    # If the total is higher than the dealers, the user has won
                    elif total > dealer_total:
                        # Add the bet to the users balance
                        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] += amount
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You won\nYour new balance is {balance}')
                        break
                    # If the total is lower than the dealers, the user has lost
                    elif total < dealer_total:
                        # Remove the bet from the users balance
                        ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance'] -= amount
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You lost\nYour new balance is {balance}')
                        break
                    # If the total is the same as the dealers, the user has tied
                    elif total == dealer_total:
                        await asyncio.sleep(1)
                        balance = ecosystem[interaction.guild.id]['users'][str(interaction.user.id)]['balance']
                        await interaction.followup.send(f'You tied\nYour new balance is {balance}')
                        break
    # Save
    with open('eco-' + str(interaction.guild.id) + '.json', 'w') as f:
        json.dump(ecosystem[interaction.guild.id], f)


# Status: Playing with x members
# Update every 10 seconds

async def status_task():
    while True:
        try:
            await client.change_presence(activity=discord.Game(name=f'with {len(client.users)} users'))
        except:
            pass
        await asyncio.sleep(10)


    





command_help = {
    'moderation': {
        'commands': {
            'moderation addautorole': {
                'parameters': {
                    'role': {
                        'description': 'The role to add to new members',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Adds a role to new members',
            },
            'moderation addreactionrole': {
                'parameters': {
                    'message_link': {
                        'description': 'The link to the message to add the reaction role to',
                        'required': True,
                        'type': 'string'
                    },
                    'emoji': {
                        'description': 'The emoji to add to the message',
                        'required': True,
                        'type': 'string'
                    },
                    'role': {
                        'description': 'The role to add to the user when they react',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Adds a reaction role to a message',
            },
            'moderation addselfrole': {
                'parameters': {
                    'role': {
                        'description': 'The role to add to the user when they react',
                        'required': True,
                        'type': 'role'
                    },
                    'description': {
                        'description': 'The description of the role',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Adds a self role to the server',
            },
            'moderation assignrole': {
                'parameters': {
                    'user': {
                        'description': 'The user to assign the role to',
                        'required': True,
                        'type': 'user'
                    },
                    'role': {
                        'description': 'The role to assign to the user',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Assigns a role to a user',
            },
            'moderation ban': {
                'parameters': {
                    'member': {
                        'description': 'The member to ban',
                        'required': True,
                        'type': 'member'
                    },
                    'reason': {
                        'description': 'The reason for the ban',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Bans a member from the server',
            },
            'moderation createchannel': {
                'parameters': {
                },
                'description': 'Creates a channel',
            },
            'moderation createrole': {
                'parameters': {
                },
                'description': 'Creates a role',
            },
            'moderation deletechannel': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to delete',
                        'required': True,
                        'type': 'channel'
                    }
                },
                'description': 'Deletes a channel',
            },
            'moderation deleterole': {
                'parameters': {
                    'role': {
                        'description': 'The role to delete',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Deletes a role',
            },
            'moderation editchannel': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to edit',
                        'required': True,
                        'type': 'channel'
                    }
                },
                'description': 'Edits a channel',
            },
            'moderation editrole': {
                'parameters': {
                    'role': {
                        'description': 'The role to edit',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Edits a role',
            },
            'moderation kick': {
                'parameters': {
                    'member': {
                        'description': 'The member to kick',
                        'required': True,
                        'type': 'member'
                    },
                    'reason': {
                        'description': 'The reason for the kick',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Kicks a member from the server',
            },
            'moderation nuke': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to nuke',
                        'required': True,
                        'type': 'channel'
                    }
                },
                'description': 'Nukes a channel',
            },
            'moderation purge': {
                'parameters': {
                    'amount': {
                        'description': 'The amount of messages to purge',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Purges messages from the channel',
            },
            'moderation removeautorole': {
                'parameters': {
                    'role': {
                        'description': 'The role to remove from new members',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Removes a role fomr the list of auto-roles'
            },
            'moderation removereactionrole': {
                'parameters': {
                    'message_link': {
                        'description': 'The link to the message to remove the reaction role from',
                        'required': True,
                        'type': 'string'
                    },
                    'emoji': {
                        'description': 'The emoji to remove from the message',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Removes a reaction role from a message',
            },
            'moderation removerole': {
                'parameters': {
                    'user': {
                        'description': 'The user to remove the role from',
                        'required': True,
                        'type': 'user'
                    },
                    'role': {
                        'description': 'The role to remove from the user',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Removes a role from a user',
            },
            'moderation removeselfrole': {
                'parameters': {
                    'role': {
                        'description': 'The role to add to the user when they react',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Removes a self role from the server',
            },
            'moderation selfroles': {
                'parameters': {
                },
                'description': 'Lists all self roles',
            },
            'moderation setboostmessage': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to send the boost message in',
                        'required': True,
                        'type': 'channel'
                    },
                    'message': {
                        'description': 'The message to send when a member boosts the server',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Sets the message to send when a member boosts the server',
            },
            'moderation unban': {
                'parameters': {
                    'user': {
                        'description': 'The user to unban',
                        'required': True,
                        'type': 'user'
                    }
                },
                'description': 'Unbans a user from the server',
            },
            'moderation addroletoall': {
                'parameters': {
                    'role': {
                        'description': 'The role to add to all members',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Adds a role to all members',
            },
            'moderation removerolefromall': {
                'parameters': {
                    'role': {
                        'description': 'The role to remove from all members',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Removes a role from all members',
            },
            'moderation autodelete': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to enable auto-delete in',
                        'required': True,
                        'type': 'channel'
                    },
                    'time': {
                        'description': 'The time to wait before deleting messages',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Enables auto-delete in a channel',
            },
            'moderation autoping': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to enable auto-ping in',
                        'required': True,
                        'type': 'channel'
                    }
                },
                'description': 'En|Disables auto-ping in a channel',
            },
        },
        'information': 'Moderation'
    },
    'automod': {
        'commands': {
            'automod block add': {
                'parameters': {
                    'word': {
                        'description': 'The word / regex to block',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Adds a word / regex to the block list',
            },
            'automod block remove': {
                'parameters': {
                    'word': {
                        'description': 'The word / regex to unblock',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Removes a word / regex from the block list',
            },
            'automod block list': {
                'parameters': {
                },
                'description': 'Lists all blocked words / regex',
            },
            'automod ai activate': {
                'parameters': {
                },
                'description': 'Activate Artificial Intelligence',
            },
            'automod ai deactivate': {
                'parameters': {
                },
                'description': 'Deactivate Artificial Intelligence',
            }
        },
        'information': 'Automod'
    },
    'invite': {
        'commands': {
            'invite addrole': {
                'parameters': {
                    'invites': {
                        'description': 'The amount of invites required to get the role',
                        'required': True,
                        'type': 'int'
                    },
                    'role': {
                        'description': 'The role to give to the user',
                        'required': True,
                        'type': 'role'
                    },
                    'reverse': {
                        'description': 'If the role should be removed when the user reachs the invite amount',
                        'required': False,
                        'type': 'bool'
                    }
                },
                'description': 'Adds a role to a user when they reach a certain amount of invites',
            },
            'invite addinvites': {
                'parameters': {
                    'user': {
                        'description': 'The user to add invites to',
                        'required': True,
                        'type': 'user'
                    },
                    'invites': {
                        'description': 'The amount of invites to add',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Adds invites to a user',
            },
            'invite cleanupinvites': {
                'parameters': {
                },
                'description': 'Deletes all invites from the server',
            },
            'invite roles': {
                'parameters': {
                },
                'description': 'Shows all invite roles',
            },
            'invite check': {
                'parameters': {
                    'user': {
                        'description': 'The user to show invites for',
                        'required': False,
                        'type': 'user'
                    }
                },
                'description': 'Shows the invites of a user',
            },
            'invite leaderboard': {
                'parameters': {
                },
                'description': 'Shows the invite leaderboard',
            },
            'invite removerole': {
                'parameters': {
                    'invites': {
                        'description': 'The amount of invites required to get the role',
                        'required': True,
                        'type': 'int'
                    },
                    'role': {
                        'description': 'The role to give to the user',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Remove a role from the list of roles to give to a user if they reach a specific amount of invites.'
            },
            'invite removeinvites': {
                'parameters': {
                    'user': {
                        'description': 'The user to remove invites from',
                        'required': True,
                        'type': 'user'
                    },
                    'invites': {
                        'description': 'The amount of invites to remove',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Removes invites from a user',
            },
            'invite resetinvites': {
                'parameters': {
                    'user': {
                        'description': 'The user to reset invites for',
                        'required': True,
                        'type': 'user'
                    }
                },
                'description': 'Resets the invites of a user',
            },
            'invite setscreen': {
                'parameters': {
                    'invites': {
                        'description': 'If the invites shall be displayed',
                        'required': True,
                        'type': 'bool'
                    },
                    'joins': {
                        'description': 'If the joins shall be displayed',
                        'required': True,
                        'type': 'bool'
                    },
                    'leaves': {
                        'description': 'If the leaves shall be displayed',
                        'required': True,
                        'type': 'bool'
                    }
                },
                'description': 'Sets the invites screen',
            },
            'invite setjoin': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to send the join message in',
                        'required': True,
                        'type': 'channel'
                    },
                    'embed': {
                        'description': 'If the join message shall be an embed',
                        'required': True,
                        'type': 'bool'
                    }
                },
                'description': 'Sets the join message',
            },
            'invite setleave': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to send the leave message in',
                        'required': True,
                        'type': 'channel'
                    },
                    'embed': {
                        'description': 'If the leave message shall be an embed',
                        'required': True,
                        'type': 'bool'
                    }
                },
                'description': 'Sets the leave message',
            },
            'invite setwelcomeimage': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to send the welcome image in',
                        'required': True,
                        'type': 'channel'
                    }
                },
                'description': 'Sets the welcome image',
            }
        },
        'information': 'Invite Management'
    },
    'antinuke': {
        'commands': {
            'antinuke allowbypass': {
                'parameters': {
                    'bot': {
                        'description': 'The bot to allow to bypass the antinuke',
                        'required': True,
                        'type': 'user'
                    }
                },
                'description': 'Allows a bot to bypass the antinuke',
            },
            'antinuke disallowbypass': {
                'parameters': {
                    'bot': {
                        'description': 'The bot to disallow to bypass the antinuke',
                        'required': True,
                        'type': 'user'
                    }
                },
                'description': 'Disallows a bot to bypass the antinuke',
            },
            'antinuke setcaptcha': {
                'parameters': {
                    'enabled': {
                        'description': 'If the captcha should be enabled',
                        'required': False,
                        'type': 'bool'
                    }
                },
                'description': 'Sets if users should solve a captcha when they join the server'
            },
            'antinuke memberbackup': {
                'parameters': {
                    'action': {
                        'description': 'The action to perform',
                        'required': True,
                        'type': 'string'
                    },
                    'newguild': {
                        'description': 'The guild to move the members to',
                        'required': False,
                        'type': 'guild'
                    },
                    'message': {
                        'description': 'The message to send to the members',
                        'required': False,
                        'type': 'string'
                    },
                    'role': {
                        'description': 'The role to add to the members',
                        'required': False,
                        'type': 'role'
                    }
                },
                'description': 'Backs up all members in the server',
            }
        },
        'information': 'Anti-Nuke System'
    },
    'freenitro': {
        'commands': {
            'allowfree': {
                'parameters': {
                    'allow': {
                        'description': 'If the server members should be able to send free nitro emojis',
                        'required': False,
                        'type': 'bool'
                    }
                },
                'description': 'Allows the server members to send free nitro emojis',
            },
        },
        'information': 'Free Nitro Emojis'
    },
    'stock': {
        'commands': {
            'stock enable': {
                'parameters': {
                    'allow': {
                        'description': 'If stock should be enabled in the server',
                        'required': False,
                        'type': 'bool'
                    }
                },
                'description': 'Allows server stock for this server.'
            },
            'stock generate': {
                'parameters': {
                    'account_type': {
                        'description': 'The type of account to generate',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Generates a stock account'
            },
            'stock removerole': {
                'parameters': {
                    'account_type': {
                        'description': 'The type of account to remove the role from',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Removes the stock role from a type of account'
            },
            'stock setrole': {
                'parameters': {
                    'account_type': {
                        'description': 'The type of account to set the role for',
                        'required': True,
                        'type': 'string'
                    },
                    'role': {
                        'description': 'The role to set for the account type',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Sets the stock role for a type of account'
            },
            'stock show': {
                'parameters': {
                },
                'description': 'Shows the stock of the server'
            },
            'stock upload': {
                'parameters': {
                    'account_type': {
                        'description': 'The type of account to upload',
                        'required': True,
                        'type': 'string'
                    },
                    'file': {
                        'description': 'The file to upload',
                        'required': True,
                        'type': 'file'
                    }
                },
                'description': 'Uploads a stock file'
            },
            'stock setdelay': {
                'parameters': {
                    'delay': {
                        'description': 'The delay in seconds',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Sets the delay between stock generations'
            }
        },
        'information': 'Account Generator / Stock System'
    },
    'giveaway': {
        'commands': {
            'giveaway drop': {
                'parameters': {
                },
                'description': 'Drop a message to the first user who clicks on claim'
            },
            'giveaway start': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to send the giveaway to',
                        'required': True,
                        'type': 'channel'
                    },
                    'sponsor': {
                        'description': 'The invite link to the giveaway sponsor\'s server',
                        'required': False,
                        'type': 'string'
                    }
                },
                'description': 'Create a giveaway'
            },
            'giveaway setboostchance': {
                'parameters': {
                    'chance': {
                        'description': 'The chance of boosters at giveaways',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Sets the chance of boosters at giveaways'
            },
        },
        'information': 'Giveaways'
    },
    'fun': {
        'commands': {
            'fun embed': {
                'parameters': {
                },
                'description': 'Create an embed'
            },
            'fun img': {
                'parameters': {
                    'text': {
                        'description': 'The text to generate the image from',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Generate an image from text'
            },
            'fun face': {
                'parameters': {
                },
                'description': 'Create a random human face',
            },
            'fun review': {
                'parameters': {
                    'website_url': {
                        'description': 'The website url to review',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Review a website'
            },
            'fun ping': {
                'parameters': {
                },
                'description': 'Shows the bot ping'
            },
            'fun poll': {
                'parameters': {
                    'type_of_poll': {
                        'description': 'The type of poll to create (text)',
                        'required': False,
                        'type': 'string'
                    },
                },
                'description': 'Create a poll'
            },
            'fun qa': {
                'parameters': {
                    'question': {
                        'description': 'The question to ask',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Reply to a question with an answer'
            },
            'fun search': {
                'parameters': {
                    'query': {
                        'description': 'The query to search for',
                        'required': True,
                        'type': 'string'
                    },
                    'typeof': {
                        'description': 'The type of search to perform',
                        'required': False,
                        'type': 'string'
                    }
                },
                'description': 'Search for something'
            },
            'fun checkshop': {
                'parameters': {
                    'website_url': {
                        'description': 'The website url to check',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Checks if a shop website is legit'
            },
            'fun hideinvites': {
                'parameters': {
                    'message': {
                        'description': 'Message to send',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Hide all discord invites in message'
            },
            'fun messagebuilder': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to send the message to',
                        'required': True,
                        'type': 'channel'
                    },
                    'message': {
                        'description': 'Message to send',
                        'required': False,
                        'type': 'string'
                    },
                    'embed': {
                        'description': 'Does the message contain an embed or not',
                        'required': False,
                        'type': 'boolean'
                    },
                    'title': {
                        'description': 'The title of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'description': {
                        'description': 'The description of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'color': {
                        'description': 'The color of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'footer': {
                        'description': 'The footer of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'image': {
                        'description': 'The image of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'thumbnail': {
                        'description': 'The thumbnail of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'author': {
                        'description': 'The author of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'author_icon': {
                        'description': 'The icon of the author of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'author_url': {
                        'description': 'The url of the author of the embed',
                        'required': False,
                        'type': 'string'
                    },
                    'fields': {
                        'description': 'The amount of fields of the embed',
                        'required': False,
                        'type': 'int'
                    },
                    'buttons': {
                        'description': 'The amount of buttons of the message',
                        'required': False,
                        'type': 'int'
                    },
                    'selects': {
                        'description': 'The amount of selects of the message',
                        'required': False,
                        'type': 'int'
                    }
                },
                'description': 'Build + Send a message'
            },
            'fun sendas': {
                'parameters': {
                    'user': {
                        'description': 'The user to send the message as',
                        'required': True,
                        'type':'string'
                    },
                    'message': {
                        'description': 'The message to send',
                        'required': False,
                        'type':'string'
                    },
                    'file': {
                        'description': 'The file to send',
                        'required': False,
                        'type':'string'
                    }
                },
                'description': 'Send a message as another user'
            }
        },
        'information': 'Fun'
    },
    'music': {
        'commands': {
            'music loop': {
                'parameters': {
                },
                'description': 'Loops the current song'
            },
            'music pause': {
                'parameters': {
                },
                'description': 'Pauses the current song'
            },
            'music playlist': {
                'parameters': {
                    'what': {
                        'description': 'The action to perform',
                        'required': True,
                        'type': 'string'
                    },
                    'song': {
                        'description': 'The song to perform the action on',
                        'required': False,
                        'type': 'string'
                    }
                },
                'description': 'Manages the playlist'
            },
            'music queue': {
                'parameters': {
                },
                'description': 'Shows the queue'
            },
            'music remove': {
                'parameters': {
                    'song': {
                        'description': 'The song to remove',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Removes a song from the queue'
            },
            'music removeall': {
                'parameters': {
                },
                'description': 'Removes all songs from the queue'
            },
            'music resume': {
                'parameters': {
                },
                'description': 'Resumes the current song'
            },
            'music shuffle': {
                'parameters': {
                },
                'description': 'Shuffles the queue'
            },
            'music skip': {
                'parameters': {
                },
                'description': 'Skips the current song'
            },
            'music record start': {
                'parameters': {
                },
                'description': 'Start recording your voice'
            },
            'music record stop': {
                'parameters': {
                },
                'description': 'Stop recording your voice'
            },
        },
        'information': 'Music'
    },
    'buttons': {
        'information': 'All help about buttons at messagebuilder'
    },
    'game': {
        'commands': {
            'game activity': {
                'parameters': {
                    'game': 'The game to play',
                    'type': 'string',
                    'required': True
                },
                'description': 'Play a game'
            },
            'game tod truth': {
                'parameters': {
                },
                'description': 'Ask a truth question'
            },
            'game tod dare': {
                'parameters': {
                },
                'description': 'Ask a dare question'
            }
        },
        'information': 'Games'
    },
    'economy': {
        'commands': {
            'economy balance': {
                'parameters': {
                },
                'description': 'Shows your balance'
            },
            'economy daily': {
                'parameters': {
                },
                'description': 'Claim your daily reward'
            },
            'economy deposit': {
                'parameters': {
                    'amount': {
                        'description': 'The amount to deposit',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Deposit money to your bank'
            },
            'economy withdraw': {
                'parameters': {
                    'amount': {
                        'description': 'The amount to withdraw',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Withdraw money from your bank'
            },
            'economy pay': {
                'parameters': {
                    'user': {
                        'description': 'The user to pay',
                        'required': True,
                        'type': 'user'
                    },
                    'amount': {
                        'description': 'The amount to pay',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Pay someone'
            },
            'economy shop': {
                'parameters': {
                },
                'description': 'Shows the shop'
            },
            'economy buy': {
                'parameters': {
                    'item': {
                        'description': 'The item to buy',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Buy an item'
            },
            'economy inventory': {
                'parameters': {
                },
                'description': 'Shows your inventory'
            },
            'economy sell': {
                'parameters': {
                    'item': {
                        'description': 'The item to sell',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Sell an item'
            },
            'economy leaderboard': {
                'parameters': {
                },
                'description': 'Shows the eco leaderboard'
            },
            'economy rob': {
                'parameters': {
                    'user': {
                        'description': 'The user to rob',
                        'required': True,
                        'type': 'user'
                    }
                },
                'description': 'Rob someone'
            },
            'economy admin reset': {
                'parameters': {
                },
                'description': 'Reset your eco'
            },
            'economy admin set': {
                'parameters': {
                    'user': {
                        'description': 'The user to set the eco of',
                        'required': True,
                        'type': 'user'
                    },
                    'amount': {
                        'description': 'The amount to set the eco to',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Set the eco of a user'
            },
            'economy admin add_coins': {
                'parameters': {
                    'user': {
                        'description': 'The user to add the eco to',
                        'required': True,
                        'type': 'user'
                    },
                    'amount': {
                        'description': 'The amount to add to the eco',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Add to the eco of a user'
            },
            'economy admin remove_coins': {
                'parameters': {
                    'user': {
                        'description': 'The user to remove the eco from',
                        'required': True,
                        'type': 'user'
                    },
                    'amount': {
                        'description': 'The amount to remove from the eco',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Remove from the eco of a user'
            },
            'economy admin give': {
                'parameters': {
                    'user': {
                        'description': 'The user to give the item to',
                        'required': True,
                        'type': 'user'
                    },
                    'item': {
                        'description': 'The item to give',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Give an item to a user'
            },
            'economy admin add_item': {
                'parameters': {
                    'item': {
                        'description': 'The item to add',
                        'required': True,
                        'type': 'string'
                    },
                    'price': {
                        'description': 'The price of the item',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Add an item to the shop'
            },
            'economy admin remove_item': {
                'parameters': {
                    'item': {
                        'description': 'The item to remove',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Remove an item from the shop'
            },
            'economy admin price': {
                'parameters': {
                    'item': {
                        'description': 'The item to set the price of',
                        'required': True,
                        'type': 'string'
                    },
                    'price': {
                        'description': 'The price to set the item to',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Set the price of an item'
            },
            'economy gamble': {
                'parameters': {
                    'amount': {
                        'description': 'The amount to gamble',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Gamble your money'
            },
            'economy slot': {
                'parameters': {
                    'amount': {
                        'description': 'The amount to gamble',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Gamble your money on the slot machine'
            }
        },
        'information': 'Economy'
    },
    'xp': {
        'commands': {
            'xp level': {
                'parameters': {
                    'user': {
                        'description': 'The user to get the level of',
                        'required': False,
                        'type': 'user'
                    }
                },
                'description': 'Get your level'
            },
            'xp addreward': {
                'parameters': {
                    'level': {
                        'description': 'The level to add the reward to',
                        'required': True,
                        'type': 'int'
                    },
                    'role': {
                        'description': 'The role to add as the reward',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Add a reward to a level'
            },
            'xp removereward': {
                'parameters': {
                    'level': {
                        'description': 'The level to remove the reward from',
                        'required': True,
                        'type': 'int'
                    },
                    'role': {
                        'description': 'The role to remove as the reward',
                        'required': True,
                        'type': 'role'
                    }
                },
                'description': 'Remove a reward from a level'
            },
            'xp rewards': {
                'parameters': {
                },
                'description': 'Shows the xp rewards'
            },
            'xp addxp': {
                'parameters': {
                    'user': {
                        'description': 'The user to add the xp to',
                        'required': True,
                        'type': 'user'
                    },
                    'amount': {
                        'description': 'The amount of xp to add',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Add xp to a user'
            },
            'xp removexp': {
                'parameters': {
                    'user': {
                        'description': 'The user to remove the xp from',
                        'required': True,
                        'type': 'user'
                    },
                    'amount': {
                        'description': 'The amount of xp to remove',
                        'required': True,
                        'type': 'int'
                    }
                },
                'description': 'Remove xp from a user'
            },
            'xp leaderboard': {
                'parameters': {
                },
                'description': 'Shows the xp leaderboard'
            },
            'xp setchannel': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to set the xp channel to',
                        'required': False,
                        'type': 'channel'
                    },
                    'extra': {
                        'description': 'The extra value',
                        'required': False,
                        'type': 'string'
                    }
                },
                'description': 'Set the xp channel'
            }
        },
        'information': 'XP'
    },
    'stats': {
        'commands': {
            'setmembers': {
                'parameters': {
                    'name': {
                        'description': 'The name to set the member count to',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Set the member count channel name, {count} will be replaced with the member count'
            },
            'setbots': {
                'parameters': {
                    'name': {
                        'description': 'The name to set the bot count to',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Set the bot count channel name, {count} will be replaced with the bot count'
            },
            'setonline': {
                'parameters': {
                    'name': {
                        'description': 'The name to set the online count to',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Set the online count channel name, {count} will be replaced with the online count'
            },
            'setoffline': {
                'parameters': {
                    'name': {
                        'description': 'The name to set the offline count to',
                        'required': True,
                        'type': 'string'
                    },
                },
                'description': 'Set the offline count channel name, {count} will be replaced with the offline count'
            },
            'setboosters': {
                'parameters': {
                    'name': {
                        'description': 'The name to set the booster count to',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Set the booster count channel name, {count} will be replaced with the booster count'
            },
            'setboostlevel': {
                'parameters': {
                    'name': {
                        'description': 'The name to set the boost level to',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Set the boost level channel name, {count} will be replaced with the boost level'
            },
            'setboosttiers': {
                'parameters': {
                    'name': {
                        'description': 'The name to set the boost tier to',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Set the boost tier channel name, {count} will be replaced with the boost tier'
            },
            'setadmins': {
                'parameters': {
                    'name': {
                        'description': 'The name to set the admin count to',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Set the admin count channel name, {count} will be replaced with the admin count'
            },
        },
        'information': 'Server Stats'
    },
    'autoresponse': {
        'commands': {
            'autoresponse add': {
                'parameters': {
                    'message': {
                        'description': 'The trigger to add',
                        'required': True,
                        'type': 'string'
                    },
                    'response': {
                        'description': 'The response to add {user}, {guild}, {channel},\n{$1}, {$2}, {$3}, {$4}, {$5}, {$6}, {$7}, {$8}, {$9},\n{$$1}, {$$2}, {$$3}, {$$4}, {$$5}, {$$6}, {$$7}, {$$8}, {$$9} are valid',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Add an autoresponse'
            },
            'autoresponse remove': {
                'parameters': {
                    'message': {
                        'description': 'The trigger to remove',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Remove an autoresponse'
            },
            'autoresponse list': {
                'parameters': {
                },
                'description': 'List all autoresponses'
            },
        },
        'information': 'Autoresponses | Custom commands'
    },
    'backup': {
        'commands': {
            'backup create': {
                'parameters': {
                },
                'description': 'Create a backup'
            },
            'backup list': {
                'parameters': {
                },
                'description': 'List all backups'
            },
            'backup restore': {
                'parameters': {
                    'backup_id': {
                        'description': 'The backup to restore',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Restore a backup'
            }
        },
        'information': 'Backups'
    },
    'share': {
        'commands': {
            'share setup': {
                'parameters': {
                },
                'description': 'Setup the share system'
            },
            'share bump': {
                'parameters': {
                },
                'description': 'Bump the server'
            },
            'share rewards': {
                'parameters': {
                    'reward': {
                        'description': 'The reward to edit, delete',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'View / edit / delete bump rewards'
            }
        },
        'information': 'Share system'
    },
    'announce': {
        'commands': {
            'announce twitch': {
                'parameters': {
                    'channel': {
                        'description': 'The channel to announce in',
                        'required': True,
                        'type': 'channel'
                    },
                    'name': {
                        'description': 'The streamers name to announce',
                        'required': True,
                        'type': 'string'
                    },
                    'follow': {
                        'description': 'Shall announcements be sent when the streamer goes live',
                        'required': True,
                        'type': 'boolean'
                    }
                },
                'description': 'Announce a twitch stream'
            },
        },
        'information': 'Announcements'
    },
    'meme': {
        'commands': {
           'create': {
                'parameters': {
                    'topText': {
                        'description': 'The top text of the meme',
                        'required': True,
                        'type': 'string'
                    },
                    'bottomText': {
                        'description': 'The bottom text of the meme',
                        'required': True,
                        'type': 'string'
                    },
                    'imgUrl': {
                        'description': 'The image url of the meme',
                        'required': True,
                        'type': 'string'
                    }
                },
                'description': 'Create a meme'
            },
            'random': {
                'parameters': {
                },
                'description': 'Get a random meme'
            }
        },
        'information': 'Memes'
    }
}

# start bot
client.run(TOKEN)

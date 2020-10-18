import os
import random
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from dotenv import load_dotenv
from scraper import anime_desc,anime_info,anime_search,anime_recommend,anime_trailer,anime_song
from utils import easyembed,helpstring
import asyncio
from youtube_search import YoutubeSearch
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='#')
players = {}

@bot.command(name='anime',brief='==> anime/manga + a little bit of music bot',
	help=helpstring)
async def cool_bot(ctx,*args):
	if len(args) >1 :
		if args[0] == 'desc':
			anime = " ".join(args[1:])
			response,img = anime_desc(anime)
			embed = easyembed(bot,"anime description",response,img)
			await ctx.send(embed = embed)
		elif args[0] == 'info':
			anime = " ".join(args[1:])
			response,img = anime_info(anime)
			embed = easyembed(bot , "anime information" , response,img )
			await ctx.send(embed = embed)
		elif args[0] == 'search':
			anime = " ".join(args[1:])
			anime_list = anime_search(anime)
			anime_list_str = ""
			i = 1
			for row in anime_list:
				anime_list_str = anime_list_str+str(i)+". "+row+"\n"
				i = i + 1
			embed = easyembed(bot , "anime search" , anime_list_str )
			await ctx.send(embed = embed)
		elif args[0] == 'recommend':
			anime = " ".join(args[1:])
			anime_list = anime_recommend(anime)
			anime_list_str = ""
			i = 1
			for row in anime_list:
				anime_list_str = anime_list_str+str(i)+". "+row+"\n"
				i = i + 1
			embed = easyembed(bot,"anime recommendations",anime_list_str)
			await ctx.send(embed = embed)
		elif args[0] == 'trailer':
			anime = " ".join(args[1:])
			links = anime_trailer(anime)
			description = ""
			i = 1
			for link in links:
				description += str(i) + ". " +  link + "\n"
				i += 1
			embed = easyembed(bot,"anime trailers" , description)
			await ctx.send(embed=embed)
		elif args[0] == 'song':
			anime = " ".join(args[1:])
			anime_song_str = anime_song(anime)
			embed = easyembed(bot,"anime openings and endings",anime_song_str)
			await ctx.send(embed = embed)
		elif args[0] == 'play':
			search_query = " ".join(args[1:])
			server = ctx.guild
			user = ctx.message.author
			voiceState = user.voice
			if not voiceState :
				await ctx.send('You must be in a voice channel to invoke this command 🔇')
				return
			voiceChannel = voiceState.channel
			voiceClient = await voiceChannel.connect()
			YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
			FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn' , }
			results = YoutubeSearch(search_query, max_results=10).to_json()
			results = json.loads(results)
			url_suffix = results['videos'][0]['url_suffix']
			video_title = results['videos'][0]['title']
			thumbnail = results['videos'][0]['thumbnails'][0]
			url = 'https://www.youtube.com' + url_suffix 
			with YoutubeDL(YDL_OPTIONS) as ydl:
				info = ydl.extract_info(url, download=False)
			URL = info['formats'][-1]['url']
			await ctx.send(embed = easyembed(bot,'Music Time 🔈🔉🔊',"playing song " + video_title + "..." , thumbnailurl = 'no' , imgurl = thumbnail))
			voiceClient.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
			while voiceClient.is_playing():
				await asyncio.sleep(1)
			await voiceClient.disconnect()
			print('bot has left voice channel')
		else :
			await ctx.send('invalid ❌')	
	elif len(args) == 1:
		if args[0] == 'owner':
			await ctx.send('I was Coded by Yajurmani and Shreikthegod 😳')
		else :
			await ctx.send('invalid ❌')
	else:
		await ctx.send('invalid Command ❌')	

@bot.event
async def on_ready():
	print("Bot is ready now !")

bot.run(TOKEN)

import discord
from discord.ext import commands, tasks
import aiohttp
import markovify
import random
import asyncio
import time

STATE = "FIRST_WORD/S_ONLY"
state_types = ["FIRST_WORD/S_ONLY","FIRST_OR_LAST","FIRST_ONLY","LAST_ONLY","RANDOM"]

# /home/dazzix/discordbot/markov/servers/
bot = commands.Bot(command_prefix="mk-", description="MarkovBot is a chatbot that uses markov chains to generate respones. Every message sent in all channels that the bot has permission to view, will be added to the bot's source text. To start a conversation, create a channel named \"markovbot\". The bot will respond based on either the first word/s or last word of a message sent (depending on the bot's choosing state). If the bot reacts to your message with a :markov_what: emote, it would most likely imply that the bot hasn't learned that much messages yet and must require more messages to learn from. - dazziX")

# excuses = ["``I can't seem to understand what you are trying to say.``", "``Sorry, I don't know what that means.``", "``ERROR 404 - WORD NOT FOUND``", "``I haven't learned that word yet, sorry...``", "``Excuse me but, what are you trying to say.``", "``markovbot.errors.MarkovException: Cannot construct sentence of specified word/s``"]
"""
def readtxt(server):
	textr = open("/home/dazzix/discordbot/markov/servers/{}.txt".format(str(server)), encoding='utf-16').read()

	return textr
"""

model = None

def addIn(mes, sid):
	with open('servers/{}.txt'.format(str(sid)), 'a+', encoding='utf-16') as txt:
		txt.write(mes + '\n')

def textChain(gid):
	sen = model.make_sentence(tries=50)
	return sen

def wordChain(word, bid):
	try:
		sn = model.make_sentence_with_start(word, strict=False, tries=50)
	except:
		return None
	else:
		return sn

async def refresh():
	global model
	while True:
		t1 = time.time()
		print('Loading source text...')
		with open('servers/438590624162250752.txt', 'r', encoding='utf-16') as f:
			text = f.read()

		model = markovify.NewlineText(text)
		num_lines = str(len(text.splitlines()))
		elapsed = str(round(time.time() - t1, 2))
		print(f'Loaded into markov model with {num_lines} lines. [{elapsed}s]\n')
		await asyncio.sleep(60 * 5)


@bot.listen()
async def on_ready():
	print('---ONLINE---')
	game = discord.Game("with markov chains || mk-help")
	await bot.change_presence(status=discord.Status.online, activity=game)

@bot.listen()
async def on_message(message):
	channel = message.channel					

	if message.content != '' and message.guild.id == 438590624162250752 and message.author.id != 558992355647029270:
		addIn(message.content, message.guild.id)

	if channel.name == 'markovbot' and message.guild.id == 438590624162250752 and message.author.bot == False:
		sent = message.content.split(' ')
		words = []
		
		if STATE == "FIRST_OR_LAST":
			if random.randint(1,3) == 3:
				words.append(sent[-1])
			else:
				if len(sent) >= 2:
					randn = random.randint(1,2)
					for i in range(randn):
						words.append(sent[i])
				else:
					words.append(sent[0])
					
		elif STATE == "FIRST_WORD/S_ONLY":
			if len(sent) >= 2:
				randn = random.randint(1,2)
				for i in range(randn):
					words.append(sent[i])
			else:
				words.append(sent[0])
					
		elif STATE == "FIRST_ONLY":
			words.append(sent[0])
			
		elif STATE == "LAST_ONLY":
			words.append(sent[-1])
			
		elif STATE == "RANDOM":
			words.append(random.choice(sent))
			

		try:
			to_send = wordChain(' '.join(words), message.guild.id)
			if to_send != None:
				await channel.trigger_typing()
				await asyncio.sleep(random.uniform(2,4))
				await channel.send(to_send)
			else:
				await message.add_reaction("markov_what:620612190902157343")
		except discord.errors.HTTPException:
			await message.add_reaction("markov_what:620612190902157343")
	#150,000 LINE LIMIT
	
	"""
	if message.guild.id == 438590624162250752 and message.author.bot == False:
		with open(f'{message.guild.id}.txt', 'r+',encoding='utf-16') as f:
			lines = f.readlines()
	
		if len(lines) > 150000:
			delin = len(lines) - 150000
			with open(f'servers/{message.guild.id}.txt', 'w',encoding='utf-16') as ff:
				ii = 0
				while ii <= delin:
					lines.pop(ii)
					ii += 1
				for line in lines:
					ff.write(line)
	"""





@bot.command()
async def chain(ctx):
	"""Generate markov text"""
	await ctx.trigger_typing()
	try:
		await ctx.send(textChain(ctx.guild.id))
	except discord.errors.HTTPException:
		await ctx.send(random.choice(excuses))

"""
@bot.command()
async def add(ctx):
	Add a text file to the bot's source
	if len(ctx.message.attachments) != 1:
		return await ctx.send("Please provide a text file")

	async with aiohttp.request('get', ctx.message.attachments[0].url) as resp:
		resp.raise_for_status()
		data = await resp.text()
		lines = data.splitlines()
		for line in lines:
			if line != '':
				addIn(line, ctx.guild.id)

	await ctx.send('Thank you for your contributions.')
"""

@bot.command()
async def lines(ctx):
	"""Check total lines in the source text file"""
	with open("servers/{}.txt".format(str(ctx.guild.id)), encoding="utf-16") as txt:
		linyas = txt.read().splitlines()
	await ctx.send("`{}` lines found in text file".format(len(linyas)))

@bot.command()
async def state(ctx, type: int=None):
	"""admin command"""
	global STATE
	if ctx.message.author.id == 472336460503187466:
		if type == None:
			await ctx.send("```Current Chaining State: {}\n\n0 - FIRST_WORD/S_ONLY\n1 - FIRST_OR_LAST\n2 - FIRST_ONLY\n3 - LAST_ONLY\n4 - RANDOM```".format(STATE))
		else:
			STATE = state_types[type]
			await ctx.send("Chaining State Set To: `{}`".format(state_types[type]))

bot.loop.create_task(refresh())

bot.run(API_KEY)
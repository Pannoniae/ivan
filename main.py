from discord.ext import commands
from discord.ext import *
import discord, os, random, time, save, keep_alive, saveparty, sys
import discord.utils
import json
import requests
from discord.utils import get
from discord import Member
import datetime
import interactions
from interactions import *
import pickle
#from interactions.utils.manage_commands import *




TOKEN = os.environ['DISCORD_TOKEN']


#slash = interactions.Client(token=TOKEN)






prefix = "$"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(prefix, intents=intents)




bot.remove_command('help')




#### LISTS OF BORING STUFF ####

sad_words = ['cry', 'unhappy', 'crying']
rick_words = ['bump', 'secret', 'pprog']
rick_stuff = ['never gunna give you up', 'never gunna let you down', "never gonna run around and desert you", "never gonna make you cry", "never gonna say goodbye", "never gonna tell a lie and hurt you"]

def billCash(id):
	#datetime.datetime.today().day
	currentday = datetime.datetime.today().day
	user = save.createUser(id)
	user = save.restore(id)
	bill = user['hitel']

	if currentday == 27:
		if bill > 0:
			return bill * 0.1
		else:
			return 0
	else:
		return 0


###############################
@bot.event
async def on_member_join(member):
		channel = bot.get_channel(978209588283338832)
		await channel.send(f"Üdv! {member} elvtárs sikeresen emigrált a Magyar Kommunista Blokkba!")
		await member.send('Üdv, elvtárs! Én Iván vagyok, a Szovjetunió marsallja és katonai vezetője. Én leszek a Pártfőtitkárok és Elnökök mellet a segítségedre! Kérlek, olvasd el, és tartsd be az alaptörvényt, de ami a legfontosabb: érezd jól magad... És persze a titkosrendőrség mindent lát...')

@bot.event
async def on_member_remove(member):
		channel = bot.get_channel(978209588283338832)
		await channel.send(f"Szomorúan közlöm, hogy {member} elvtárs munkatáborba került, mert kapitalista elveket követett. Szerintem soha nem látjuk újra...")


#bot státusz
@bot.event
async def on_ready():
    activity = discord.Game(name="$help | Vodka ivás Leninnel", type=1)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")

@bot.event
async def on_message(message):
	for word in message.content.split(" "):
		if word in sad_words:
			await message.channel.send("Don't be sad, it's that easy!")
			break
		if word in rick_words:
			user = save.createUser(message.author.id)
			user = save.restore(message.author.id)
			currentTime = time.time()
			lastTime = int(user['lastTime'])
			user['smackers'] += 30
			user['lastTime'] = time.time()
			save.save(user) # save the changes
			await message.channel.send("💵 You earned 30 Followrel Coins!")
			break
		if message.content.lower() in rick_stuff:
			await message.channel.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
	await bot.process_commands(message) # I forgot to add this before, but it neccesarry for the on_message stuff not to override the commands



####################


#### BOT BASIC COMMANDS ####

#@slash.command(
#    name="ping",
#    description="Pingpong",
#    scope=978204080797261854,
#)
#async def ping(ctx: interactions.CommandContext):
#    await ctx.send("Pong")

@bot.command()
async def ping(ctx):
	await ctx.send("Pong")

@bot.command()
async def bug(ctx, *args):
	author = ctx.message.author
	dev = await bot.fetch_user(707550269600169984)
	embed = discord.Embed(title="Új hibajelentés " + str(author) + "-tól", description="Itt egy hibajelentés a bottal vagy szerverrel kapcsolatban.")
	# add fields
	embed.add_field(name="Hibaleírás", value=' '.join(args), inline=False)
	await ctx.send("Sikeres hibajelentés!")
	await dev.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def inventory(ctx):
	user = save.restore(ctx.author.id)
	inventory = user['items']
	embed = discord.Embed(title = str(ctx.message.author) + " cuccai", description="Itt látszanak a boltban megvásárolt dolgok.", color=0xff0000)

	for item in inventory:
		for (a, b, c) in zip(itemslower, itemsprice, itemsname):
			if item == a:
				embed.add_field(name=c, value="Ár: " + str(b), inline=False)
	await ctx.send(embed=embed)
		
				
			


@bot.command(pass_context=True)
@commands.has_any_role('Tesztelő')
async def pártalapítás(ctx):
	author = ctx.message.author
	user = save.restore(ctx.author.id)
	if user['smackers'] >= 100000:
		user['smackers'] -= 100000
		save.save(user)
		await author.send('Szóval egy pártot szeretnél alapítani... Mi legyen a párt neve?')
		partyname = await bot.wait_for('message')
		await author.send("Vettem, elvtárs! Mi legyen a(z) " + str(partyname.content) + " leírása?")
		partydesc = await bot.wait_for('message')
		await author.send("Okés! Mi legyen a párt ideológiája? (csak kommunista lehet kisebb változtatásokkal)")
		ideology = await bot.wait_for('message')
		await author.send("Mentés folyamatban...")
		part = saveparty.createParty(ctx.author.id)
		part = saveparty.restoreParty(ctx.author.id)
		part["name"] = str(partyname.content)
		part["leader"] = str(ctx.author)
		part["desc"] = str(partydesc.content)
		part["ide"] = str(ideology.content)
		saveparty.save(part)
		await author.send("Sikeres pártalapítás!")
		#author.send("")
	else:
		await ctx.send("Még nincs meg a megfelelő kezdőtőkéd egy párt megalapításához! (100000 rubel)")


#ADMIN TOOLS

@bot.command(pass_context=True)
@command.has_any_role('Vezérkar')
async def üzi(ctx, *args):
    await ctx.message.delete()
    for user in ctx.guild.members:
        try:
            await user.send(' '.join(args))
        except:
            print("Nem sikerült")
    ctx.send("Üzenet mindenkinek kiküldve")

#börtön parancs
@bot.command(pass_context=True)
@commands.has_any_role('Állam Védelmi Hatóság', 'Vezérkar')
async def börtön(ctx, member:discord.Member, *args):#idáig műkszik
	fogoly = discord.utils.get(ctx.guild.roles, id=978619998199234600)
	proli = discord.utils.get(ctx.guild.roles, id=978207066491588678)
	await member.add_roles(fogoly)
	await member.remove_roles(proli)
	channel = bot.get_channel(978620073029804052)
	embed = discord.Embed(title="Új fogoly", description="Valaki már megint megszegte az alkotmányt!")
	# add fields
	embed.add_field(name=f"Elítélt: {member} ", value=' '.join(args), inline=False)
	await channel.send(embed=embed)
	await ctx.send("Sikeres elfogás!")
	await member.send("Látom börtönbe lettél zárva... Azt ugye tudod, hogy a 3. ilyennél Szibériába kerülsz? Amíg a börtönben szelidűlsz, élvezd ezt a dalt: <https://www.youtube.com/watch?v=Jzm71rlRgPg> :)")
	print(member)


@bot.command(pass_context=True)
@commands.has_any_role('Vezérkar')
async def gulag(ctx, member:discord.Member, *args):
	await member.ban(reason=' '.join(args))
	channel = bot.get_channel(978620073029804052)
	embed = discord.Embed(title="Gulag transzportálás", description="Ez az ember egy gyökér... Vesszen a gulágban!")
	# add fields
	embed.add_field(name=f"Elítélt: {member} ", value=' '.join(args), inline=False)
	await channel.send(embed=embed)
	await ctx.send("Gulágra küldtem, Elvtárs!")


@bot.command(pass_context=True)
@commands.has_any_role('Vezérkar')
async def addrub(ctx, amount, user:discord.Member):
	usr = save.createUser(user.id)
	usr = save.restore(user.id)
	usr['smackers'] += int(amount)
	save.save(usr)
	await ctx.send("Sikeressen hozzáadtál " + str(amount) + " rubelt " + str(user) + " fiókjához!")

@bot.command(pass_context=True)
@commands.has_any_role('Vezérkar')
async def delrub(ctx, amount, user:discord.Member):
	usr = save.createUser(user.id)
	usr = save.restore(user.id)
	usr['smackers'] -= int(amount)
	save.save(usr)
	await ctx.send("Sikeressen eltávolítottál " + str(amount) + " rubelt " + str(user) + " fiókjából!")

@bot.command(pass_context=True)
@commands.has_any_role('Vezérkar')
async def delhitel(ctx, user:discord.Member):
	usr = save.createUser(user.id)
	usr = save.restore(user.id)
	usr['hitel'] = 0
	save.save(usr)
	await ctx.send("Sikeresen törölted " + str(user) + " tartozásait!")

@bot.command()
async def info(ctx):
	for guild in bot.guilds:
		await ctx.send(f'Folyamatosan szolgálok {len(guild.members)} hithű proletárt a {guild.name} szerveren. Minden fasza, 13ms válaszidővel futok...')

# ADMIN END


@bot.command()
async def érmedobás(ctx):
	heads_tails = ['Fej', 'Írás']
	
	choice = random.choice(heads_tails)
	
	await ctx.send(choice)

@bot.command()
async def dobókocka(ctx):
	num = random.randrange(1, 6)
	await ctx.send('A dobókocka ' + str(num) + ' pöttyöt mutat!')


@bot.command()
async def jelentés(ctx, member:discord.Member, *args):
	author = ctx.message.author
	reported = str(member)
	channel = bot.get_channel(978730688465477796)
	embed = discord.Embed(title="Új jelentés " + str(author) + "-tól", description="Itt egy jelentés, amit a besúgók küldtek. Ha a bejelentés oka valós, az elkövető akár mehet is börtönbe.")
	# add fields
	embed.add_field(name=f"Név: {reported}", value=' '.join(args), inline=False)
	await ctx.send("Sikeres bejelentés!")
	await channel.send(embed=embed)



@bot.command(pass_context=True)
@commands.has_any_role('Tesztelő')
async def adomány(ctx, value):
	await ctx.send("Köszönjük, hogy adományoddal segíted a Szovjet űrkutatást, Elvtárs! Még {rubel} kell ahhoz, hogy megelőzhessük a kapitalista Ámeríkaiakat!")
	




@bot.command()
async def mondd(ctx, *args):
	await ctx.message.delete()
	await ctx.send(' '.join(args), tts=True)





@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def hitel(ctx, amount=0):
	author = ctx.message.author
	if billCash(ctx.author.id) == 0:
		author = save.createUser(ctx.author.id)
		author = save.restore(ctx.author.id)
		print(author)
		author['hitel'] += int(amount)
		author['smackers'] += int(amount)
		save.save(author)
		channel = bot.get_channel(981973830325116998)
		embed = discord.Embed(title="Új hitel", description="Valaki hitelt vett fel.")
		# add fields
		embed.add_field(name=f"Felhasználó: {ctx.message.author}", value='Összeg: ' + str(int(amount)), inline=False)
		await channel.send(embed=embed)
		await ctx.send("Felvettél " + str(amount) + " rubel hitelt. Minden hónapban be kell fizetned a 10%-át amíg a tartozás meg nem szűnik. Be nem fizetett hitel esetén nem tudsz dolgozni illetve vásárolni a befizetésig.")
	else:
		user = save.createUser(ctx.author.id)
		user = save.restore(ctx.author.id)
		szazalek = user['hitel'] * 0.1
		user['smackers'] -= szazalek
		print(user['hitel'])
		user['hitel'] -= szazalek
		save.save(user)
		await ctx.send("A tartozásod 10%-a kifizetve erre a hónapra!")


@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def fizetés(ctx, amount, ping:discord.Member):
	if billCash(ctx.author.id) == 0:
		for user_mentioned in ctx.message.mentions:
			pingid = user_mentioned.id
			pingmention = user_mentioned
		
		payer = save.createUser(ctx.author.id)
		payer = save.restore(ctx.author.id)
		ping = save.createUser(pingid)
		ping = save.restore(pingid)

		if payer['smackers'] >= abs(int(amount)):
			payer['smackers'] -= abs(int(amount))
			ping['smackers'] += abs(int(amount))
			save.save(payer) # save the changes
			save.save(ping)
			await ctx.send("Sikeres tranzakció!")
			channel = bot.get_channel(981973830325116998)
			embed = discord.Embed(title="Új banki utalás", description="Típus: pénzküldés")
			# add fields
			embed.add_field(name=f"Fizető: {ctx.author} -> {pingmention}", value='Összeg: ' + str(abs(int(amount))), inline=False)
			await channel.send(embed=embed)
		else:
			await ctx.send("Nincs elég rubeled a tranzakcióhoz!")
	else:
		await ctx.send("Nem fizetted ki a hitelt!")
	



@bot.event
async def on_raw_reaction_add(payload):
	guild = bot.get_guild(payload.guild_id) # Get guild
	member = get(guild.members, id=payload.user_id) # Get the member out of the guild
	# Lakhatás
	if payload.message_id == 1015968546305605632: # Only message where it will work
		if str(payload.emoji) == "✅": # Your emoji
			role = get(payload.member.guild.roles, id=978207066491588678) # Role ID
		else:
			role = get(guild.roles, name=payload.emoji)
		if role is not None: # If role exists
			await payload.member.add_roles(role)
			await payload.member.send(f"Megkaptad a lakhatást! ({role} rang)")
	# Ide jöhet még reakciós rang		



@bot.command()
async def rand(ctx, num=10): # defualts to 10 if nothing is included. 
	random_number = random.randint(0, int(num)) # don't forget to convert from string to a number
	
	await ctx.send(str(random_number))


############################

#### BOT HELP ####

@bot.command()
async def help(ctx):
	embed = discord.Embed(title="Parancsok", description="Minden parancsnak ezzel a prefixxel kell kezdődnie: `$`")
	# add fields
	embed.add_field(name="Érmedobás", value="`$érmedobás`", inline=False)
	embed.add_field(name="Random Szám", value="`$rand <num>` a `<num>` -al optimális", inline=False)
	embed.add_field(name="Dolgozás", value="`$munka` Csak minden 30. percben tudsz dolgozni.", inline=False)
	embed.add_field(name="Napi", value="`$napi` Ajándék megszerzése 12 óránként", inline=False)
	embed.add_field(name="Leaderboard", value="`$leaderboard`", inline=False)
	embed.add_field(name="Rubel számlád", value="`$rubel`", inline=False)
	embed.add_field(name="Bolt", value='`$bolt`', inline=False)
	embed.add_field(name="Buziságmérő", value='`$gayrate <ping>`', inline=False)
	embed.add_field(name="Jelentés", value='`$jelentés <ping> <Jelentés oka>`', inline=False)
	embed.add_field(name="Rubel küldése", value='`$fizetés <pénzösszeg> <ping, akinek küldöd>`', inline=False)
	embed.add_field(name="Hiba jelentése", value='`$bug <hiba leírása>` ezzel vagy szerver vagy bot hibát tudsz jelenteni a fejlesztőnek', inline=False)
	embed.add_field(name="Hitel felvétele", value='`$hitel <összeg>`', inline=False)
	embed.add_field(name="Inventory megtekintése", value='`$inventoty`', inline=False)
	embed.add_field(name="Bot tulajdonságok", value='Fenntartó: petyadev#1129 | Szeretnél saját Discord botot? [Csinálok neked egyet!](https://www.fiverr.com/petertill/create-a-custom-discord-bot-for-you) ')
	# then send the embed
	await ctx.send(embed=embed)

##################


#### BOT SMACKERS ####

@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def munka(ctx):
	if billCash(ctx.author.id) == 0:
		try:
			avh = discord.utils.get(ctx.guild.roles, name="Állam Védelmi Hatóság") # Get the role
			katona = discord.utils.get(ctx.guild.roles, name="Katona")
		except:
			await ctx.send("Valami váratlan hiba történt. Ez lehet azért, mert privátban akartál dolgozni, ahol nincsenek rangok. Ha a probléma a szerveren is előfordul, írj Petru elvtársnak!")
		if save.checkExist(ctx.author.id):
			pass
		else:
			user = save.createUser(ctx.author.id)
		user = save.restore(ctx.author.id)
		currentTime = time.time()
		lastTime = int(user['lastTime'])
		if lastTime+30 <= currentTime or megvan(ctx.author.id, "trabant"):
			random_szam = random.randint(100, 170)
			if avh in ctx.author.roles:
				szazalek = random_szam * 2
				user['smackers'] += szazalek
				user['lastTime'] = time.time()
				save.save(user)
				embed = discord.Embed(title = "💵 " + str(szazalek) + " Rubelt szereztél! 100%-os emeléssel", color=0x59ff00)
				await ctx.send(embed=embed)
			elif katona in ctx.author.roles:
				szazalek = random_szam * 2
				user['smackers'] += szazalek
				user['lastTime'] = time.time()
				save.save(user)
				embed = discord.Embed(title = "💵 " + str(szazalek) + " Rubelt szereztél! 100%-os emeléssel", color=0x59ff00)
				await ctx.send(embed=embed)
			else:
				user['smackers'] += random_szam
				user['lastTime'] = time.time()
				save.save(user) # save the changes
				embed = discord.Embed(title = "💵 " + str(random_szam) +" Rubelt szereztél!", color=0x59ff00)
				await ctx.send(embed=embed)
		else:
			await ctx.send(f"{ctx.author.mention}, várnod kell még {str(int(30-(currentTime-lastTime)))} másodpercet")
	else:
		await ctx.send("Nem fizetted ki a hitelt!")


@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def napi(ctx):
	if billCash(ctx.author.id) == 0:
		if save.checkExist(ctx.author.id):
			pass
		else:
			user = save.createUser(ctx.author.id)
		print("Working")
		user = save.restore(ctx.author.id)

		currentTime = time.time()
		lastTime = int(user['bonusTime'])
		if lastTime+43200 <= currentTime:
			user['smackers'] += 1000
			user['bonusTime'] = time.time()
			save.save(user) # save the
			embed = discord.Embed(title = "💵 1000 Rubelt szereztél!", color=0x59ff00)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f"{ctx.author.mention}, várnod kell még {str(int((43200-(currentTime-lastTime)) / 60))} percet")
	else:
		await ctx.send("Nem fizetted ki a hitelt!")

@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def leaderboard(ctx):
	topTen = save.leaderboard()
	
	embed = discord.Embed(title="Leaderboard", description="Top 5 proletár Rubel szerint")
	
	for user in topTen:
		discordData = await ctx.message.guild.query_members(user_ids=[user['userid']])
		username = discordData[0]
		embed.add_field(name=f"{str(topTen.index(user)+1)}. {username.name}", value=f"Rubelek: `{str(user['smackers'])}`")
	await ctx.send(embed=embed)


@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def rubel(ctx):
	user = save.restore(ctx.author.id)
	embed = discord.Embed(title=f"{ctx.author.name} számlája", description=f"Rubelek: `{str(user['smackers'])}`")
	await ctx.send(embed=embed)



# boltos cuccok


itemsname = ["Kőbányai", "Talicska", "Google Bylat asszisztens", "Trabant", "Ikarus busz", "Lenin szobra", "Füves cigi", "Volga-M22"]
itemsprice = [50, 2000, 6000, 120000, 220000, 60000, 100, 160000]
itemslower = ["kőbányai", "talicska", "g-blyat", "trabant", "ikarus", "lenin-szobor", "füves-cigi", "volga"]
itemsrole = ["Igazán proli", "Kulák", "Google Blyat felhasználó", "Trabanton szállni...", "Buszvezető", "Hithű kommunista", "Igazán proli", "Volgatulajdonos"]



@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def bolt(ctx):
	user = save.restore(ctx.author.id)

	embed = discord.Embed(title="Bolt", description=f"Neked {str(user['smackers'])} rubeled van")

	for (a, b, c) in zip(itemsname, itemsprice, itemslower):
		embed.add_field(name=a, value='`' + str(b) + '` Rubel | Parancs : `$buy "' + c + '"`', inline=False)
	
	await ctx.send(embed=embed)


@bot.command()
async def gayrate(ctx, member:discord.User):
  author = member.id
  authname = member.name
  if (author == 877884542566957117):
    gayratenum = 100
  elif (author == 707550269600169984):
    gayratenum = 0
  else:
    gayratenum = random.randint(0, 100)
  


  await ctx.send(authname + " a számításaim szerint " + str(gayratenum) + "%-ban buzi.")


@bot.command()
async def whois(ctx, member):
  url = "https://api.followrel.ga/api.php?id=" + member
  r = requests.get(url)
  # parse x:
  y = r.json()
  user = y["customers"]
  id = user["id"]
  name = user["name"]
  bio = user["bio"]
  job = user["job"]
  website = user["website"]
  coin = user["coin"]
  embed = discord.Embed(title=name + " on Followrel", description=f"Bio: {bio} ")
  embed.add_field(name="Job", value='Works at: ' + job, inline=False)
  embed.add_field(name="Website", value=website, inline=False)
  embed.add_field(name="Coins", value=coin, inline=False)
	
  await ctx.send(embed=embed)

def megvan(id, item):
	user = save.restore(id)
	list = user['items']
	if item in list:
		return 1
	else:
		return 0


@bot.command(pass_context=True)
@commands.has_any_role('Proletárok')
async def buy(ctx, item):
	if billCash(ctx.author.id) == 0:
		for (a, b, c, d) in zip(itemsname, itemsprice, itemslower, itemsrole):
			if item.lower() == c:
				#if megvan(ctx.author.id, c):
				#	await ctx.send("Neked már meg van ez a cucc!")
				user = save.restore(ctx.author.id)
				if user['smackers'] >= b:
					member = await ctx.message.guild.query_members(user_ids=[ctx.author.id])
					member = member[0]
					await member.add_roles(discord.utils.get(member.guild.roles, name=d))
					user['smackers'] -= b
					list = user['items']
					list.append(str(c))
					user['items'] = list
					print(user['items'])
					save.save(user)
					await ctx.send("Sikeres vásárlás elvtárs!")
				else:
					await ctx.send(f"Még {str(b-user['smackers'])} rubel kell, hogy megvehesd a(z) '{a}'-t!")
			else:
				pass
	else:
		await ctx.send("Nem fizetted ki a hitelt!")

######################




keep_alive.keep_alive()
try:
	bot.run(TOKEN)
	slash.start()
except discord.errors.HTTPException:
	print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
	os.system("kill 1")
	os.system("python restarter.py")

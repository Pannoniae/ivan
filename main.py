from discord.ext import commands
import discord, os, random, time, save, keep_alive, saveparty
import discord.utils
import json
import requests
from discord.utils import get
from discord import Member
import interactions

TOKEN = os.environ['DISCORD_TOKEN']

prefix = "$"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(prefix, intents=intents)

#creating client



bot.remove_command('help')


#### LISTS OF BORING STUFF ####

sad_words = ['cry', 'unhappy', 'crying']
rick_words = ['bump', 'secret', 'pprog']
rick_stuff = ['never gunna give you up', 'never gunna let you down', "never gonna run around and desert you", "never gonna make you cry", "never gonna say goodbye", "never gonna tell a lie and hurt you"]


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


#párt alapítása
@bot.command()
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



@bot.command()
async def adomány(ctx, value):
	await ctx.send("Köszönjük, hogy adományoddal segíted a Szovjet űrkutatást, Elvtárs! Még {rubel} kell ahhoz, hogy megelőzhessük a kapitalista Ámeríkaiakat!")
	




@bot.command()
async def mondd(ctx, *args):
	await ctx.message.delete()
	await ctx.send(' '.join(args), tts=True)


@bot.command(pass_context=True)
@commands.has_any_role('Vezérkar')
async def addrub(ctx, amount):
	author = save.createUser(ctx.author.id)
	author = save.restore(ctx.author.id)
	author['smackers'] += int(amount)
	save.save(author)
	await ctx.send("Sikeressen hozzáadtál " + str(amount) + " rubelt a fiókodhoz!")


@bot.command()
async def hitel(ctx, amount):
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


@bot.command()
async def fizetés(ctx, amount, ping:discord.Member):
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
	


@bot.command()
async def atombomba(ctx):
	message = await ctx.send("Üdv, Elvtárs! Szeretnél atombombát indítani a kapitalista nácik ellen?")
	igen = '\N{THUMBS UP SIGN}'
	nem = '\N{THUMBS DOWN SIGN}'
	await message.add_reaction(igen)
	await message.add_reaction(nem)



	



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
	embed.add_field(name="Hitel felvétele", value='`$hitel <összeg>`')
	embed.add_field(name="Bot tulajdonságok", value='Fenntartó: petyadev#1129 | [Nyílt forráskódú projekt](https://github.com/petertill/ivan) ')
	# then send the embed
	await ctx.send(embed=embed)

##################


#### BOT SMACKERS ####

@bot.command()
async def munka(ctx):
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
	if lastTime+30 <= currentTime:
		random_szam = random.randint(20, 70)
		if avh in ctx.author.roles:
			szazalek = random_szam * 2
			user['smackers'] += szazalek
			user['lastTime'] = time.time()
			save.save(user)
			await ctx.send("💵 " + str(szazalek) +" Rubelt szereztél! 100%-os emeléssel")
		elif katona in ctx.author.roles:
			szazalek = random_szam * 2
			user['smackers'] += szazalek
			user['lastTime'] = time.time()
			save.save(user)
			await ctx.send("💵 " + str(szazalek) +" Rubelt szereztél! 100%-os emeléssel")
		else:
			user['smackers'] += random_szam
			user['lastTime'] = time.time()
			save.save(user) # save the changes
			await ctx.send("💵 " + str(random_szam) +" Rubelt szereztél!")
	else:
		await ctx.send(f"{ctx.author.mention}, várnod kell még {str(int(30-(currentTime-lastTime)))} másodpercet")



@bot.command()
async def napi(ctx):
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
		save.save(user) # save the changes
		await ctx.send("💵 1000 Rubelt szereztél!")
	else:
		await ctx.send(f"{ctx.author.mention}, várnod kell még {str(int((43200-(currentTime-lastTime)) / 60))} percet")


@bot.command()
async def leaderboard(ctx):
	topTen = save.leaderboard()
	
	embed = discord.Embed(title="Leaderboard", description="Top 5 proletár Rubel szerint")
	
	for user in topTen:
		discordData = await ctx.message.guild.query_members(user_ids=[user['userid']])
		username = discordData[0]
		embed.add_field(name=f"{str(topTen.index(user)+1)}. {username.name}", value=f"Rubelek: `{str(user['smackers'])}`")
	await ctx.send(embed=embed)


@bot.command()
async def rubel(ctx):
	user = save.restore(ctx.author.id)
	embed = discord.Embed(title=f"{ctx.author.name} számlája", description=f"Rubelek: `{str(user['smackers'])}`")
	await ctx.send(embed=embed)



# boltos cuccok


itemsname = ["Kőbányai", "Talicska", "Google Bylat asszisztens", "Trabant", "Ikarus busz", "Lenin szobra"]
itemsprice = [1000, 5000, 6000, 10000, 20000, 15000]
itemslower = ["kőbányai", "talicska", "g-blyat", "trabant", "ikarus", "lenin-szobor"]



@bot.command()
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


@bot.command()
async def buy(ctx, item):
	if item.lower() == 'kőbányai':
		user = save.restore(ctx.author.id)
		if user['smackers'] >= 1000:
			member = await ctx.message.guild.query_members(user_ids=[ctx.author.id])
			member = member[0]
			await member.add_roles(discord.utils.get(member.guild.roles, name="Igazán proli"))
			user['smackers'] -= 1000
			save.save(user)
			await ctx.send("Sikeres vásárlás elvtárs!")
		else:
			await ctx.send(f"Még {str(1000-user['smackers'])} rubel kell, hogy megvehesd a(z) 'Kőbányai'-t!")
	if item.lower() == 'g-blyat':
		user = save.restore(ctx.author.id)
		if user['smackers'] >= 6000:
			member = await ctx.message.guild.query_members(user_ids=[ctx.author.id])
			member = member[0]
			await member.add_roles(discord.utils.get(member.guild.roles, name="Google Blyat felhasználó"))
			user['smackers'] -= 6000
			save.save(user)
			await ctx.send("Sikeres vásárlás elvtárs!")
		else:
			await ctx.send(f"Még {str(6000-user['smackers'])} rubel kell, hogy megvehesd a(z) 'Google Blyat'-t!")
	if item.lower() == 'trabant':
		user = save.restore(ctx.author.id)
		if user['smackers'] >= 10000:
			member = await ctx.message.guild.query_members(user_ids=[ctx.author.id])
			member = member[0]
			await member.add_roles(discord.utils.get(member.guild.roles, name="Trabanton szállni..."))
			user['smackers'] -= 10000
			save.save(user)
			await ctx.send("Sikeres vásárlás elvtárs!")
		else:
			await ctx.send(f"Még {str(10000-user['smackers'])} rubel kell, hogy megvehesd a(z) 'Trabant'-t!")
	if item.lower() == 'ikarus':
		user = save.restore(ctx.author.id)
		if user['smackers'] >= 20000:
			member = await ctx.message.guild.query_members(user_ids=[ctx.author.id])
			member = member[0]
			await member.add_roles(discord.utils.get(member.guild.roles, name="Buszvezető"))
			user['smackers'] -= 20000
			save.save(user)
			await ctx.send("Sikeres vásárlás elvtárs!")
		else:
			await ctx.send(f"Még {str(20000-user['smackers'])} rubel kell, hogy megvehesd a(z) 'Ikarus busz'-t!")
	if item.lower() == 'lenin-szobor':
		user = save.restore(ctx.author.id)
		if user['smackers'] >= 15000:
			member = await ctx.message.guild.query_members(user_ids=[ctx.author.id])
			member = member[0]
			await member.add_roles(discord.utils.get(member.guild.roles, name="Hithű kommunista"))
			user['smackers'] -= 15000
			save.save(user)
			await ctx.send("Sikeres vásárlás elvtárs!")
		else:
			await ctx.send(f"Még {str(15000-user['smackers'])} rubel kell, hogy megvehesd a(z) 'Lenin szobor (2.5 méter)'-t!")
	if item.lower() == 'talicska':
		user = save.restore(ctx.author.id)
		if user['smackers'] >= 5000:
			member = await ctx.message.guild.query_members(user_ids=[ctx.author.id])
			member = member[0]
			await member.add_roles(discord.utils.get(member.guild.roles, name="Kulák"))
			user['smackers'] -= 5000
			save.save(user)
			await ctx.send("Sikeres vásárlás elvtárs!")
		else:
			await ctx.send(f"Még {str(5000-user['smackers'])} rubel kell, hogy megvehesd a(z) 'talicska'-t!")
	else:
		pass

######################



keep_alive.keep_alive()
bot.run(TOKEN)
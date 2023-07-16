import discord
from discord.ext import commands
from discord import app_commands
import random
import string
from datetime import timedelta, datetime
import pytz
import requests
import json
import os
from discord.ui import View, Button, Select
import asyncio
import aiohttp
from app_commands import Choice
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(),
case_insensitive=True)

mainshop = [{"name":"Watch","price":100,"description":"Tell the time"
            "name":"Jaboro's Respect","price":20000,"description":"Earn Jaboros Respect by Getting a role when you buy this!"}]


mod_channel_id = 1128903406707277904



@bot.tree.command(name="modmail", description="modmail")
async def modmail(interaction: discord.Interaction, *, message: str):
    if interaction.guild:
        await interaction.response.send_message(f"This can only be used in dms, or when you need to appeal a mute or a ban.")
        return
    mod_channel_id = 1128903406707277904 
    mod_channel = bot.get_channel(mod_channel_id)
    author = interaction.user
    await interaction.response.send_message(f"Message was sent to the moderation team, they will respond to you soon.")
    await mod_channel.send(f'Modmail from **{author.mention}** ID: **({author.id})**, message: `{message}`')
    
    








@bot.tree.command(name="modreply", description="reply to modmail, MODS ONLY")
async def reply(interaction: discord.Interaction, member: discord.Member, *, message: str):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(f"{interaction.user.mention} you are not allowed to use this command!")
        return
    await member.send(f'Response from the moderation team, {interaction.user.mention}: {message}')
    await interaction.response.send_message('Message sent successfully.')


@bot.event
async def on_message(message):
    if message.channel.id == mod_channel_id and not message.author.bot:
        if ':' in message.content:
            user_id = int(message.content.split(':')[0].split('(')[1].split(')')[0].strip())
            content = ':'.join(message.content.split(':')[1:]).strip()
            await bot.invoke(await bot.get_context(message), 'reply', user_id, message=content)
        else:
            await message.channel.send("Invalid format. Please use 'user_id: message'.")

    await bot.process_commands(message)





























async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("economy17.json", "w") as f:
        json.dump(users,f)
    return True



async def get_bank_data():
    with open("economy17.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = "wallet"):
    users = await get_bank_data()


    users[str(user.id)][mode] += change

    with open("economy17.json", "w") as f:
        json.dump(users,f)


        bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("economy17.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]




async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("economy17.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]



















 
@bot.event
async def on_ready():
    print(f"Starting up {bot.user.name}!")
    print(f"{bot.user.name} is now online!")
    try:
        synced = await bot.tree.sync()
        print(f"{bot.user.name} has synced {len(synced)} application command(s)")
    except Exception as e:
        print(e)
    activity = discord.Game(name="Discord")
    await bot.change_presence(activity=activity)
    status = discord.Status.do_not_disturb
    await bot.change_presence(status=status, activity=activity)
    print(f"Have fun wth the bot!")



@bot.tree.command(name="say")
@app_commands.describe(what_to_say = "What Should I Say?")
async def say(interaction: discord.Interaction, what_to_say: str):
    await interaction.response.send_message(f"{interaction.user.mention} said `{what_to_say}`")




@bot.tree.command(name="cf", description="coinflip")
async def cf(interaction: discord.Interaction, choice: str):
    valid_choices = ["heads", "tails"]

    if choice.lower() not in valid_choices:
        await interaction.response.send_message("Invalid choice! Please choose either 'heads' or 'tails'.")
        return

    coin_side = random.choice(valid_choices)

    if choice.lower() == coin_side:
        result = "You win!"
    else:
        result = "You lose!"

    await interaction.response.send_message(f"The coin landed on ```{coin_side}. {result}```")


@bot.tree.command(name="ban", description="bans users")
async def ban(interaction: discord.Interaction, member: discord.Member, reason : str):
    if not interaction.user.guild_permissions.ban_members:
        em1 = discord.Embed(title=f"Ban Case", description=f"You do not have permission to use this command.")
        await interaction.response.send_message(em1=em1)
        return
    await member.ban()
    embed = discord.Embed(title=f"Ban Case", description=f"{member.mention} was banned from ```{interaction.guild.name}``` for reason: ```{reason}``` they were banned by {interaction.user.mention}")
    await interaction.response.send_message(embed=embed)
    embed = discord.Embed(title=f"Ban Case", description=f"You were banned from ```{interaction.guild.name}``` for reason: ```{reason}``` you were banned by {interaction.user.mention}")
    await member.send(embed=embed)





















@bot.tree.command(name="kick", description="kicks users")
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    if not interaction.user.guild_permissions.kick_members:
        embed = discord.Embed(title=f"You are not allowed to use this command.", description=f"You must have the permission: Kick Members.")
        await interaction.response.send_message(embed=embed)
        if interaction.user == member:
            embed = discord.Embed(title="You cannot kick yourself.")
            await interaction.response.send_message(embed=embed)
        return

    await member.kick(reason=reason)
    embed = discord.Embed(title=f"Kick Case", description=f"{member.mention} has been kicked for reason: {reason}")
    await interaction.response.send_message(embed=embed)

    embed = discord.Embed(title=f"Kick Case", description=f"You have been kicked from {interaction.guild.name} by {interaction.user.mention}. For reason: {reason}")
    await member.send(embed=embed)








@bot.tree.command()
async def embedcreate(interaction: discord.Interaction, title: str, description: str):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.random()
    )
    await interaction.response.send_message(embed=embed)










@bot.tree.command(name="ui", description="gets mentioned user's user info")
async def ui(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title="User Info", color=discord.Color.random())
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Roles", value=", ".join(role.name for role in member.roles[1:]), inline=False)


    await interaction.response.send_message(embed=embed)



@bot.tree.command(name="rng", description="random number generator")
async def rng(interaction: discord.Interaction, min: int, max: int):
    if min >= max:
        await interaction.response.send_message("Invalid range. The start value must be less than the end value.")
        return
    random_num = random.randint(min, max)
    await interaction.response.send_message(f"{random_num}")

@bot.tree.command(name="rlg", description="random letter generator")
async def rlg(interaction: discord.Interaction):
    random_letter = random.choice(string.ascii_letters)
    await interaction.response.send_message(f"{random_letter}")


@bot.tree.command(name="shutdown-bot")
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id == 761071450207420416 or 910618087957598219:
        await interaction.response.send_message(f"**{interaction.user.name}** has shut down `{bot.user.name}`!")
    else:  
        await bot.close()




@bot.tree.command()
async def fakesay(interaction:discord.Interaction,member:discord.Member ,text:str):
    pfp = member.avatar.url
    name = member.name
    url = 'https://discord.com/api/webhooks/1129216635023139036/SqKwtFcJGUqOr4vESgAMBZl6mTeyi95Y3TtrnbLLntET8iVEUqjIgOACU0dRpAOo9XGx'
    json = {
        "content": text,
        "avatar_url": pfp,
        "username": name
    }
    requests.post(url=url, json=json)
    await interaction.response.send_message("sent!", ephemeral=True)


      
        
    





@bot.tree.command(name="embedtitle", description="title of an embed")
async def embedtitle(interaction: discord.Interaction, title_say: str):
    embed = discord.Embed(title=f" {interaction.user.name} said: {title_say}", color= discord.Color.random()) 
    await interaction.response.send_message(embed=embed)







@bot.tree.command(name="balance", description="check user balance")
async def balance(interaction: discord.Interaction):
    await open_account(interaction.user)

    users = await get_bank_data()
    
    user = interaction.user


    

    wallet_amt = users[str(user.id)]["wallet"] 
    bank_amt = users[str(user.id)]["bank"] 

    em =  discord.Embed(title=f"{interaction.user.name} here is your balance.", color=discord.Color.dark_blue())
    em.add_field(name = "Wallet Balance",value= wallet_amt)
    em.add_field(name = "Bank Balance",value= bank_amt)
    await interaction.response.send_message(embed=em)
    


@bot.tree.command(name="beg", description="beg for money")
@app_commands.checks.cooldown(1,120, key=lambda i: (i.guild.id, i.user.id))
async def beg(interaction: discord.Interaction):
        await open_account(interaction.user)
        users = await get_bank_data()
        user = interaction.user

        earnings = random.randint(1, 500)


        await interaction.response.send_message(f"You begged and begged and someone gave you {earnings} dollars.")



        users[str(user.id)]["wallet"] += earnings

        with open("economy17.json", "w") as f:
            json.dump(users,f)



        wallet_amt = users[str(user.id)]["wallet"]

@beg.error
async def on_beg_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error,app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True) 





@bot.tree.command(name="withdraw", description="withdraw money from the bank")
async def withdraw(interaction: discord.Interaction, amount:str):
    await open_account(interaction.user)
    if amount == None:
        await interaction.response.send_message("Please enter the amount of money you want to withdraw.")
        return
    bal= await update_bank(interaction.user)
    amount = int(amount)
    if amount>bal[1]:
        await interaction.response.send_message("You dont have that amount of money.")
        return
    if amount<0:
        await interaction.response.send_message("Amount must be positive.")
        return
    

    await update_bank(interaction.user,amount,"wallet")
    await update_bank(interaction.user,-1*amount,"bank")



    await interaction.response.send_message(f"You withdrew {amount} dollars from your bank.")




@bot.tree.command(name="deposit", description="deposit money into the bank")
async def withdraw(interaction: discord.Interaction, amount:str):
    await open_account(interaction.user)
    if amount == None:
        await interaction.response.send_message("Please enter the amount of money you want to deposit.")
        return
    bal= await update_bank(interaction.user)
    amount = int(amount)
    if amount>bal[0]:
        await interaction.response.send_message("You dont have that amount of money.")
        return
    if amount<0:
        await interaction.response.send_message("Amount must be positive.")
        return
    

    await update_bank(interaction.user,-1*amount,"wallet")
    await update_bank(interaction.user, amount,"bank")



    await interaction.response.send_message(f"You deposited {amount} dollars into your bank.")







@bot.tree.command(name="give", description="give money to other users")
async def give(interaction: discord.Interaction, member: discord.Member, amount:str):
    if member == interaction.user:
        await interaction.response.send_message(f"{interaction.user.mention} you cant give money to yourself!!")
    await open_account(interaction.user)
    await open_account(member)
    if amount == None:
        await interaction.response.send_message("Please enter the amount of money you want to send.")
        return
    bal= await update_bank(interaction.user)
    amount = int(amount)
    if amount>bal[1]:
        await interaction.response.send_message("You dont have that amount of money.")
        return
    if amount<0:
        await interaction.response.send_message("Amount must be positive.")
        return
    

    await update_bank(interaction.user,-1*amount,"bank")
    await update_bank(member, amount,"bank")



    await interaction.response.send_message(f"You gave {member.mention} {amount} dollars.")

















@bot.tree.command(name="rob", description="rob users")
@app_commands.checks.cooldown(1,300, key=lambda i: (i.guild.id, i.user.id))
async def rob(interaction: discord.Interaction, member: discord.Member):
    if member == interaction.user:
        await interaction.response.send_message(f"{interaction.user.mention} you cant rob yourself!!")
    await open_account(interaction.user)
    await open_account(member)
    bal= await update_bank(member)
    if bal[0]<100:
        await interaction.response.send_message(f"{member.mention} does not have enough money.")
        return
    

    earnings = random.randrange(0, bal[0])


    await update_bank(interaction.user, earnings)
    await update_bank(interaction.user, -1* earnings)



    await interaction.response.send_message(f"You robbed {member.mention} and gained {earnings} dollars.")

@rob.error
async def on_rob_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error,app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)








@bot.tree.command(name="shop", description="buy items!")
async def shop(interaction: discord.Interaction):
    em = discord.Embed(title="Shop")


    for item in mainshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        em.add_field(name = name, value= f"${price} | {description}")

        await interaction.response.send_message(embed=em)





@bot.tree.command(name="buy", description="buy a item")
async def buy(interaction: discord.Interaction, item:str, amount: int = 1):
    await open_account(interaction.user)

    res = await buy_this(interaction.user,item, amount)

    if not res[0]:
        if res[1]==1:
            await interaction.response.send_message("That Object isn't there!")
            return
        if res[1]==2:
            await interaction.response.send_message(f"You don't have enough money in your wallet to buy {amount} {item}")
            return
        


    await interaction.response.send_message(f"You just bought {amount} {item}")




@bot.tree.command(name="sell", description="sell items")
async def sell(interaction: discord.Interaction,item:str,amount: int = 1):
    await open_account(interaction.user)

    res = await sell_this(interaction.user,item,amount)

    if not res[0]:
        if res[1]==1:
            await interaction.response.send_message("That Object isn't there!")
            return
        if res[1]==2:
            await interaction.response.send_message(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await interaction.response.send_message(f"You don't have {item} in your bag.")
            return

    await interaction.response.send_message(f"You just sold {amount} {item}.")


@bot.tree.command(name="bag", description="check your bag")
async def bag(interaction: discord.Interaction):
    await open_account(interaction.user)
    user = interaction.user
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await interaction.response.send_message(embed = em)    



    




@bot.tree.command(name="work", description="work for money")
@app_commands.checks.cooldown(1,120, key=lambda i: (i.guild.id, i.user.id))
async def work(interaction: discord.Interaction):
    await open_account(interaction.user)
    users = await get_bank_data()
    user = interaction.user

    earnings = random.randrange(1000)


    await interaction.response.send_message(f"You worked and got {earnings} dollars!")



    users[str(user.id)]["bank"] += earnings

    with open("economy17.json", "w") as f:
        json.dump(users,f)


@work.error
async def on_work_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error,app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)










@bot.tree.command(name="memberbalance", description="check user balance")
async def memberbalance(interaction: discord.Interaction, member: discord.Member):
    await open_account(interaction.user)
    await open_account(member)

    users = await get_bank_data()
    

    wallet_amt2 = users[str(member.id)]["wallet"] 
    bank_amt2 = users[str(member.id)]["bank"] 

    em2 = discord.Embed(title=f"Here is {member.name}'s balance", color = discord.Color.dark_blue())
    em2.add_field(name = "Wallet Balance", value= wallet_amt2)
    em2.add_field(name = "Bank Balance", value= bank_amt2)
    await interaction.response.send_message(embed=em2)























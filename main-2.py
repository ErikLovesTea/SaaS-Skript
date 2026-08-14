# Erik ....., TA-25A, viimati muudetud: 2023-04-29
# kahju, et see kõik nii hardcoded siin on......
import time

import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
import pickle
import sys
import wget
import os

privileged_accounts = [0, 0]
keys = []
accounts = {}

load_dotenv()

token = "" # tundus ohutuvam kuna see ei olnud public code.

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command('help')

current_file = sys.argv[0]
current_path = os.path.dirname(sys.argv[0])
current_file_name = os.path.basename(sys.argv[0])
in_the_path = os.listdir(current_path)

for files in in_the_path:
    if files == current_file:
        pass
    if files == "oldversion.tmp":
        os.remove(files)

@bot.event
async def on_ready():



    response = requests.get(url='XXXXXX') # webhook req
    thingbefore = response.content.decode()
    thething = thingbefore.splitlines()

    if float(thething[0]) != 1.0:
        CRED = '\33[31m'
        CEND = '\033[0m'
        CGREEN = '\33[32m'

        print(f'UPDATE IS AVAILABLE | CURRENT VERSION : {1.0} | NEWEST VERSION : {str(thething[0])}' + "\n")
        print('ATTEMPTING TO DOWNLOAD THE LATEST VERSION\nESTIMATED TIME : 10 seconds' + "\n")

        a1a = wget.download('XXXXX') # siia siis läks mu enda hostitud domain, kahjuks peate selle ise uuesti välja nuputama.
        time.sleep(5)
        t12 = os.path.isfile(a1a)
        if t12:
            print("\n" + 'UPDATE DOWNLOADED AND FOUND BY PROGRAM, CONTINUING...' + "\n")
            os.system(f'start {a1a}')
            print(CRED + 'closing and deleting this version' + CEND + "\n")
            time.sleep(2)

            old_name = sys.argv[0]
            new_name = os.path.dirname(sys.argv[0]) + "\\oldversion.tmp"
            os.rename(old_name, new_name)

            try:
                exit()
            except Exception as err:
                print(err)
            sys.exit()
            os.close()


        else:
            print(CRED + "UPDATE DOWNLOAD FAILED, PLEASE REDOWNLOAD PROGRAM FROM DISCORD\nEXITING IN 5 SECONDS...")
            time.sleep(5)
            sys.exit()

    print('Connected to siegeMP discord server')
    await  bot.change_presence(activity=discord.Activity
    (type=discord.ActivityType.playing, name=".KEY"))

    try:
        with open('saved_dictionary.pkl', 'rb') as f:
            loaded_dict = pickle.load(f)
        with open('saved_list.pkl', 'rb') as r:
            loaded_keys = pickle.load(r)
    except:
        log = bot.get_channel(1099368067403874377)
        await log.send("No save file was found, all keys and accounts have been reset.")
        print("No save file was found, all keys and accounts have been reset.")
        return

    global accounts
    global keys

    accounts = loaded_dict
    keys = loaded_keys

    print('loaded recent save')


@bot.command()
async def save(ctx):
    if ctx.author.id in privileged_accounts:
        pass
    else:
        ctx.send("Not authorized")
        return
    await ctx.send('saving...')
    with open('saved_dictionary.pkl', 'wb') as f:
        pickle.dump(accounts, f)

    with open('saved_list.pkl', 'wb') as a:
        pickle.dump(keys, a)

    await ctx.send('save was succsesful ( i have no clue how you spell it )')


@bot.command()
async def load(ctx):
    if ctx.author.id in privileged_accounts:
        pass
    else:
        ctx.send("Not authorized")
        return

    with open('saved_dictionary.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)
    with open('saved_list.pkl', 'rb') as r:
        loaded_keys = pickle.load(r)

    global accounts
    global keys

    accounts = loaded_dict
    keys = loaded_keys


@bot.command()
async def key(ctx, *args):
    if int(ctx.channel.id) == 1099363028731969567:
        print('GENERAL MESSAGE DECLINED')
        log = bot.get_channel(1099368067403874377)
        await log.send(f'GENERAL MESSAGE DECLINED, TRIGGERED BY {ctx.author}')
        return

    int_aa = 0
    for key_a in keys:
        if key_a in args:
            keys.remove(str(key_a))
            # keys are the usernames and values are passwords

            aa = get(accounts.values())
            bb = get(accounts.keys())
            try:
                await ctx.send(aa + " : " + bb)
            except:
                await ctx.send("We have ran into an issue and staff has been notified, please come back later.")
                channel = 1099368067403874377
                log = bot.get_channel(1099368067403874377)
                await log.send("We have ran out of accounts, please feed me father.")
                return
            del accounts[bb]

        else:
            int_aa += 1
            if int_aa == len(keys):
                await ctx.send("Key not found")


@bot.command()
async def refill(ctx, *args):
    if ctx.author.id in privileged_accounts:
        pass
    else:
        ctx.send("Not authorized")
        return
    if args[0] == 'account':
        await ctx.send('accounts selected')
        channel = ctx.channel
        await channel.send('type your account information below, please enter one account at a time.')

        def check(m):
            if m.author.id == 425545896873426944:
                return m.channel == channel

        msg = await bot.wait_for('message', check=check)
        formated = str(format(msg.content)).replace(':', '\n')
        splitted = formated.split('\n')
        accounts.update({splitted[0]: splitted[1]})

        return


    elif args[0] == 'keys':
        await ctx.send('keys selected')
        channel = ctx.channel
        await channel.send('type your keys below, please type one key at a time.')

        def check(m):
            if m.author.id == 425545896873426944:
                return m.channel == channel

        msg = await bot.wait_for('message', check=check)
        formated = str(format(msg.content)).replace(':', '\n')
        keys.append(formated)

        return

    else:
        await ctx.send('are you retarded?')

        return


@bot.command()
async def clean(ctx):
    if ctx.author.id in privileged_accounts:
        pass
    else:
        ctx.send("Not authorized")
        return
    accounts.clear()
    keys.clear()


@bot.command()
async def help(ctx):
    await ctx.send('Please state your problems in the ticket system.')


@bot.command()
async def database(ctx):
    if ctx.author.id in privileged_accounts:
        pass
    else:
        ctx.send("Not authorized")
        return
    print(accounts)
    print(keys)


@bot.command()
async def quit(ctx):
    if ctx.author.id in privileged_accounts:
        pass
    else:
        ctx.send("Not authorized")
        return

    await ctx.send('saving and then quiting.')
    with open('saved_dictionary.pkl', 'wb') as f:
        pickle.dump(accounts, f)
    with open('saved_list.pkl', 'wb') as a:
        pickle.dump(keys, a)

    await ctx.send('save was succsesful ( i have no clue how you spell it )')
    sys.exit()


bot.run(str(token))

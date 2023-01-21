from os.path import exists
import os
import discord
from discord.ext import tasks
from dataimport import *
from os.path import exists
import calendar
from dotenv import load_dotenv

def configure():
    load_dotenv()

def mainDiscord():
    TOKEN = os.getenv("decaDiscord")
    intents = discord.Intents(messages=True, guilds=True, message_content=True)
    client = discord.Client(intents=intents)
    configure()

    def rstockChange(s):
        reload()
        final=["Stock for {}\n".format(s)]

        for y in range(1,c+1):
            t=ral[y][s]
            final.append(t["sp500growth"]+" | "+t[""])


        return final


    def reload():
        global c,rl, nl, ral, nal
        c = len(os.listdir('rdata/'))
        rl = rdailyimporter(c)
        nl = ndailyimporter(c)
        ral = rlimporter()
        nal = nlimporter()
        return [c,rl, nl, ral, nal]

    def stringSmaller(new):
        full=[]
        if len(new) > 1000:
            s = list(new.split("\n"))
            u = len(new) // 600
            p = len(s) // u
            new = ''
            tem = 0
            for i, x in enumerate(s):
                new += x + '\n'
                tem += 1
                if p == tem:
                    tem = 0

                    full.append(new)
                    new = ''
            if new != '':
                full.append(new)
        else:
            full.append(new)

        return full

    def rranker(n):
        if n>400:
            return "num too large"

        reload()
        a=rdailyimporter(c)
        b=rdailyimporter(c-1)

        s='Update on rank: \nrank change | sp500 change | equity change | teamname | school\n'
        for xx in a:
            x=a[xx]
            if int(x["rank"])<=n:
                if xx in b:
                    pa = str(int(b[xx]["rank"]) - int(x["rank"]))
                    pb = str(round(float(x["sp500growth"].replace(",",'')) - float(b[xx]["sp500growth"].replace(",",'')),2))
                    pc = str(round(float(x["totalequity"].replace(",",'')) - float(b[xx]["totalequity"].replace(",",'')),2))
                else:
                    pa = "NA"
                    pb = "NA"
                    pc = "NA"


                s+=pa+' | '+pb+' | '+pc+' | '+ xx +' | '+x["schoolname"]+"\n"

        return stringSmaller(s)



    def nranker(n):
        if n > 400:
            return "num too large"

        reload()
        a = ndailyimporter(c)
        b = ndailyimporter(c - 1)

        s = 'Update on rank: \nrank change | sp500 change | equity change | teamname | school\n'
        for xx in a:
            x = a[xx]
            if int(x["rank"]) <= n:
                if xx in b:
                    pa = str(int(b[xx]["rank"]) - int(x["rank"]))
                    pb = str(round(float(x["sp500growth"].replace(",",'')) - float(b[xx]["sp500growth"].replace(",",'')),2))
                    pc = str(round(float(x["totalequity"].replace(",",'')) - float(b[xx]["totalequity"].replace(",",'')),2))
                else:
                    pa = "NA"
                    pb = "NA"
                    pc = "NA"

                s += pa + ' | ' + pb + ' | ' + pc + ' | ' + xx + ' | ' + x["schoolname"] + "\n"

        return stringSmaller(s)


    def daily():
        if c==1 or c==0: return ["Not enough data to conduct report\n"]
        a=rdailyimporter(c)
        b=rdailyimporter(c-1)
        ba=0
        bb=0
        bc=0

        for xx in a:
            x=a[xx]
            if int(x["rank"])==25:
                ba=float(x["sp500growth"])
            if xx == "DEC_11_ZZ529".lower():
                bb=float(x["sp500growth"])
                bc=int(x["rank"])
        for xx in b:
            x=b[xx]
            if int(x["rank"])==25:
                ba-=float(x["sp500growth"])
            if xx == "DEC_11_ZZ529".lower():
                bb-=float(x["sp500growth"])
                bc -= int(x["rank"])

        if c == 1 or c==0: return ["Not enough data to conduct report\n"]
        a = ndailyimporter(c)
        b = ndailyimporter(c - 1)
        bba = 0
        bbc = 0
        for xx in a:
            x=a[xx]
            if int(x["rank"]) == 125:
                bba = float(x["sp500growth"])
            if xx == "DEC_11_ZZ529".lower():
                bbc = int(x["rank"])
        for xx in b:
            x=b[xx]
            if int(x["rank"]) == 125:
                bba -= float(x["sp500growth"])
            if xx == "DEC_11_ZZ529".lower():
                bbc -= int(x["rank"])

        s = "Daily update: \n"
        s += "top 25 regional Change is " + str(round(ba,2)) + "\n"
        s += "top 125 national Change is " + str(round(bba,2)) + "\n"
        s += "Your regional rank change is " + str(bc) + "\n"
        s += "Your national rank change is " + str(bbc) + "\n"
        s += "Your smp 500 change is " + str(round(bb,2)) + "\n"


        return s



    def fileAdder(s):
        t=1
        while exists("exports/main{}".format(t)): t+=1

        with open('exports/main{}.txt'.format(t), 'w') as f:
            f.write(s)
        f.close()


    @tasks.loop(seconds=1)
    async def checker():
        channel = client.get_channel(1042347081018392616)

        for x in os.listdir("exports/"):
            myfile = open("exports/"+x)
            mystuff = myfile.read()
            myfile.close()
            os.remove("exports/" + x)
            await channel.send(mystuff)


    @client.event
    async def on_ready():

        print('online')
        checker.start()


    @client.event
    async def on_message(message):
        if (message.author.id != 1040107450390544427):

            msg = message.content.lower()
            reload()

            if message.content.startswith("!calendar "):
                if 2 == len(msg.split(" ")):
                    if not msg.split(" ")[1].isdigit():
                        await message.channel.send("print correctly")
                    else:
                        mm = int(msg.split(" ")[1])
                        year = 2023

                        s = "```" + calendar.month(year, mm) + "```"

                        for b in range(33):
                            b = str(b)
                            s = s.replace(' ' + b + ' ', ' .' + b + ' ')
                            s = s.replace('\n' + b + ' ', '\n.' + b + ' ')
                            s = s.replace(' ' + b + '\n', ' .' + b + '\n')
                            s = s.replace('\n' + b + '\n', '\n.' + b + '\n')

                        c = "Mo Tu We Th Fr Sa Su"
                        for x in list(c.split(' ')):
                            s = s.replace(x, x + " ")

                        for x in os.listdir('rdata/'):
                            x = (x[:-4])
                            a, b = x.split("-")
                            if int(a) == mm:
                                s = s.replace(' .' + b + ' ', ' !' + b + ' ')
                                s = s.replace('\n.' + b + ' ', '\n!' + b + ' ')
                                s = s.replace(' .' + b + '\n', ' !' + b + '\n')
                                s = s.replace('\n.' + b + '\n', '\n!' + b + '\n')

                        await message.channel.send(s)

                else:
                    await message.channel.send("bro input it correctly")

            if msg == "!download":
                s = datetime.datetime.now()
                d = str(s.month) + "-" + str(s.day)
                if exists("rdata/{}.xml".format(d)):
                    await message.channel.send("already download today")
                else:
                    await message.channel.send("Attempting...")
                    try:
                        fulldownload()
                        await client.get_channel(1045882549114765382).send(file=discord.File("rdata/{}.xml".format(d)))
                        await client.get_channel(1045876530288545894).send(file=discord.File("ndata/{}.xml".format(d)))
                        await message.channel.send('complete')
                    except:
                        await message.channel.send('something is broken')
                    await client.get_channel(1042998479984807937).send(daily())
                    for x in rranker(25):
                        await client.get_channel(1042998479984807937).send(x)
                    for x in nranker(25):
                        await client.get_channel(1042998479984807937).send(x)


            if msg == "!online":
                await message.channel.send('Hello Dad!')


            if message.content.startswith("!rprinter "):
                if 2 == len(msg.split(" ")):
                    dd = list(msg.split(" ")[1].split("-"))
                    if len(dd)==2:
                        for x in rranker(dd):
                            await message.channel.send(x)
                    else:
                        await message.channel.send("bro input it correctly")

            if message.content.startswith("!rranker "):
                if 2 == len(msg.split(" ")):
                    dd = int(msg.split(" ")[1])
                    for x in rranker(dd):
                        await message.channel.send(x)
                else:
                    await message.channel.send("bro input it correctly")


            if message.content.startswith("!nranker "):
                if 2 == len(msg.split(" ")):
                    dd = int(msg.split(" ")[1])
                    for x in nranker(dd):
                        await message.channel.send(x)
                else:
                    await message.channel.send("bro input it correctly")


            if message.content.startswith("!rprint "):
                if 2 == len(msg.split(" ")):
                    dd = msg.split(" ")[1]
                    if dd in rl:
                        c = rl[dd]
                        s = ''
                        s += "Regional Rank:\n" + "rank: " + c["rank"] + "\n" + "equity: " + c[
                            "totalequity"] + "\n" + "smp 500 growht: " + c["sp500growth"] + "\n" + "schoolname: " + \
                             c[
                                 "schoolname"] + "\n"
                        await message.channel.send(s)
                    else:
                        await message.channel.send("that team dont exist")
                else:
                    await message.channel.send("bro input it correctly")

            if message.content.startswith("!nprint "):
                if 2 == len(msg.split(" ")):
                    dd = msg.split(" ")[1]
                    if dd in nl:
                        c = nl[dd]
                        s = ''
                        s += "National Rank:\n" + "rank: " + c["rank"] + "\n" + "equity: " + c[
                            "totalequity"] + "\n" + "smp 500 growht: " + c["sp500growth"] + "\n" + "schoolname: " + \
                             c[
                                 "schoolname"] + "\n"
                        await message.channel.send(s)
                    else:
                        await message.channel.send("that team dont exist")
                else:
                    await message.channel.send("bro input it correctly")



            if message.content.startswith("!rlist "):
                if not 2 == len(msg.split(" ")):
                    await message.channel.send("bro input it correctly")
                else:
                    dd = msg.split(" ")[1]
                    tem = []
                    for y in rl:
                        x = rl[y]
                        if x["schoolname"] == dd:
                            tem.append([y, x["rank"]])
                    if tem == []:
                        await message.channel.send("none found")
                    else:
                        s = 'Regional List:\n'
                        for x in tem:
                            s += x[1] + " " + x[0] + '\n'
                        await message.channel.send(s)

            if message.content.startswith("!nlist "):
                if 2 == len(msg.split(" ")):
                    dd = msg.split(" ")[1]
                    tem = []
                    for y in nl:
                        x = nl[y]
                        if x["schoolname"] == dd:
                            tem.append([y, x["rank"]])
                    if tem == []:
                        await message.channel.send("none found")
                    else:
                        s = 'National List:\n'
                        for x in tem:
                            s += x[1] + " " + x[0] + '\n'
                        await message.channel.send(s)
                else:
                    await message.channel.send("bro input it correctly")

            if message.content.startswith("!rupdate "):
                if 2 != len(msg.split(" ")):
                    await message.channel.send("bro input it correctly")
                else:

                    dd = msg.split(" ")[1]
                    if dd.isnumeric() == False:
                        await message.channel.send("bro input it correctly")

                    else:
                        e=reload()
                        dd = int(dd)
                        t = rdailyimporter(e[0] - 1)

                        # new
                        new = 'New teams in top {}:\n'.format(dd)
                        for x in rl:
                            if int(rl[x]['rank']) <= dd:
                                if (x not in t) or int(t[x]['rank']) > dd:
                                    new += rl[x]['rank'] + " | "
                                    new += ("NA" if x not in t else t[x]['rank']) + " | "
                                    new += (str(round(float(rl[x]['sp500growth']) - float(t[x]['sp500growth']),
                                                      2)) if (
                                            (x in rl) and x in t) else "NA") + " | "
                                    new += x + " | "
                                    new += rl[x]['schoolname'] + '\n'

                        new += "\nTeams that dropped from top {}:\n".format(dd)

                        # dropped
                        for x in t:
                            if int(t[x]['rank']) <= dd:
                                if (x not in rl) or int(rl[x]['rank']) > dd:
                                    new += ("NA" if x not in rl else rl[x]['rank']) + " | "
                                    new += t[x]['rank'] + " | "
                                    new += (str(round(float(rl[x]['sp500growth']) - float(t[x]['sp500growth']),
                                                      2)) if (
                                            (x in rl) and x in t) else "NA") + " | "
                                    new += x + " | "
                                    new += t[x]['schoolname'] + '\n'

                        if len(new) > 1000:
                            s = list(new.split("\n"))
                            u = len(new) // 600
                            p = len(s) // u
                            new = ''
                            tem = 0
                            for i, x in enumerate(s):
                                new += x + '\n'
                                tem += 1
                                if p == tem:
                                    tem = 0

                                    await message.channel.send(new)
                                    new = ''
                            if new != '':
                                await message.channel.send(new)
                        else:
                            await message.channel.send(new)

            if message.content.startswith("!nupdate "):
                if 2 != len(msg.split(" ")):
                    await message.channel.send("bro input it correctly")
                else:

                    dd = msg.split(" ")[1]
                    if dd.isnumeric() == False:
                        await message.channel.send("bro input it correctly")

                    else:
                        e=reload()
                        dd = int(dd)
                        t = ndailyimporter(e[0] - 1)

                        # new
                        new = 'New teams in top {}:\n'.format(dd)
                        for x in nl:

                            if int(nl[x]['rank']) <= dd:
                                if (x not in t) or int(t[x]['rank']) > dd:
                                    new += nl[x]['rank'] + " | "
                                    new += ("NA" if x not in t else t[x]['rank']) + " | "
                                    new += (str(round(float(nl[x]['sp500growth']) - float(t[x]['sp500growth']),
                                                      2)) if (
                                            (x in nl) and x in t) else "NA") + " | "
                                    new += x + " | "
                                    new += nl[x]['schoolname'] + '\n'

                        new += "\nTeams that dropped from top {}:\n".format(dd)

                        # dropped
                        for x in t:
                            if int(t[x]['rank']) <= dd:
                                if (x not in nl) or int(nl[x]['rank']) > dd:
                                    new += ("NA" if x not in nl else nl[x]['rank']) + " | "
                                    new += t[x]['rank'] + " | "
                                    new += (str(round(float(nl[x]['sp500growth']) - float(t[x]['sp500growth']),
                                                      2)) if (
                                            (x in nl) and x in t) else "NA") + " | "
                                    new += x + " | "
                                    new += t[x]['schoolname'] + '\n'

                        if len(new) > 1000:
                            s = list(new.split("\n"))
                            u = len(new) // 600
                            p = len(s) // u
                            new = ''
                            tem = 0
                            for i, x in enumerate(s):
                                new += x + '\n'
                                tem += 1
                                if p == tem:
                                    tem = 0

                                    await message.channel.send(new)
                                    new = ''
                            if new != '':
                                await message.channel.send(new)
                        else:
                            await message.channel.send(new)

            if msg == "!daily":
                await message.channel.send(daily())



    client.run(TOKEN)


if __name__ == "__main__":
    mainDiscord()
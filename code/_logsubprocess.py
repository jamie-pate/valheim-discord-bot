from datetime import datetime
from socket import timeout
import time, os, re, a2s
import csv, asyncio
import config

## Added new regex define to pickup spaces, if character names have additional characters and are not being picked up add them inside brackets i.e. [\w ']+
## regex101.com will assist with making sure names are parsed correctly
## use pdeath inside quotes as search criteria
## use '10/12/2021 01:14:24: Got character ZDOID from Example : 0:0' as search string

pdeath = '.*?Got character ZDOID from ([\w ]+) : 0:0'
log = config.file

async def timenow():
    now = datetime.now()
    gettime = now.strftime("%d/%m/%Y %H:%M:%S")
    return gettime

async def writecsv():
    while True:    
        try:
            server = a2s.info(config.SERVER_ADDRESS)
            with open('csv/playerstats.csv', 'a', newline='') as f:
                csvup = csv.writer(f, delimiter=',')
                curtime, players = await timenow(), server.player_count
                csvup.writerow([curtime, players])
                print(curtime, players)
        except timeout:
            with open('csv/playerstats.csv', 'a', newline='') as f:
                csvup = csv.writer(f, delimiter=',')  
                curtime, players = await timenow(), '0'
                csvup.writerow([curtime, players])
                print(curtime, 'Cannot connect to server')
        await asyncio.sleep(60)

async def deathcount():
    while True:           
        with open(log, encoding='utf-8', mode='r') as f:
            f.seek(0,2)
            while True:
                line = f.readline()
                if(re.search(pdeath, line)):
                    pname = re.search(pdeath, line).group(1)
                    with open('csv/deathlog.csv', 'a', newline='', encoding='utf-8') as dl:
                        curtime = await timenow()
                        deathup = csv.writer(dl, delimiter=',')
                        deathup.writerow([curtime, pname])
                        print(curtime, pname, ' has died!')
                await asyncio.sleep(0.2)

loop = asyncio.get_event_loop()
loop.create_task(deathcount())
loop.create_task(writecsv())
loop.run_forever()

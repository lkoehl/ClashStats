import discord 
from dotenv import dotenv_values
import sqlite3
conn = sqlite3.connect('./ClashStats/ClashStats.db')
c = conn.cursor()

config = dotenv_values("./ClashStats/.env")  
TOKEN = config["DISCORD_TOKEN"]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        
        if message.author == self.user:
            return

        if message.content == '>help':
            response = 'Known commands to ClashStatsBot\n```\n>help - Shows the help menu\n>ping - Pings the bot and if I am online you should get a response\n>list attacks - List Avg. Destruction of all war attacks known\n>list attacks <number> - Limit the number of results to <number>\n>list defences - List Avg. Destruction of all war defences known\n>list defences <number> - Limit the number of results to <number>\n```'
            await message.channel.send(response)

        if message.content == '>ping':
            await message.channel.send("pong")

        if ">list attacks" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Attacks ' + '\n\n'

            content = message.content.split(" ")
            try:
                limit = content[2]
            except IndexError:
                # List all of them
                for row in c.execute('select members.name as "Player", avg(attacks.destruction) as "Avg Destruction", count(attacks.destruction) as "Number of attacks" from attacks inner join members on members.id = attacks.attacker group by attacks.attacker order by avg(attacks.destruction) desc', []):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'
            else:
                # List with limit
                 for row in c.execute('select members.name as "Player", avg(attacks.destruction) as "Avg Destruction", count(attacks.destruction) as "Number of attacks" from attacks inner join members on members.id = attacks.attacker group by attacks.attacker order by avg(attacks.destruction) desc limit (?)', [limit]):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'

            response = response + '\n```'
            await message.channel.send(response) 

        if ">list member attacks" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Attacks ' + '\n\n'

            content = message.content.split(" ")
            try:
                date = content[3]
            except IndexError:
                # List all of them
                print("Do nothing")
            else:
                # List with limit
                 for row in c.execute('select members.name as "Player", avg(attacks.destruction) as "Avg Destruction", count(attacks.destruction) as "Number of attacks" from attacks inner join members on members.id = attacks.attacker where members.id in (select members.id from attacks inner join members on members.id = attacks.attacker inner join war on attacks.war_id = war.war_id  where war.start_date >= (?) group by members.id) group by attacks.attacker order by avg(attacks.destruction) desc', [date]):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'

            response = response + '\n```'
            await message.channel.send(response) 

        if ">list defences" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Defences ' + '\n\n'

            content = message.content.split(" ")
            try:
                limit = content[2]
            except IndexError:
                # List all of them
                for row in c.execute('select members.name as "Player", avg(defence.destruction) as "Avg Destruction", count(defence.destruction) as "Number of defences" from defence inner join members on members.id = defence.defender group by defence.defender order by avg(defence.destruction) asc', []):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'
            else:
                # List with limit
                 for row in c.execute('select members.name as "Player", avg(defence.destruction) as "Avg Destruction", count(defence.destruction) as "Number of defences" from defence inner join members on members.id = defence.defender group by defence.defender order by avg(defence.destruction) asc limit (?)', [limit]):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'

            response = response + '\n```'
            await message.channel.send(response) 

        if message.content == '>wars':
            response = 'All known wars to ClashStatsBot\n```'

            for row in c.execute('select start_date from war', []):
                    response = response + str(row[0]) + '\n'
            
            for row in c.execute('select count(start_date) from war', []):
                    response = response + '\nTotal Number of Wars: ' + str(row[0]) + '\n'

            response = response + '\n```'
            await message.channel.send(response)


client = MyClient()

client.run(TOKEN)
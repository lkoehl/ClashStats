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
            response = 'Known commands to ClashStatsBot\n```\n>help - Shows the help menu\n>ping - Pings the bot and if I am online you should get a response\n>list attacks - List Avg. Destruction of all war attacks known\n>list attacks since <date> - Only includes data newer then <date>\n>list attacks in war <war_id> - Only includes data from the specific war\n>list member attacks <date> - Include all the data, but only from members seen since <date>\n>list defences - List Avg. Destruction of all war defences known\n>list defences since <date> - Only includes data newer then <date>\n>list attacks in war <war_id> - Only includes data from the specific war\n>list member defences <date> - Include all the data, but only from members seen since <date>\n>wars - List all wars known to the bot\n```'
            await message.channel.send(response)

        if message.content == '>ping':
            await message.channel.send("pong")

        if message.content == ">list attacks":
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Attacks ' + '\n\n'

            # List all of them
            for row in c.execute('select members.name as "Player", avg(attacks.destruction) as "Avg Destruction", count(attacks.destruction) as "Number of attacks" from attacks inner join members on members.id = attacks.attacker group by attacks.attacker order by avg(attacks.destruction) desc', []):
                response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'

            response = response + '\n```'
            await message.channel.send(response) 

        if ">list attacks since" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Attacks ' + '\n\n'

            content = message.content.split(" ")

            try:
                date = content[3]
            except IndexError:
                await message.channel.send("Date Format wrong. Use 20210501 (1st May of 2021).")
            else:
                for row in c.execute('select members.name as "Player", avg(attacks.destruction) as "Avg Destruction", count(attacks.destruction) as "Number of attacks" from attacks inner join members on members.id = attacks.attacker where attacks.id in (select attacks.id from attacks inner join members on members.id = attacks.attacker inner join war on attacks.war_id = war.war_id where war.start_date >= (?)) group by attacks.attacker order by avg(attacks.destruction) desc', [date]):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'
                response = response + '\n```'
                await message.channel.send(response)

        if ">list attacks in war" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Attacks ' + '\n\n'

            content = message.content.split(" ")

            try:
                war_id = content[4]
            except IndexError:
                await message.channel.send("Date Format wrong. Use 20210501 (1st May of 2021).")
            else:
                for row in c.execute('select members.name as "Player", avg(attacks.destruction) as "Avg Destruction", count(attacks.destruction) as "Number of attacks" from attacks inner join members on members.id = attacks.attacker where attacks.id in (select attacks.id from attacks inner join members on members.id = attacks.attacker inner join war on attacks.war_id = war.war_id where war.war_id = (?)) group by attacks.attacker order by avg(attacks.destruction) desc', [war_id]):
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
                await message.channel.send("Date Format wrong. Use 20210501 (1st May of 2021).")
            else:
                for row in c.execute('select members.name as "Player", avg(attacks.destruction) as "Avg Destruction", count(attacks.destruction) as "Number of attacks" from attacks inner join members on members.id = attacks.attacker where members.id in (select members.id from attacks inner join members on members.id = attacks.attacker inner join war on attacks.war_id = war.war_id  where war.start_date >= (?) group by members.id) group by attacks.attacker order by avg(attacks.destruction) desc', [date]):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'
                response = response + '\n```'
                await message.channel.send(response)

        if ">list defences" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Defences ' + '\n\n'

            content = message.content.split(" ")

            # List all of them
            for row in c.execute('select members.name as "Player", avg(defence.destruction) as "Avg Destruction", count(defence.destruction) as "Number of defences" from defence inner join members on members.id = defence.defender group by defence.defender order by avg(defence.destruction) asc', []):
                response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'
            
            response = response + '\n```'
            await message.channel.send(response) 
        
        if ">list defences since" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Defences ' + '\n\n'

            content = message.content.split(" ")

            try:
                date = content[3]
            except IndexError:
                await message.channel.send("Date Format wrong. Use 20210501 (1st May of 2021).")
            else:
                for row in c.execute('select members.name as "Player", avg(defence.destruction) as "Avg Destruction", count(defence.destruction) as "Number of defences" from defence inner join members on members.id = defence.defender where defence.id in (select defence.id from defence inner join members on members.id = defence.defender inner join war on defence.war_id = war.war_id where war.start_date >= (?)) group by defence.defender order by avg(defence.destruction) asc', [date]):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'
                response = response + '\n```'
                await message.channel.send(response)

        if ">list defences in war" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Defences ' + '\n\n'

            content = message.content.split(" ")

            try:
                war_id = content[4]
            except IndexError:
                await message.channel.send("Date Format wrong. Use 20210501 (1st May of 2021).")
            else:
                for row in c.execute('select members.name as "Player", avg(defence.destruction) as "Avg Destruction", count(defence.destruction) as "Number of defences" from defence inner join members on members.id = defence.defender where defence.id in (select defence.id from defence inner join members on members.id = defence.defender inner join war on defence.war_id = war.war_id where war.war_id = (?)) group by defence.defender order by avg(defence.destruction) asc', [war_id]):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'
                response = response + '\n```'
                await message.channel.send(response)
        
        if ">list member defences" in message.content:
            response = '```\n'
            response = response + 'Player Name' + ' - ' + 'Avg. Destruction' + ' - ' + 'Number of Defences ' + '\n\n'

            content = message.content.split(" ")
            try:
                date = content[3]
            except IndexError:
                await message.channel.send("Date Format wrong. Use 20210501 (1st May of 2021).")
            else:
                for row in c.execute('select members.name as "Player", avg(defence.destruction) as "Avg Destruction", count(defence.destruction) as "Number of defences" from defence inner join members on members.id = defence.defender where members.id in (select members.id from defence inner join members on members.id = defence.defender inner join war on defence.war_id = war.war_id  where war.start_date >= (?) group by members.id) group by defence.defender order by avg(defence.destruction) asc', [date]):
                    response = response + str(row[0]) + ' - ' + str(round(row[1]))+ '% - ' + str(row[2]) + '\n'
                response = response + '\n```'
                await message.channel.send(response)

        if message.content == '>wars':
            response = 'All known wars to ClashStatsBot\n```'

            for row in c.execute('select start_date, war_id from war', []):
                    response = response + str(row[1]) + ' - ' + str(row[0]) + '\n'
            
            for row in c.execute('select count(start_date) from war', []):
                    response = response + '\nTotal Number of Wars: ' + str(row[0]) + '\n'

            response = response + '\n```'
            await message.channel.send(response)


client = MyClient()

client.run(TOKEN)
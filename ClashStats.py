from cocapi import CocApi
from dotenv import dotenv_values
import sqlite3

# conn = sqlite3.connect('./ClashStats/ClashStats.db')
conn = sqlite3.connect('./ClashStats.db')
c = conn.cursor()

config = dotenv_values(".env")  

token = config["CLASH_TOKEN"]
timeout=1 #requests timeout

api=CocApi(token,timeout)

clanTag = config["CLAN_TAG"]
war = api.clan_current_war(clanTag)
print(war)

league = api.clan_leaguegroup(clanTag)
print(league)

print(war["startTime"])
members = war["clan"]["members"]

startTime = war["startTime"]
try:
    print("Add new war to database")
    c.execute("INSERT INTO war (start_date) VALUES (?)", [startTime])
except:
    print("War already exists")

try:
    for row in c.execute('SELECT war_id FROM war WHERE start_date = (?)', [startTime]):
            war_id = row[0]
except:
    print("No war selected")

for member in members:
    try:
        name = member["name"]
        tag = member["tag"]
        c.execute("INSERT INTO members VALUES (?, ?)", [tag, name])
        print("Added new attacker to Database", name, tag)
    except:
        print("User already exists in database")
        
for member in members:
    try:
        attacks = member["attacks"]
        for attack in attacks:
            attacker = attack["attackerTag"]
            defender = attack["defenderTag"]
            stars = attack["stars"]
            destruction = attack["destructionPercentage"] 

            for row in c.execute('SELECT COUNT(*) FROM attacks WHERE attacker = (?) AND defender = (?) AND war_id = (?)', [attacker, defender, war_id]):
                count = row[0]

            if count == 0:
                c.execute('INSERT INTO attacks (attacker, defender, stars, destruction, war_id) VALUES (?, ?, ?, ?, ?)' , [attacker, defender, stars, destruction, war_id])
            else:
                print("Attack already exists in database")
            print(attacker, defender, stars, destruction)
    except:
        print("Not attacked yet")


opponents = war["opponent"]["members"]
for opponent in opponents:
    try:
        attacks = opponent["attacks"]
        for attack in attacks:
            attacker = attack["attackerTag"]
            defender = attack["defenderTag"]
            stars = attack["stars"]
            destruction = attack["destructionPercentage"] 

            for row in c.execute('SELECT COUNT(*) FROM defence WHERE attacker = (?) AND defender = (?) AND war_id = (?)', [attacker, defender, war_id]):
                count = row[0]

            if count == 0:
                c.execute('INSERT INTO defence (attacker, defender, stars, destruction, war_id) VALUES (?, ?, ?, ?, ?)' , [attacker, defender, stars, destruction, war_id])
            else:
                print("Defence already exists in database")
            print(attacker, defender, stars, destruction)
    except:
        print("Not defenced yet")

conn.commit()
conn.close()


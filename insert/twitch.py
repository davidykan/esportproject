import MySQLdb, requests, urllib.parse, datetime, json
from language import language_array

def twitch_function():
    game = ["Smite", "Dark Souls III", "Final Fantasy XV", "Dark Souls II%3A Scholar of the First Sin", "The Culling", "FIFA 16", "Clash Royale", "Rocket League", "World of Tanks", "Diablo III: Reaper of Souls", "StarCraft: Brood War", "H1Z1: King of the Kill", "Grand Theft Auto V", "Black Desert", "Tom Clancy%27s The Division", "Tom Clancy%27s Rainbow Six: Siege", "Counter-Strike: Global Offensive", "Hearthstone: Heroes of Warcraft", "Dota 2", "SpeedRunners", "Call of Duty: Black Ops III", "Garry%27s Mod", "Minecraft", "Stardew Valley", "HITMAN", "World of Warcraft", "Destiny", "StarCraft II", "Heroes of the Storm", "Diablo II: Lord of Destruction", "League of Legends"]
    twitch_id=[]
    for g in game:
        json_data = json.loads(requests.get('https://api.twitch.tv/kraken/streams?game='+urllib.parse.quote(g)+'&limit=100&offset=0').text)
        for l in range(len(json_data['streams'])):
            twitch_id.append(json_data['streams'][l]['channel']['name'])

    conn = MySQLdb.connect()
    c = conn.cursor()
    c.execute("select name_id from newapp_entry where source='twitch'")
    conn.commit()

    database_id=[]
    for a in c:
        database_id.append(a[0])

    notonline=[]
    if database_id:
        for a in database_id:
            if a not in twitch_id:
                notonline.append(a)

    if notonline:
        for a in notonline:
            conn = MySQLdb.connect("davidykan.mysql.pythonanywhere-services.com", "davidykan", "qwerqwer", "davidykan$default", charset='utf8')
            c = conn.cursor()
            c.execute("UPDATE newapp_entry SET time = '"+str(datetime.datetime.today())+"', status = 0, viewers = 0 WHERE name_id='"+a+"' AND source='twitch'")
            conn.commit()

    for g in game:
        json_data = json.loads(requests.get('https://api.twitch.tv/kraken/streams?game='+urllib.parse.quote(g)+'&limit=100&offset=0').text)
        for l in range(len(json_data['streams'])):
            if json_data['streams'][l]['channel']['name'] in twitch_id:
                conn = MySQLdb.connect("davidykan.mysql.pythonanywhere-services.com", "davidykan", "qwerqwer", "davidykan$default", charset='utf8')
                c = conn.cursor()
                c.execute("INSERT IGNORE into newapp_entry VALUES(%s,%s, %s, %s, %s,%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE time = %s, title = %s, viewers = %s, status = 1",
                    ('Twitch_'+json_data['streams'][l]['channel']['name'],
                    datetime.datetime.today(),
                    json_data['streams'][l]['viewers'],
                    json_data['streams'][l]['channel']['name'],
                    json_data['streams'][l]['channel']['name'],
                    'Twitch',
                    json_data['streams'][l]['channel']['status'],
                    json_data['streams'][l]['preview']['medium'],
                    json_data['streams'][l]['channel']['url'],
                    1,
                    datetime.datetime.today(),
                    json_data['streams'][l]['channel']['status'],
                    json_data['streams'][l]['viewers']
                    ))
                conn.commit()

            if json_data['streams'][l]['channel']['name'] not in database_id:
                c.execute("INSERT IGNORE into newapp_game_table VALUES(%s,%s)",
                    ('Twitch_'+json_data['streams'][l]['channel']['name']+'_'+json_data['streams'][l]['channel']['game'],
                    json_data['streams'][l]['channel']['game']))
                conn.commit()

                c.execute("INSERT IGNORE into newapp_game_table_entry VALUES(%s,%s,%s)",
                    ('',
                    'Twitch_'+json_data['streams'][l]['channel']['name']+'_'+json_data['streams'][l]['channel']['game'],
                    'Twitch_'+json_data['streams'][l]['channel']['name']))
                conn.commit()

                for r in range(len(language_array)):
                    if json_data['streams'][l]['channel']['broadcaster_language'] in language_array[r]:
                        lang = language_array[r][json_data['streams'][l]['channel']['broadcaster_language']]


                if json_data['streams'][l]['channel']['broadcaster_language']:
                    c.execute("INSERT IGNORE into newapp_language_table VALUES(%s,%s)",
                        ('Twitch_'+json_data['streams'][l]['channel']['name']+'_'+lang,
                        lang))
                    conn.commit()

                    c.execute("INSERT IGNORE into newapp_language_table_entry VALUES(%s,%s,%s)",
                        ('',
                        'Twitch_'+json_data['streams'][l]['channel']['name']+'_'+lang,
                        'Twitch_'+json_data['streams'][l]['channel']['name']))
                    conn.commit()

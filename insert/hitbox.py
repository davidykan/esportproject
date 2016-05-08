import MySQLdb, requests, datetime, json
from country import country_array

def hitbox_function():
    json_data = json.loads(requests.get('http://api.hitbox.tv/api/media/live/list.json?limit=50&filter=popular').text)
    game = ["Live Show", "League of Legends", "Dota 2", "Heroes of the Storm", "Counter-Strike: Global Offensive", "FIFA 16", "Tom Clancy's The Division", "H1Z1: King of the Kill", "World of Tanks", "Tom Clancy's Rainbow Six: Siege"]
    hitbox_id=[]
    for l in range(len(json_data['livestream'])):
        if json_data['livestream'][l]['category_name'] in game:
            hitbox_id.append(json_data['livestream'][l]['media_user_name'])

    conn = MySQLdb.connect()
    c = conn.cursor()
    c.execute("select name_id from newapp_entry where source='hitbox'")
    conn.commit()

    database_id=[]
    for a in c:
        database_id.append(a[0])

    notonline=[]
    if database_id:
        for a in database_id:
            if a not in hitbox_id:
                notonline.append(a)

    if notonline:
        for a in notonline:
            conn = MySQLdb.connect("davidykan.mysql.pythonanywhere-services.com", "davidykan", "qwerqwer", "davidykan$default", charset='utf8')
            c = conn.cursor()
            c.execute("UPDATE newapp_entry SET time = '"+str(datetime.datetime.today())+"', status = 0, viewers = 0 WHERE name_id='"+a+"' AND source='hitbox'")
            conn.commit()

    for l in range(len(hitbox_id)):
        conn = MySQLdb.connect("davidykan.mysql.pythonanywhere-services.com", "davidykan", "qwerqwer", "davidykan$default", charset='utf8')
        c = conn.cursor()
        if json_data['livestream'][l]['media_status'] == "" or json_data['livestream'][l]['media_status'] == " ":
            title = 'Untitled'
        else:
            title = json_data['livestream'][l]['media_status']
        c.execute("INSERT into newapp_entry VALUES(%s,%s, %s, %s, %s,%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE time = %s, title = %s, viewers = %s, status = 1",
            ('Hitbox_'+json_data['livestream'][l]['media_user_name'],
            datetime.datetime.today(),
            json_data['livestream'][l]['media_views'],
            json_data['livestream'][l]['media_user_name'],
            json_data['livestream'][l]['media_display_name'],
            'Hitbox',
            title,
            "http://edge.sf.hitbox.tv"+json_data['livestream'][l]['media_thumbnail'],
            "http://www.hitbox.tv/"+json_data['livestream'][l]['media_user_name'].lower(),
            1,
            datetime.datetime.today(),
            title,
            json_data['livestream'][l]['media_views']))
        conn.commit()

        if json_data['livestream'][l]['media_user_name'] not in database_id:
            c.execute("INSERT IGNORE into newapp_game_table VALUES(%s,%s)",
                ('Hitbox_'+json_data['livestream'][l]['media_user_name']+'_'+json_data['livestream'][l]['category_name'],
                json_data['livestream'][l]['category_name']))
            conn.commit()

            c.execute("INSERT IGNORE into newapp_game_table_entry VALUES(%s,%s,%s)",
                ('',
                'Hitbox_'+json_data['livestream'][l]['media_user_name']+'_'+json_data['livestream'][l]['category_name'],
                'Hitbox_'+json_data['livestream'][l]['media_user_name']))
            conn.commit()


            for f in range(len(json_data['livestream'][l]['media_countries'])):
                #lang = json_data['livestream'][l]['media_countries'][f]
                for r in range(len(country_array)):
                    if json_data['livestream'][l]['media_countries'][f] in country_array[r]:
                        lang = country_array[r][json_data['livestream'][l]['media_countries'][f]]

                        c.execute("INSERT IGNORE into newapp_language_table VALUES(%s,%s)",
                            ('Hitbox_'+json_data['livestream'][l]['media_user_name']+'_'+lang,
                            lang))
                        conn.commit()

                        c.execute("INSERT IGNORE into newapp_language_table_entry VALUES(%s,%s,%s)",
                            ('',
                            'Hitbox_'+json_data['livestream'][l]['media_user_name']+'_'+lang,
                            'Hitbox_'+json_data['livestream'][l]['media_user_name']))
                        conn.commit()



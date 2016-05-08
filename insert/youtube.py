import MySQLdb, requests, urllib.parse, datetime, json

def youtube_function():
    game = ["gta", "minecraft", "division", "black ops", "black ops 3", "bo3", "clash", "smite"]
    youtube_id = []
    for g in game:
        json_data = json.loads(requests.get('https://www.googleapis.com/youtube/v3/search?part=id&type=video&maxResults=30&eventType=live&videoCategoryId=20&order=viewCount&key=AIzaSyDFEdso9vNW26UhmvFyNd94odgvdqHsUTs&q='+urllib.parse.quote(g)).text)
        for j in range(len(json_data['items'])):
            youtube_id.append(json_data['items'][j]['id']['videoId'])

    conn = MySQLdb.connect()
    c = conn.cursor()
    c.execute("select name_id from newapp_entry where source='youtube'")
    conn.commit()
    database_id=[]
    for a in c:
        database_id.append(a[0])

    notonline=[]
    for a in database_id:
        if a not in youtube_id:
            notonline.append(a)


    for a in notonline:
        conn = MySQLdb.connect("davidykan.mysql.pythonanywhere-services.com", "davidykan", "qwerqwer", "davidykan$default", charset='utf8')
        c = conn.cursor()
        c.execute("UPDATE newapp_entry SET time = '"+str(datetime.datetime.today())+"', status = 0, viewers = 0 WHERE name_id='"+a+"' AND source='youtube'")
        conn.commit()





    for y in youtube_id:
        json_id = json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&key=AIzaSyDFEdso9vNW26UhmvFyNd94odgvdqHsUTs&id='+urllib.parse.quote(y)).text)
        game_dict = {
            'Minecraft':['minecraft'],
            'Grand Theft Auto V':['gta 5', 'gta5', 'gta v', 'gtav'],
            "Tom Clancy's The Division":["division"],
            "Call of Duty: Black Ops III":["black ops|Black Ops 3|BO3"],
            "Clash Royale":["clash"],
            }
        for game_name in game_dict:
            for game_array in range(len(game_dict[game_name])):
                if game_dict[game_name][game_array].lower() in json_id['items'][0]['snippet']['title'].lower():
                    conn = MySQLdb.connect("davidykan.mysql.pythonanywhere-services.com", "davidykan", "qwerqwer", "davidykan$default", charset='utf8')
                    c = conn.cursor()
                    c.execute("INSERT into newapp_entry VALUES(%s,%s, %s, %s, %s,%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE time = %s, title = %s, viewers = %s, status = 1",
                        ('Youtube_'+y,
                        datetime.datetime.today(),
                        json_id['items'][0]['liveStreamingDetails']['concurrentViewers'],
                        y,
                        json_id['items'][0]['snippet']['channelTitle'],
                        'Youtube',
                        json_id['items'][0]['snippet']['title'],
                        json_id['items'][0]['snippet']['thumbnails']['medium']['url'],
                        "https://www.youtube.com/watch?v="+y,
                        1,
                        datetime.datetime.today(),
                        json_id['items'][0]['snippet']['title'],
                        json_id['items'][0]['liveStreamingDetails']['concurrentViewers']))
                    conn.commit()

                    if y not in database_id:
                        c.execute("INSERT IGNORE into newapp_game_table VALUES(%s,%s)",
                            ('Youtube_'+y+'_'+game_name,
                            game_name))
                        conn.commit()

                        c.execute("INSERT IGNORE into newapp_game_table_entry VALUES(%s,%s,%s)",
                            ('',
                            'Youtube_'+y+'_'+game_name,
                            'Youtube_'+y))
                        conn.commit()

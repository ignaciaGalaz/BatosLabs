import psycopg2
import csv
import re

conn = psycopg2.connect(host="localhost", user="matiastoro", database="anime", password="", port="5432")

cur = conn.cursor()

# Borra todos los datos que ya existan en las tablas
cur.execute("truncate table studio restart identity cascade")
cur.execute("truncate table anime restart identity cascade")
cur.execute("truncate table character restart identity cascade")
cur.execute("truncate table voice_actor restart identity cascade")
cur.execute("truncate table tag restart identity cascade")
cur.execute("truncate table anime_tag restart identity cascade")

studio_cache = {}
character_cache = {}
actor_cache = {}
avac_cache = {}
tag_cache = {}
at_cache = {}

with open('./Anime.csv') as csvfile:
    #delimeter: indica el caracter que se usa para separar columnas en el csv
    #quotechar: indica que se usan "" para definir cada valor
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    i = 0
    for row in reader:
        i +=1 
        if i == 1:
            continue #para que ignore la cabecera de la tabla
        #if i>3:
        #    break
        print(i)
        name = row[1] 
        episode = row[4].split(".")[0] if row[4] else None
        #print(f"name: {name} episode: {episode}")

        studio = row[5].strip()

        #primero buscamos el studio en la base de datos
        studio_id = studio_cache[studio] if studio in studio_cache else None
        if not studio_id:
            cur.execute("insert into studio (name) values (%s) returning id", [studio])
            studio_id = cur.fetchone()[0]
            studio_cache[studio] = studio_id
        #print(studio_id)

        cur.execute("insert into anime (name, episodes, studio_id) values (%s, %s, %s) returning id", [name, episode, studio_id]) #retorna el id
        anime_id = cur.fetchone()[0] #agarra lo que retorna la insercion

        voice_actors = row[15].strip()
        #print(voice_actors)

        match = re.findall('([^,]+):([^,]+)', voice_actors)
        if match:
            for m in match:
                character = m[0].strip()
                actor = m[1].strip()

                #creamos el character
                character_id = character_cache[character] if character in character_cache else None
                if not character_id:
                    cur.execute("insert into character (name) values (%s) returning id", [character])
                    character_id = cur.fetchone()[0]
                    character_cache[character] = character_id

                #creamos el actor
                actor_id = actor_cache[actor] if actor in actor_cache else None
                if not actor_id:
                    cur.execute("insert into voice_actor (name) values (%s) returning id", [actor])
                    actor_id = cur.fetchone()[0]
                    actor_cache[actor] = actor_id

                #creamos la relacion entre anime, actor y character
                if not (anime_id, actor_id, character_id) in avac_cache:
                    cur.execute("insert into anime_voice_actor_character (anime_id, voice_actor_id, character_id) values (%s, %s, %s)", [anime_id, actor_id, character_id])
                    avac_cache[(anime_id, actor_id, character_id)] = True

        #los tags
        tags = [r.strip() for r in row[7].split(",")]
        for tag in tags:
            if not tag:
                continue
            tag_id = tag_cache[tag] if tag in tag_cache else None
            if not tag_id:
                cur.execute("insert into tag (name) values (%s) returning id", [tag])
                tag_id = cur.fetchone()[0]
                tag_cache[tag] = tag_id
            
            #creamos la relacion entre anime y tag
            if not (anime_id, tag_id) in at_cache:
                cur.execute("insert into anime_tag (anime_id, tag_id) values (%s, %s)", [anime_id, tag_id])
                at_cache[(anime_id, tag_id)] = True


        #print(match)
        #print(row)

    conn.commit()


import psycopg2
import psycopg2.extras
import csv
import re


conn = psycopg2.connect ( host ="cc3201.dcc.uchile.cl",
                          database ="cc3201",
                          user ="cc3201",
                          password ="j'<3_cc3201", 
                          port ="5440")

cur = conn.cursor()

# Borra todos los datos que ya existan en las tablas
cur.execute("truncate table cardumen_superhero restart identity cascade")
cur.execute("truncate table cardumen_character restart identity cascade")
cur.execute("truncate table cardumen_alterego restart identity cascade")
cur.execute("truncate table cardumen_workOccupation restart identity cascade")
cur.execute("truncate table cardumen_superheroe_alterego restart identity cascade")
cur.execute("truncate table anime_tag restart identity cascade")

alter_egos_cache = {}
work_occupation_cache = {}
shae_cache = {} #cache relacion superheroe alterego
shwo_cache={}

with open('data.csv') as cvsfile:
    reader = csv.reader(cvsfile, delimiter=',', quotechar='"') 

    i=0
    for row in reader:
        i+=1
        if i==1:
            continue
        if i>31:
            break

        print(i-1, end=" ")

        # PUSE NONE EN CUALQUIER DATO QUE NO SE ENTREGUE

        superheroe = row[1] #nombre de superheroe
        full_name = row[8].strip() if row[8]!="" else None #nombre real
        
        # pueden estar separados por comas o punto y coma: se usan expresiones regulares
        # .replace('"', '') quita las dobles comillas
        alter_egos = [s.strip() for s in re.split(r'[;,]', row[9].replace('"', ''))] if row[9] != "No alter egos found." else None
        

        #appearance__height__001 = row[17]  # altura en pies
        #appearance__weight__001 = row[19]  # peso en libras
        # no sé si es necesario castear a int (creo que si)
        # (!!) no considera los casos en que se dan metros en vez de cm -> ej: fila 33, fila 288
        height = row[18].strip().replace(' cm', '') # altura en centimetros
        weight = row[20].strip().replace(' kg', '') # peso en kg
        
        # hace lo mismo que alter egos
        # no me fijé si los que no tienen alter ego pueden tenerl null en vez de '-'
        # algunos están escritos como '(former) trabajo' y otros como 'former trabajo'
        work_occupation = [s.strip().lower() for s in re.split(r'[;,]', row[23].replace('"', ''))] if row[23] != "-" else None

        #----------para comprobar que está funcionando-----------
        print(f"name: {superheroe}, biography name: {full_name}")

        print("   alteregos:", alter_egos)
        print("   peso:", weight)
        print("   altura:", height)
        print("   work ocupation:", work_occupation)

        ## INSERTAMOS EN LA TABLA IMAGINARIA
        # i. Inserte el superhero, obteniendo su id.
        cur.execute("INSERT INTO cardumen_superhero(name, height, weight) VALUES (%s, %s, %s) RETURNING id", [superheroe, height, weight])
        superheroe_id = cur.fetchone()[0]

        # ii. Inserte el character usando el id del punto anterior.
        if full_name is not None: # si es character
            cur.execute("INSERT INTO cardumen_character(superheroe_id, biography_name) VALUES (%s, %s)", [superheroe_id, full_name])
        
        # iii. Para cada alter ego (asuma que están separados por “,” o “;”)
            # A. Elimine espacios blancos al comienzo y al final, y comillas dobles.
            # B. Busque si ya existe el alter ego para ese superhéroe. Si no existe, insertelo.
        if alter_egos is not None:
            for alter_ego in alter_egos:
                alter_egos_id = alter_egos_cache[alter_ego] if alter_ego in alter_egos_cache else None
                if not alter_egos_id:
                    cur.execute("insert into alter_ego (name) values (%s) returning id", [alter_ego])
                    alter_egos_id = cur.fetchone()[0]
                    alter_egos_cache[alter_ego] = alter_egos_id
                if not (superheroe_id,alter_egos_id) in shae_cache:
                    cur.execute("insert into cardumen_superheroe_alterego (superheroe_id, alteregos_id) values (%s, %s)", [superheroe_id, alter_egos_id])
                    shae_cache[(superheroe_id, alter_egos_id)] = True
        
        # iv. Para cada ocupación/oficio (asuma que estan separadas por “,” o “;”)
            # A. Elimine espacios blancos al comienzo y al final, y comillas dobles.
            # B. Seleccione el id de la ocupaci´on dado el nombre de esta. Si no existe, cr´eala.
            # C. Busque si ya existe un elemento en la tabla intermedia entre superh´eroe y ocupaci´on. Si no existe insertela.
        if work_occupation is not None:
            for i in work_occupation:
                work_occupation_id = work_occupation_cache[i] if i in work_occupation_cache else None
                if not work_occupation_id:
                    cur.execute("insert into cardumen_workOccupation (name) values (%s) returning id", [i])
                    work_occupation_id = cur.fetchone()[0]
                    work_occupation_cache[i] = work_occupation_id
                if not (superheroe_id,work_occupation_id) in shwo_cache:
                    cur.execute("insert into cardumen_superheroe_workOcupation (superheroe_id, workOcupation_id) values (%s, %s)", [superheroe_id, work_occupation_id])
                    shwo_cache[(superheroe_id, work_occupation_id)] = True
    
    conn.commit()
            


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
cur.execute("truncate table cardumen_superhero_alterego restart identity cascade")
cur.execute("truncate table cardumen_superhero_workoccupation restart identity cascade")

alteregos_cache = {}
work_occupation_cache = {}
shae_cache = {} #cache relacion superhero alterego
shwo_cache = {}

with open('data.csv') as cvsfile:
    reader = csv.reader(cvsfile, delimiter=',', quotechar='"') 

    i=0
    for row in reader:
        i+=1
        if i==1:
            continue
        #if i>35:
        #    break

        print(i-1, end=" ")

        # PUSE NONE EN CUALQUIER DATO QUE NO SE ENTREGUE

        superhero = row[1] #nombre de superhero
        full_name = row[8].strip() if row[8]!="" else None #nombre real
        
        # pueden estar separados por comas o punto y coma: se usan expresiones regulares
        # .replace('"', '') quita las dobles comillas
        alteregos = [s.strip() for s in re.split(r'[;,]', row[9].replace('"', ''))] if row[9] != "No alter egos found." else None
        
        # (!!) pesos y alturas con valor 0
        height = row[18].strip() # altura en centimetros, FALTA CONSIDERAR VACIOS
        weight = row[20].strip() 
        if height.count("meters") == 1:
            height = height.replace(' meters', '').strip()
            print("alturaaa:", height, ".")
            height = str(int(float(height))*100)
        else:
            height = height.replace(' cm', '')
        
        if weight.count("tons") == 1:
            weight = weight.replace(' tons', '')
            weight = str(int(weight)*1000)
        else:
            weight = weight.replace(' kg', '')
        
        # hace lo mismo que alter egos
        # no me fijé si los que no tienen alter ego pueden tenerl null en vez de '-'
        # algunos están escritos como '(former) trabajo' y otros como 'former trabajo'
        work_occupation = [s.strip().lower() for s in re.split(r'[;,]', row[23].replace('"', ''))] if row[23] != "-" else None

        #----------para comprobar que está funcionando-----------
        print(f"name: {superhero}, biography name: {full_name}")

        print("   alteregos:", alteregos)
        print("   peso:", weight)
        print("   altura:", height)
        print("   work occupation:", work_occupation)

        print(type(weight)==str)
        print(type(height)==str)

        ## INSERTAMOS EN LA TABLA IMAGINARIA
        # i. Inserte el superhero, obteniendo su id.
        cur.execute("INSERT INTO cardumen_superhero(name, height, weight) VALUES (%s, %s, %s) RETURNING id", [superhero, height, weight])
        superhero_id = cur.fetchone()[0]

        # ii. Inserte el character usando el id del punto anterior.
        if full_name is not None: # si es character
            cur.execute("INSERT INTO cardumen_character(superhero_id, biography_name) VALUES (%s, %s)", [superhero_id, full_name])
        
        # iii. Para cada alter ego (asuma que están separados por “,” o “;”)
            # A. Elimine espacios blancos al comienzo y al final, y comillas dobles.
            # B. Busque si ya existe el alter ego para ese superhéroe. Si no existe, insertelo.
        if alteregos is not None:
            for alterego in alteregos:
                alteregos_id = alteregos_cache[alterego] if alterego in alteregos_cache else None
                if not alteregos_id:#agregar vacios
                    cur.execute("insert into cardumen_alterego (name) values (%s) returning id", [alterego])
                    alteregos_id = cur.fetchone()[0]
                    alteregos_cache[alterego] = alteregos_id
                if not (superhero_id,alteregos_id) in shae_cache:
                    cur.execute("insert into cardumen_superhero_alterego (superhero_id, alterego_id) values (%s, %s)", [superhero_id, alteregos_id])
                    shae_cache[(superhero_id, alteregos_id)] = True
        
        # iv. Para cada ocupación/oficio (asuma que estan separadas por “,” o “;”)
            # A. Elimine espacios blancos al comienzo y al final, y comillas dobles.
            # B. Seleccione el id de la ocupaci´on dado el nombre de esta. Si no existe, cr´eala.
            # C. Busque si ya existe un elemento en la tabla intermedia entre superh´eroe y ocupaci´on. Si no existe insertela.
        if work_occupation is not None:
            for _i in work_occupation:
                work_occupation_id = work_occupation_cache[_i] if _i in work_occupation_cache else None
                if not work_occupation_id:
                    cur.execute("insert into cardumen_workOccupation (name) values (%s) returning id", [_i])
                    work_occupation_id = cur.fetchone()[0]
                    work_occupation_cache[_i] = work_occupation_id
                if not (superhero_id,work_occupation_id) in shwo_cache:
                    cur.execute("insert into cardumen_superhero_workoccupation (superhero_id, workoccupation_id) values (%s, %s)", [superhero_id, work_occupation_id])
                    shwo_cache[(superhero_id, work_occupation_id)] = True
    
    conn.commit()
            


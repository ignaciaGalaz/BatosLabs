# Integrantes: Camilo Álvarez, Ignacia Galaz A., Javier Lobos
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
shae_cache = {} #superhero alterego relation cache
shwo_cache = {} # superhero work occupation relation cache

with open('data.csv') as cvsfile:
    reader = csv.reader(cvsfile, delimiter=',', quotechar='"') 

    i=0
    for row in reader:
        i+=1
        if i==1:
            continue
        #if i>35:
        #    break

        # OBTENEMOS LOS DATOS DEL CSV
        # None en cualquier dato que no se entregue

        # Nombre de superhero
        superhero = row[1] 
        # Nombre real
        full_name = row[8].strip() if row[8]!="" else None 
        # Lista de alteregos
        alteregos = [s.strip() for s in re.split(r'[;,]', row[9].replace('"', ''))] if row[9] != "No alter egos found." else None
        
        # Altura en centimetros
        height = row[18].strip() if row[18]!='' else "0"
        if height.count("meters") == 1: # Pasa metros a centímetros
            height = height.replace(' meters', '').strip()
            height = str(int(float(height))*100)
        else:
            height = height.replace(' cm', '')
        
        # Peso en kg
        weight = row[20].strip() 
        if weight.count("tons") == 1:
            weight = weight.replace(' tons', '').replace(',','')
            weight = str(int(weight)*1000)
        else:
            weight = weight.replace(' kg', '')
        
        # Ocupación
        work_occupation = [s.strip().lower() for s in re.split(r'[;,]', row[23].replace('"', ''))] if row[23] != "-" else None

        #----------para comprobar que está funcionando----------------------
        #print(i-1, end=" ")
        #print(f"name: {superhero}, biography name: {full_name}")
        #print("   alteregos:", alteregos)
        #print("   peso:", weight)
        #print("   altura:", height)
        #print("   work occupation:", work_occupation)
        #print()
        #-------------------------------------------------------------------

        ## INSERTAMOS EN LA TABLA

        # Insertamos el superheroe
        cur.execute("INSERT INTO cardumen_superhero(name, height, weight) VALUES (%s, %s, %s) RETURNING id", [superhero, height, weight])
        superhero_id = cur.fetchone()[0]

        # Insertamos un superheroe si es character
        if full_name is not None: # si es character
            cur.execute("INSERT INTO cardumen_character(superhero_id, biography_name) VALUES (%s, %s)", [superhero_id, full_name])
        
        # Insertamos los alteregos si no existen en la tabla
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
        
        # Insertamos las ocupaciones si no existen en la tabla
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
            


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

alter_egos_cache = {}
work_occupation_cache = {}

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
        cur.execute("INSERT INTO superheores.cardumen_superhero(name, height, weight) VALUES (%s, %s, %s) RETURNING id", [superheroe, height, weight])
        superheroe_id = cur.fetchone()[0]

        # ii. Inserte el character usando el id del punto anterior.
        if full_name is not None: # si es character
            cur.execute("INSERT INTO superheores.cardumen_character(superheroe_id, biography_name) VALUES (%s, %s)", [superheroe_id, full_name])
        
        # iii. Para cada alter ego (asuma que están separados por “,” o “;”)
            # A. Elimine espacios blancos al comienzo y al final, y comillas dobles.
            # B. Busque si ya existe el alter ego para ese superhéroe. Si no existe, insertelo.
        
        # iv. Para cada ocupación/oficio (asuma que estan separadas por “,” o “;”)
            # A. Elimine espacios blancos al comienzo y al final, y comillas dobles.
            # B. Seleccione el id de la ocupaci´on dado el nombre de esta. Si no existe, cr´eala.
            # C. Busque si ya existe un elemento en la tabla intermedia entre superh´eroe y ocupaci´on. Si no existe insertela.

            


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

        superheroe_name = row[1]
        biography__full_name = row[8] if row[8]!="" else None
        
        # pueden estar separados por comas o punto y coma: se usan expresiones regulares
        # .replace('"', '') quita las dobles comillas
        biography__alter_egos = [s.strip() for s in re.split(r'[;,]', row[9].replace('"', ''))] if row[9] != "No alter egos found." else None
        

        #appearance__height__001 = row[17]  # altura en pies
        #appearance__weight__001 = row[19]  # peso en libras
        # no sé si es necesario castear a int
        appearance__height__002 = row[18].strip().replace(' cm', '') # altura en centimetros
        appearance__weight__002 = row[20].strip().replace(' kg', '') # peso en kg
        
        # hace lo mismo que alter egos
        # no me fijé si los que no tienen alter ego pueden tenerl null en vez de -
        work__occupation = [s.strip() for s in re.split(r'[;,]', row[23].replace('"', ''))] if row[23] != "-" else None

        #----------para comprobar que está funcionando-----------
        print(f"name: {superheroe_name}, biography name: {biography__full_name}")

        print("   alteregos:", biography__alter_egos)
        print("   peso:", appearance__weight__002)
        print("   altura:", appearance__height__002)
        print("   work ocupation:", work__occupation)


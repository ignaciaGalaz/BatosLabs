import psycopg2
import psycopg2.extras

def get_conn():
    conn = psycopg2.connect ( host ="cc3201.dcc.uchile.cl",
    database ="cc3201",
    user ="cc3201",
    password ="j'<3_cc3201 ", 
    port ="5440")
    return conn

get_conn()
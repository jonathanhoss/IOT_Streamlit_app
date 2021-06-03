from datetime import time
import psycopg2
import my_secrets

DB_HOST, DB_NAME, DB_USER, DB_PASS = my_secrets.db_secrets()

def get_values(name):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    with conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT zeit_lokal, ort, temperatur, feuchte, luftdruck FROM bme WHERE name = '{name}';")
            values = cur.fetchall()
    conn.close()
    return values

def querry_names():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT name FROM bme")
            values = cur.fetchall()
    conn.close()
    name_list = []
    for val in values:
        name_list.append(val[0])
    return name_list

def querry_names(): #holt alle Namen aus Liste
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT name FROM bme")
            values = cur.fetchall()
    conn.close()
    name_list = []
    for val in values:
        name_list.append(val[0])
    return name_list

def get_last(): #holt die letzen 50 werte aus Datenbank
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    with conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT name, breitengrad, laengengrad, temperatur FROM bme ORDER BY id DESC LIMIT 50;")
            values = cur.fetchall()
    conn.close()
    return values


import psycopg2
import csv

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
cur = conn.cursor()
cur.execute("""
CREATE TABLE users(
    name text,
    surname text,
    company text,
    title text,
    dateofbirth text,
    photo text
)
""")

with open('Book1.csv', 'r') as csv_file:
    csv_file.next()
    cur.copy_from(csv_file, 'users', sep=',')

conn.commit()







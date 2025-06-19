import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="admin123",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()

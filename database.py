import psycopg2

connection = psycopg2.connect(
    user = "postgres",
    password = "",
    host = "127.0.0.1",
    port = "5432",
    database = "flask"
)
cursor = connection.cursor()
print("Conectado")
create_table = """CREATE TABLE IF NOT EXISTS hoteis (hotel_id INT PRIMARY KEY, nome TEXT, estrelas REAL, diaria REAL,
cidade TEXT
    );"""

create_hotel = """
    INSERT INTO hoteis (hotel_id, nome, estrelas, diaria, cidade)
    VALUES (1, 'Alpha Hotel', 4.3, 345.40, 'Rio de Janeiro');
"""

cursor.execute(create_table) 
cursor.execute(create_hotel)

connection.commit()
connection.close()

import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('carcerale.db')
cursor = conn.cursor()


entry_date="2023-11-1"
end_date="2023-11-15"

cursor = conn.cursor()
cursor = conn.cursor()
cursor.execute("""
        SELECT prisonners.nom, prisonners.prenom
        FROM prisonners
        INNER JOIN peine ON prisonners.id = peine.user_id
        WHERE peine.entry_date >= ? AND peine.entry_date <= ?
    """, (entry_date, end_date))
print(cursor.fetchall())

conn.commit()

# Fermeture de la connexion
conn.close()
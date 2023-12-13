import sqlite3



import sqlite3

# Establishing a connection to the SQLite database
conn = sqlite3.connect("goodDB.db")

# Creating a cursor object
cursor = conn.cursor()


create_table_query = """
CREATE TABLE prison (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name_prison VARCHAR(200),
	oblast VARCHAR(100),
	number_of_prisonners INT,
	capacityPrison INT,
	prison_Type VARCHAR(100)
)
"""

# Exécution de la requête de création de la table
cursor.execute(create_table_query)




# Table des prisonniers
create_table_prisonners = """
CREATE TABLE IF NOT EXISTS prisonners (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
    prenom VARCHAR(100),
    nom VARCHAR(100),
    type_de_peine VARCHAR(100),
    collaborateur BOOLEAN,

    prison_id INT,
    FOREIGN KEY (prison_id) REFERENCES prison(id)
)
"""

# Table des peines
create_table_peine = """
CREATE TABLE IF NOT EXISTS peine (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INT,
    type_de_peine VARCHAR(100),
    collaborateur BOOLEAN,
    entry_date DATE,
    out_door DATE,
    FOREIGN KEY (user_id) REFERENCES prisonners(id)
)
"""

# Table du personnel
create_table_personnel = """
CREATE TABLE IF NOT EXISTS personnel (
    id INTEGER PRIMARY KEY NOT NULL,
    prenom VARCHAR(100),
    nom VARCHAR(100),
    status VARCHAR(100)
)
"""

# Exécution des requêtes de création de tables
cursor.execute(create_table_prisonners)
cursor.execute(create_table_peine)
cursor.execute(create_table_personnel)



# Insertion de données fictives dans la table 'prison'
prisons_data = [
    ('Akhtuba', 'Tambov', 120, 150, 'Fédérale'),
    ('Belomorstroy', 'Tomsk', 90, 120, 'Régionale'),
    ('Bezymyansky ', 'Vladimir', 80, 100, 'Locale'),
    ('Chapayevsky', 'Volgograd', 110, 130, 'Fédérale'),
    ('Ilimsky', ' Iaroslavl', 95, 110, 'Régionale'),
    ('Kirovlag ', 'Kalouga', 75, 90, 'Locale'),
    ('Kosvinsky ', 'Kalouga', 130, 160, 'Fédérale'),
    ('Maykainskoe ', 'Volgograd', 85, 100, 'Régionale'),
    ('Primorsky', 'Volgograd', 100, 120, 'Locale'),
    ('Privolzhsky', 'Tomsk', 105, 140, 'Fédérale')
]

insert_query_prison = """
INSERT INTO prison (name_prison, oblast, number_of_prisonners, capacityPrison, prison_Type)
VALUES (?, ?, ?, ?, ?)
"""
cursor.executemany(insert_query_prison, prisons_data)

# Insertion de données fictives dans la table 'prisonners'
prisonners_data = [
    ('Bagrov', 'Joutov', 'Peine légère', False, 1),
    ('Bachikrov', 'Delov', 'Peine sévère', True, 2),
    ('Yritov', 'Maienov', 'Peine modérée', False, 3),
    ('Dani', 'Iritiv', 'Peine sévère', True, 4),
    ('Ruskov', 'Kalounov', 'Peine légère', False, 5),
    ('Andrrey', 'Supol', 'Peine modérée', True, 6),
    ('Aleksandr', 'Andretcha', 'Peine sévère', False, 7),
    ('Boris', 'Kimosov', 'Peine modérée', True, 8),
    ('Irinia', 'Bajov', 'Peine légère', False, 9),
    ('Celenia', 'Veidenev', 'Peine sévère', True, 10)
]

insert_query_prisonners = """
INSERT INTO prisonners (prenom, nom, type_de_peine, collaborateur, prison_id)
VALUES (?, ?, ?, ?, ?)
"""
cursor.executemany(insert_query_prisonners, prisonners_data)

# Insertion de données fictives dans la table 'peine'
peine_data = [
    (1, 'Travaux d\'intérêt général', True, '2023-11-01', '2023-11-10'),
    (2, 'Emprisonnement à vie', False, '2023-11-05', '2023-12-01'),
    (3, 'Travaux forcés', True, '2023-11-10', '2023-11-20'),
    (4, 'Peine de prison', False, '2023-11-15', '2023-11-25'),
    (5, 'Travaux d\'intérêt général', True, '2023-11-20', '2023-12-05'),
    (6, 'Peine de prison', False, '2023-11-25', '2023-12-10'),
    (7, 'Travaux forcés', True, '2023-11-30', '2023-12-15'),
    (8, 'Emprisonnement à vie', False, '2023-12-05', '2023-12-20'),
    (9, 'Peine de prison', True, '2023-12-10', '2023-12-25'),
    (10, 'Travaux forcés', False, '2023-12-15', '2023-12-30')
]

insert_query_peine = """
INSERT INTO peine (user_id, type_de_peine, collaborateur, entry_date, out_door)
VALUES (?, ?, ?, ?, ?)
"""
cursor.executemany(insert_query_peine, peine_data)

# Insertion de données fictives dans la table 'personnel'
personnel_data = [
    ('Alevtina', 'Aksionov', 'Garde'),
    ('Aniussia', 'Aliev', 'Administrateur'),
    ('Milena', 'Ameline', 'Agent de sécurité'),
    ('Tanya', 'Bok', 'Infirmier'),
    ('Соня', 'Boitsov', 'Psychologue'),
    ('Yana', 'Wilson', 'Agent de libération conditionnelle'),
    ('Пётр', 'Bonine', 'Chef de prison'),
    ('Ivan', 'Vesseloki', 'Agent administratif'),
    ('Annochka', 'Voltchov', 'Agent de probation'),
    ('Annochka', 'Kaninov', 'Instructeur')
]

insert_query_personnel = """
INSERT INTO personnel (prenom, nom, status)
VALUES (?, ?, ?)
"""
cursor.executemany(insert_query_personnel, personnel_data)

conn.commit()
conn.close()
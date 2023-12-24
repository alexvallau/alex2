
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 11:39:04 2023

@author: user
"""
import sqlite3

import classes as func



def connect_database(database_path):
    return sqlite3.connect(database_path)


def ajoute_prisonnier(prenom, nom, type_de_peine, collaborateur, prison_id):
    # Créer une nouvelle connexion à la base de données
    conn =connect_database('carcerale.db')

    try:
        cursor = conn.cursor()

        # Insérer le prisonnier dans la table prisonners
        cursor.execute("""
            INSERT INTO prisonners (prenom, nom, type_de_peine, collaborateur, prison_id)
            VALUES (?, ?, ?, ?, ?)
        """, (prenom, nom, type_de_peine, collaborateur, prison_id))

        # Mettre à jour le nombre de prisonniers dans la table prison
        cursor.execute("""
            UPDATE prison
            SET number_of_prisonners = number_of_prisonners + 1
            WHERE id = ?
        """, (prison_id,))
        
        # Valider la transaction
        conn.commit()

    finally:
        # Fermer la connexion dans tous les cas (même en cas d'exception)
        conn.close()


# Fonction pour lister tous les prisonniers
def lister_prisonniers():
    #conn =connect_database('carcerale.db')
    #cursor = conn.cursor()
    #test=cursor.execute("SELECT * FROM prisonners")
    #print(test.fetchall())
    prisonniers= func.Prisonnier.getAllPrisonners()
    #print(prisonniers[0][1])
    

    
    
    #html = python
    return prisonniers


def getAllPrisonners():
    conn = connect_database('goodDB.db')
    cursor = conn.cursor()

    # Modifiez la requête pour inclure le nom de la prison en utilisant une jointure
    query = """
    SELECT prisonners.id, prisonners.prenom, prisonners.nom, prisonners.type_de_peine,
           prisonners.collaborateur, prison.name_prison
    FROM prisonners
    JOIN prison ON prisonners.prison_id = prison.id
    """

    prisonners = cursor.execute(query).fetchall()
    
    conn.close()  # N'oubliez pas de fermer la connexion après utilisation
    return prisonners

#test=lister_prisonniers()
#print(test)

def getIdFromPrisonName(prison_name):
   conn=connect_database('goodDB.db')
   cursor = conn.cursor()
   query = "SELECT id FROM prison WHERE name_prison = ?"
   cursor.execute(query, (prison_name,))
   result = cursor.fetchone()
   con.close
   return result



def getPrisonnersFilteredByPrison(prisonName):
        
        
    prisonId=getIdFromPrisonName(prisonName)
    print(prisonId[0])
    conn=connect_database('goodDB.db')
    cursor = conn.cursor()
    query = "SELECT * from prisonners WHERE prison_id = ?"
        
    cursor.execute(query, (prisonId))
    result = cursor.fetchall()
        
    conn.close()
        
    return result


# Fonction pour lister tous les goulags
def lister_goulags():
    conn =connect_database('goodDB.db')
    #cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute("SELECT name_prison, oblast FROM prison")
    return cursor.fetchall()
#test=lister_goulags()
#print(test[1])

# Fonction pour lister les prisonniers qui ont une certaine date
def lister_prisonniers_par_date(conn, entry_date, end_date):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT prisonners.nom, prisonners.prenom
        FROM prisonners
        INNER JOIN peine ON prisonners.id = peine.user_id
        WHERE peine.entry_date >= ? AND peine.entry_date <= ?
    """, (entry_date, end_date))
    return cursor.fetchall()

# Fonction pour changer un prisonnier de goulag
def deplacer_prisonnier(conn, prisoner_id, new_prison_id):
    cursor = conn.cursor()
    cursor.execute("UPDATE prisonners SET prison_id = ? WHERE id = ?", (new_prison_id, prisoner_id))
    conn.commit()

# Fonction pour lister tout le personnel
def lister_personnel(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT prenom, nom FROM personnel")
    return cursor.fetchall()


#Fonction qui aura pour but de récupérer un prisonnier selon son id
def getPrisonner(id):
    conn=connect_database('goodDB.db')
    cursor = conn.cursor()
    query = "SELECT * FROM prisonners WHERE id = ?"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    conn.close
    return result

#getpris= getPrisonner(9)
#prisonnier=func.Prisonnier(getpris[1], getpris[2], "test", getpris[3], getpris[4], getpris[5], getpris[7])
#print(prisonnier.image)

# Fonction pour lister les prisonniers selon la prison
def lister_prisonniers_par_goulag(conn, prison_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT prisonners.nom, prisonners.prenom
        FROM prisonners
        WHERE prisonners.prison_id = ?
    """, (prison_id,))
    return cursor.fetchall()

# Fonction pour lister tous les morts
def lister_morts(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT prisonners.nom, prisonners.prenom
        FROM prisonners
        INNER JOIN peine ON prisonners.id = peine.user_id
        WHERE peine.out_door IS NOT NULL
    """)
    return cursor.fetchall()

# Fonction pour lister les prisonniers libérés
def lister_liberes(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT prisonners.nom, prisonners.prenom
        FROM prisonners
        INNER JOIN peine ON prisonners.id = peine.user_id
        WHERE peine.out_door IS NOT NULL
    """)
    return cursor.fetchall()





hi=func.Prisonnier.filterPrisonnersCrossedFilter("default", "default", "default", "default", "2023-11-01", "default", "default")
print(hi)

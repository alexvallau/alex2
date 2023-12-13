# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:48:03 2023

@author: user
"""
import sqlite3

def connect_database(database_path):
    return sqlite3.connect(database_path)





class Prison:
     def __init__(self, name_prison, oblast, number_of_prisoners, capacity_prison, prison_type):
        self.name_prison = name_prison
        self.oblast = oblast
        self.number_of_prisoners = number_of_prisoners
        self.capacity_prison = capacity_prison
        self.prison_type = prison_type



class Personne:
    def __init__(self, Prenom , Nom):
        self.Prenom = Prenom
        self.Nom = Nom
        

class Employe(Personne):
    def __init__(self, Prenom, Nom, status):
        super().__init__(Nom, Prenom)
        self.status= status
        


class Prisonnier(Personne):
    def __init__(self, Prenom, Nom, type_de_peine, collaborateur, prison_id):
        super().__init__(Nom, Prenom)
        self.type_de_peine = type_de_peine
        self.collaborateur = collaborateur
        self.prison_id = prison_id
        
        
        
    def ajoute_prisonnier(self,prenom, nom, type_de_peine, collaborateur, prison_id):
        # Créer une nouvelle connexion à la base de données
        
    
        try:
            conn =connect_database('goodDB.db')
            cursor = conn.cursor()
    
            # Insérer le prisonnier dans la table prisonners
            cursor.execute("""
                INSERT INTO prisonners (prenom, nom, type_de_peine, collaborateur, prison_id)
                VALUES (?, ?, ?, ?, ?)
            """, (self.Prenom, self.nom, self.type_de_peine, self.collaborateur, self.prison_id))
    
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



class Peine:
    def __init__(self, id, user_id, type_de_peine, collaborateur, entry_date, out_door):
        self.id = id
        self.user_id = user_id
        self.type_de_peine = type_de_peine
        self.collaborateur = collaborateur
        self.entry_date = entry_date
        self.out_door = out_door



# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:48:03 2023

@author: user
"""
import sqlite3

from datetime import datetime

def connect_database(database_path):
    return sqlite3.connect(database_path)


###############################################################

class Administrateur:

    def __init__(self, account, password,managedPrisonId,isSuperUser ):

        self.account=account
        self.password=password
        self.managedPrisonId=managedPrisonId
        self.isSuperUser=isSuperUser
    def IsValidUser(username, password):
        conn = sqlite3.connect('goodDB.db')
        cursor = conn.cursor()
        # Utilisez des paramètres de requête pour éviter les injections SQL
        query = "SELECT * FROM administrateurs WHERE account = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()  # Récupérer le premier résultat de la requête
        conn.close()
        # Si l'utilisateur est trouvé, la variable 'user' ne sera pas None
        if(user):
            return user
        else:
            return False
    
    def IsUserSuperAdmin(username):
        conn = sqlite3.connect('goodDB.db')
        cursor = conn.cursor()
        query= "SELECT isSuperUser FROM administrateurs WHERE account = ?"
        cursor.execute(query, (username,))
        isUserAdmin=cursor.fetchone()
        conn.close()
        return isUserAdmin


###############################################################
class Prison:
     
    def __init__(self, name_prison, oblast, number_of_prisoners, capacity_prison, prison_type, long, latt):
        self.name_prison = name_prison
        self.oblast = oblast
        self.number_of_prisoners = number_of_prisoners
        self.capacity_prison = capacity_prison
        self.prison_type = prison_type
        self.longitude = long
        self.latt = latt
    
    def getAllPrisons():
        conn =connect_database('goodDB.db')
        cursor = conn.cursor()
        prisons=cursor.execute("SELECT * FROM prison").fetchall()
        return prisons
    
    def getIdFromPrisonName(prison_name):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT id FROM prison WHERE name_prison = ?"
        cursor.execute(query, (prison_name,))
        result = cursor.fetchone()
        return result

    def getPrisonIdFromAdminId(admin_id):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT managedPrisonId FROM administrateurs WHERE id = ?"
        cursor.execute(query, (admin_id,))
        result = cursor.fetchone()
        return result
    
    def getPrisonInfoFromId(prison_id):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT * FROM prison WHERE id = ?"
        cursor.execute(query, (prison_id,))
        result = cursor.fetchone()
        return result
    
    
    

###############################################################

class Personne:
    def __init__(self, Prenom, Nom, birthday):
        self.Prenom = Prenom
        self.Nom = Nom
        self.birthday = birthday

class Employe(Personne):
    def __init__(self, Prenom, Nom, birthday, status):
        super().__init__(Prenom, Nom, birthday)
        self.status = status

class Prisonnier(Personne):
    def __init__(self, Prenom, Nom, birthday, type_de_peine, collaborateur, prison_id, image, isAlive):
        super().__init__(Prenom, Nom, birthday)
        self.type_de_peine = type_de_peine
        self.collaborateur = collaborateur
        self.prison_id = prison_id
        self.image=image
        self.isAlive=isAlive

    def getPrisonner(id):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT * FROM prisonners WHERE id = ?"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        prisonnier=Prisonnier(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])
        conn.close()
        return prisonnier

    def updatePrisonner(id_prisonnier, nom, prenom, date_naissance):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "UPDATE prisonners SET nom =?, prenom =?, birthday =? WHERE id = ?"
        cursor.execute(query, (nom, prenom, date_naissance, id_prisonnier))
        conn.commit()
        conn.close()
    
    def getAllPrisonners():
        conn = connect_database('goodDB.db')
        cursor = conn.cursor()
        
        query = """
        SELECT prisonners.id, prisonners.prenom, prisonners.nom, prisonners.type_de_peine,
               prisonners.collaborateur, prison.name_prison, peine.entry_date, peine.out_door, prisonners.isAlive
        FROM prisonners
        JOIN prison ON prisonners.prison_id = prison.id
		JOIN peine ON prisonners.id = peine.user_id
        """
        prisonners = cursor.execute(query).fetchall()
        conn.close()  
        return prisonners
    
    def filterPrisonnersCrossedFilter(prenom, type_de_peine, collaborateur, prison_name, entry_date, out_door, isAlive):
           #on récupère ici tous les prisonniers
           prisonnersRawData=Prisonnier.getAllPrisonners()
           #filtered Prisonner
           filteredPrisonners=[]
           #default filter
           defaultFilters={'prenom':"default", 'type_de_peine':"default", 'collaborateur':"default", 'prison_name':"default", 'entry_date':"default", 'date':"default", 'isAlive':"default"}
           userFilter={'prenom':prenom, 'type_de_peine':type_de_peine, 'collaborateur':collaborateur, 'prison_name':prison_name, 'entry_date':entry_date, 'out_door':out_door, 'isAlive':isAlive}
           #On créé un dictionnaire avec les filtres qui ne sont pas par défaut
           appliedFilters = {key: value for key, value in userFilter.items() if value != defaultFilters.get(key, "default")}
           print(len(appliedFilters))
           hadAllFiltersBeenVisited=0
           for prisonner in prisonnersRawData:
               hadAllFiltersBeenVisited=0
               for key, value in appliedFilters.items():
                   if(hadAllFiltersBeenVisited==len(appliedFilters)):
                            print("Tous les filtres ont été visités")
                            filteredPrisonners.append(prisonner)
                   if key == "prenom":
                       if str(prisonner[1]) == str(value):
                           #Si le prénom de mon prisonnier vaut la valeur, alors je continue de boucler dans mes filtres
                           #print(prisonner[1] )
                           hadAllFiltersBeenVisited=hadAllFiltersBeenVisited+1
                           if(hadAllFiltersBeenVisited==len(appliedFilters)):
                            print("Tous les filtres ont été visités")
                            filteredPrisonners.append(prisonner)
                           continue
                       else:
                           #Sinon, je break mon filtre
                           break
                   if key == "type_de_peine":
                       if prisonner[3]== value:
                           #Si le prénom de mon prisonnier vaut la valeur, alors je continue de boucler dans mes filtres
                           print("Je suis dans type de peine")
                           hadAllFiltersBeenVisited=hadAllFiltersBeenVisited+1
                           if(hadAllFiltersBeenVisited==len(appliedFilters)):
                            print("Tous les filtres ont été visités")
                            filteredPrisonners.append(prisonner)
                           continue
                       else:
                           #Sinon, je break mon filtre
                           break

                   if key == "collaborateur":
                       if str(prisonner[4])== value:
                           hadAllFiltersBeenVisited=hadAllFiltersBeenVisited+1
                           if(hadAllFiltersBeenVisited==len(appliedFilters)):
                            print("Tous les filtres ont été visités")
                            filteredPrisonners.append(prisonner)
                           continue
                       else:
                           break
                   if key == "prison_name":
                       if prisonner[5]== value:
                           hadAllFiltersBeenVisited=hadAllFiltersBeenVisited+1
                           #Si la prison est la prison filtrée
                           if(hadAllFiltersBeenVisited==len(appliedFilters)):
                            print("Tous les filtres ont été visités")
                            filteredPrisonners.append(prisonner)
                           continue
                       else:
                           #Sinon, je break mon filtre
                           break
                   if key == "entry_date":
                       if str(prisonner[6]) == value:
                           hadAllFiltersBeenVisited=hadAllFiltersBeenVisited+1
                           #Si la prison est la prison filtrée
                           if(hadAllFiltersBeenVisited==len(appliedFilters)):
                            print("Tous les filtres ont été visités")
                            filteredPrisonners.append(prisonner)
                           continue
                       else:
                           #Sinon, je break mon filtre
                           break
                   if key == "out_date":
                       if str(prisonner[7]) == value:
                           hadAllFiltersBeenVisited=hadAllFiltersBeenVisited+1
                           #Si la prison est la prison filtrée
                           if(hadAllFiltersBeenVisited==len(appliedFilters)):
                            print("Tous les filtres ont été visités")
                            filteredPrisonners.append(prisonner)
                           continue
                       else:
                           #Sinon, je break mon filtre
                           break
                   print("Je print la key")
                   if key == "isAlive":
                       print("Je suis dans is Alive et prisonner8 vaut"+str(prisonner[8])+"Value vaut"+str(value))
                       if str(prisonner[8])== value:
                           hadAllFiltersBeenVisited=hadAllFiltersBeenVisited+1
                           if(hadAllFiltersBeenVisited==len(appliedFilters)):
                            print("Tous les filtres ont été visités")
                            filteredPrisonners.append(prisonner)
                           print("Je suis dans is Alive")
                           #Si la prison est la prison filtrée
                       else:
                           #Sinon, je break mon filtre
                           break
                       #Et je continue dans mes prisonniers
                   else:
                       return f"No fucking key {key}"
    #Je continue dans mes prisonniers
               continue
           
           return filteredPrisonners  
        
    
    ##Renvoi les prisonniers qui correspondent à une certaine prison
    def getPrisonnersFilteredByPrison(prisonName):
        prisonId=Prison.getIdFromPrisonName(prisonName)
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT * from prisonners WHERE prison_id = ?"
        cursor.execute(query,(prisonId))
        result = cursor.fetchall()
        conn.close()
        return result
        
    def getLastPrisonnerId():
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT id FROM prisonners ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        return result[0]
        
    def ajoute_prisonnier(self):
        try:
            conn =connect_database('goodDB.db')
            cursor = conn.cursor()
            # Insérer le prisonnier dans la table prisonners
            cursor.execute("""
                INSERT INTO prisonners (prenom, nom, birthday ,type_de_peine, collaborateur, prison_id, image, isAlive)
                VALUES (?, ?, ?, ?, ?, ?, ?,?)
            """, (self.Prenom, self.Nom,  self.birthday ,self.type_de_peine,self.collaborateur,self.prison_id, self.image, self.isAlive))
            cursor.execute("UPDATE prison SET number_of_prisonners = number_of_prisonners + 1 WHERE id = ?", (self.prison_id,))
            conn.commit()
        finally:
            # Fermer la connexion dans tous les cas (même en cas d'exception)
            conn.close()



    def getPrisonIdFromPrisonner(prisonner_id):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT prison_id FROM prisonners WHERE id = ?"
        cursor.execute(query,(prisonner_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0]




    def killPrisonner(prisonner_id, date, reason):
        conn =connect_database('goodDB.db')
        cursor = conn.cursor()

        #décrémente de 1 le nombre de prisonniers dans la prison
        prison_id=Prisonnier.getPrisonIdFromPrisonner(prisonner_id)
        cursor.execute("UPDATE prison SET number_of_prisonners = number_of_prisonners - 1 WHERE id = ?", (prison_id,))

        
        query1="UPDATE prisonners SET isAlive = 0 WHERE id = ?"
        query2="INSERT INTO morts (id_prisonner, death_date, REASON) VALUES (?,?,?)"
        cursor.execute(query1, (prisonner_id,))
        cursor.execute(query2, (prisonner_id, date, reason))
        conn.commit()
        conn.close()

    def prisonnerChangePrison(prisonner_id, new_prison_id, current_prison_id):

        conn =connect_database('goodDB.db')
        cursor = conn.cursor()
        
        #change l'id de la prison
        cursor.execute("UPDATE prisonners SET prison_id = ? WHERE id = ?", (new_prison_id, prisonner_id))

        #décrménete la prison dans laquelle
        #  il se trouve actuellement
        cursor.execute("UPDATE prison SET number_of_prisonners = number_of_prisonners - 1 WHERE id = ?", (current_prison_id,))

        # Decrement the number of prisonners in the new prison
        cursor.execute("UPDATE prison SET number_of_prisonners = number_of_prisonners + 1 WHERE id = ?", (new_prison_id,))


    # Commit the changes and close the connection
        conn.commit()
        conn.close()
        
   

        
###############################################################

class Peine:
    def __init__(self, user_id, type_de_peine,  entry_date, out_door):
     
        self.user_id = user_id
        self.type_de_peine = type_de_peine
        self.entry_date = entry_date
        self.out_door = out_door


    def addPeine(self):
        conn =connect_database('goodDB.db')
        cursor = conn.cursor()
        # Insérer la peine dans la table peine
        cursor.execute("""
            INSERT INTO peine (user_id, type_de_peine, entry_date, out_door)
            VALUES (?, ?, ?, ?)
        """, (self.user_id, self.type_de_peine, self.entry_date, self.out_door))
        conn.commit()
        conn.close()

    def getPeineFromUserID(prisonnerId):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT * from peine WHERE user_id = ?"
        cursor.execute(query,(prisonnerId,))
        result = cursor.fetchone()
        peine=Peine(result[1], result[2], result[4], result[5])
        conn.close()
        return peine





###############################################################
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



from colorama import Fore, Back, Style
#import overpy
import classes as func
import fonctions as stp
import random
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
#UPLOAD_FOLDER = "C:/Users/aarizzi.JEANLAIN/alex2/static/uploads"
UPLOAD_FOLDER="C:/Users/arizz/Documents/Master/alex2/static/uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def connect_database(database_path):
    return sqlite3.connect(database_path)

@app.route("/")
def default():
    return redirect("index")

@app.route("/hi")
def greeting():
    return "Hello world"

@app.route("/hello")
def hello():
    return render_template("test.html")

    
    #return render_template("connected.html")
@app.route("/connexion", methods=['GET', 'POST'])
def connexion():
    if request.method == "POST":
        username = request.form["pseudo"]
        password = request.form["pass"]
        if(len(username)<1 or len(password)<1):
            return render_template("login.html", invalidUser=True)
        #print("test"+str(func.Administrateur.IsValidUser(username, password)[3]) )
        else:
                isUservalid=func.Administrateur.IsValidUser(username, password)
                if(isUservalid):
                    isUserSuperAdmin=str(func.Administrateur.IsUserSuperAdmin(username))
                    
                    resp =  make_response(redirect(url_for("index"), 200))
                    resp.set_cookie('username', username)
                    resp.set_cookie('IsSuperUserAd', str(isUserSuperAdmin[1]))
                    resp.set_cookie('managedPrisonId', str(isUservalid[3]))
                    return resp  # Return the response here
                else:
                    return render_template("login.html", invalidUser=True)

    return render_template("login.html")

@app.route("/deconnexion")
def deconnexion():
        resp = make_response(redirect(url_for("connexion"), 200))
        resp.delete_cookie('username')
        resp.delete_cookie('IsSuperUserAd')
        resp.delete_cookie('managedPrisonId')
        return resp
   

@app.route("/index")
def index():

    prisons=func.Prison.getAllPrisons()

    return render_template("index.html", prisons = prisons)


@app.route('/get_prison_info/<int:prison_id>')
def get_prison_info(prison_id):
    prison_info = func.Prison.getPrisonInfoFromId(prison_id)
    #print(jsonify(prison_info))  
    return jsonify(prison_info)



#page qui montre toutes les prisons
@app.route("/Touteslesprisons")
def Touteslesprisons():
    prisons=func.Prison.getAllPrisons()
    return render_template("Touteslesprisons.html",prisons=prisons)

#page d'information sur prisonnier
@app.route("/ConsultPrisonner", methods=['GET','POST'])
def ConsultPrisonner():
    if request.method=="GET":
        id_prisonnier=request.args.get('id', default="", type=str)
        prisonner=func.Prisonnier.getPrisonner(id_prisonnier)
        peine=func.Peine.getPeineFromUserID(id_prisonnier)
        prisons=func.Prison.getAllPrisons()
        
        return render_template("prisonnerInformation.html", id_prisonnier=id_prisonnier,prisonner=prisonner, peine=peine, prisons=prisons )


@app.route("/changePrisonnerInformation", methods=["POST", "GET"])
def changePrisonnerInformation():
    if request.method=="GET":
        id_prisonnier=request.args.get('id', default="", type=str)
        prisonner=func.Prisonnier.getPrisonner(id_prisonnier)
        peine=func.Peine.getPeineFromUserID(id_prisonnier)
        prisons=func.Prison.getAllPrisons()
        
        return render_template("changePrisonnerInformations.html", id_prisonnier=id_prisonnier,prisonner=prisonner, peine=peine, prisons=prisons )

    return render_template("prisonnerInformation.html")


@app.route("/changePrisonnerInformation/changeIt", methods=["POST"])
def changeIt():
    if request.method=="POST":
        id_prisonnier=request.form['prisonner_id']
        nom=request.form['nom']
        prenom=request.form['prenom']
        date_naissance=request.form['birthday']
        
        print("id prisonner "+id_prisonnier+" nom "+nom+" prenom "+prenom+" date_naissance "+date_naissance)
        func.Prisonnier.updatePrisonner(id_prisonnier, nom, prenom, date_naissance)
        #func.Prisonnier.changePrisonnerInformation(id_prisonnier, nom, prenom, date_naissance, lieu_naissance, num_secu, id_prison)
        return redirect(url_for('Touslesprisonniers'))

@app.route("/killPrisonner", methods=["POST"])
def killPrisonner():
    if request.method == "POST":
        
        id_prisonnier = request.form['prisonner_id']
        death_date = request.form['death_date']
        death_reason = request.form['reason']
        print("id prisonner "+id_prisonnier+" death_date "+death_date+" death_reason "+death_reason)
        func.Prisonnier.killPrisonner(id_prisonnier,death_date, death_reason )
        return redirect(url_for('Touslesprisonniers'))


@app.route("/prisonnerChangePrison", methods=["POST"])
def prisonnerChangePrison():
    if request.method=="POST":
        new_id_prison=request.form['prison']
        prisonner_id=request.form['prisonner_id']
        current_prison_id=request.form['current_prison']
        func.Prisonnier.prisonnerChangePrison(prisonner_id, new_id_prison, current_prison_id )
        return redirect(url_for('Touslesprisonniers'))


@app.route("/Touslesprisonniers", methods=['GET', 'POST'])
def Touslesprisonniers():
    #Pour le résultat du filtre
    if request.method=="GET":
        prenom=request.args.get('prenom', default="default",type=str )
        prisons=func.Prison.getAllPrisons()
        nom_ville=request.args.get('prisonFilter', default="default", type=str)
        entry_date=request.args.get('entryDateFilter', default="default", type=str)
        out_date=request.args.get('outDoorDateFilter', default="default", type=str)
        isAlive=request.args.get('isAlive', default="default", type=str)
        type_de_peine=request.args.get('type_de_peine', default="default", type=str)
        collaborateur=request.args.get('collaborateur', default="default", type=str)
        
        if(str(entry_date)=="0001-01-01"):
            entry_date="default"
        if(str(out_date)=="0001-01-01"):
            out_date="default"

        if str(prenom)=="":
            prenom="default"
        

        test=func.Prisonnier.filterPrisonnersCrossedFilter(prenom, type_de_peine, collaborateur, nom_ville, entry_date, out_date, isAlive)
        print(test)
        #print("LA mzfEMOIFNEVÔMNEVÔZmvnzoVJNZOMnomlneomnmzeùpovzcnEDAte EST"+entry_date)
        #return nom_ville
        if(prenom != "default" or nom_ville != "default" or entry_date != "default" or out_date != "default" or isAlive != "default" or type_de_peine!= "default" or collaborateur != "default"):
         #   return nom_ville
            #filteredPrisonners=func.Prisonnier.getPrisonnersFilteredByPrison(nom_ville)
            #print(vars(filteredPrisonners))
            return render_template("Touslesprisonniers.html", prisonniers=test, prisons=prisons)
        else:
            prisonniers=func.Prisonnier.getAllPrisonners()
            #print(prisonniers)
            return render_template("Touslesprisonniers.html", prisonniers=prisonniers, prisons=prisons)
            #return jsonify(prisonniers)


#ajouter un prisonnier depuis un formulaire:
@app.route("/ajoutPrisonnier", methods=['GET', 'POST'])
def ajoutPrisonnier():
    prisons=func.Prison.getAllPrisons()
    if request.method == "POST":
        prenom = request.form['prenom']
        nom = request.form['nom']
        birthday=request.form['birthday']
        entrydate=request.form['entrydate']
        exitdate=request.form['exitdate']
        type_de_peine = request.form['type_de_peine']
        collaborateur = bool(request.form.get('collaborateur', False))
        prison_id = request.form['prison_id']
        isAlive=True
        ##On ajoute l'image
        print(collaborateur)
        nombre=random.randint(0,46354354113)
            # Obtient le fichier téléchargé depuis la requête
        uploaded_img = request.files['file']
    #test
            # Vérifie si le nom du fichier est valide (évite les injections)
        if uploaded_img.filename != '':
                # Déplace le fichier téléchargé dans le dossier UPLOAD_FOLDER
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{nombre}.jpg")
            uploaded_img.save(img_filename)
        prisonnier = func.Prisonnier(prenom, nom, birthday, type_de_peine, collaborateur, prison_id, nombre, isAlive)
        prisonnier.ajoute_prisonnier()
        lastPrisonnerId=func.Prisonnier.getLastPrisonnerId()
        peine=func.Peine(lastPrisonnerId,type_de_peine,entrydate, exitdate)
        peine.addPeine()
        #func.ajoute_prisonnier( prenom, nom, type_de_peine, collaborateur, prison_id)

    return render_template("AjoutPrisonnier.html", prisons = prisons)


app.run(debug=True)
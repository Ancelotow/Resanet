#!/usr/bin/python
# -*- coding: utf-8 -*-


import mysql.connector



connexionBD = None

def getConnexionBD() :
	global connexionBD
	try :
		if connexionBD == None :
			connexionBD = mysql.connector.connect(
					host = 'localhost' ,
					user = 'root' ,
					password = 'azerty' ,
					database = 'resanet'
				)
		return connexionBD
	except :
		return None


def seConnecterGestionnaire( login , mdp ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select nom,prenom
					from Gestionnaire
					inner join Personnel 
					on Gestionnaire.matricule = Personnel.matricule
					where login = %s
					and mdp = %s
				'''

		curseur.execute( requete , ( login , mdp ) )
		
		enregistrement = curseur.fetchone()
		
		gestionnaire = {}
		if enregistrement != None :
			gestionnaire[ 'login' ] = login
			gestionnaire[ 'nom' ] = enregistrement[ 0 ]
			gestionnaire[ 'prenom' ] = enregistrement[ 1 ]
			
		curseur.close()
		return gestionnaire
		
	except :
		return None
		
def seConnecterUsager( numeroCarte , mdpCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select solde,activee,nom,prenom 
					from Carte
					inner join Personnel 
					on Carte.matricule = Personnel.matricule
					where numeroCarte = %s
					and mdpCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , mdpCarte ) )
		
		enregistrement = curseur.fetchone()
		
		usager = {}
		if enregistrement != None :
			usager[ 'numeroCarte' ] = numeroCarte
			usager[ 'solde' ] = enregistrement[ 0 ]
			usager[ 'activee' ] = enregistrement[ 1 ]
			#print type( usager[ 'activee' ] )
			usager[ 'nom' ] = enregistrement[ 2 ]
			usager[ 'prenom' ] = enregistrement[ 3 ]
			
		curseur.close()
		return usager
		
	except :
		return None


def getSolde( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select solde
					from Carte
					where numeroCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , ) )
		
		enregistrement = curseur.fetchone()
		
		solde = 'inconnu'
		if enregistrement != None :
			solde = enregistrement[ 0 ]
			#print type(solde)
			
		curseur.close()
		return solde
		
	except :
		return None
		
		
def getTarifRepas( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select tarifRepas
					from Fonction
					inner join Personnel
					on Fonction.idFonction = Personnel.idFonction
					inner join Carte
					on Personnel.matricule = Carte.matricule
					where numeroCarte = %s
				'''

		curseur.execute( requete , ( numeroCarte , ) )
		
		enregistrement = curseur.fetchone()
		
		tarif = 'inconnu'
		if enregistrement != None :
			tarif = enregistrement[ 0 ]
			#print type(tarif)
			
		curseur.close()
		return tarif
		
	except :
		return None

def getPersonnelsSansCarte() :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select matricule, nom , prenom , nomService
					from Service
					inner join Personnel
					on Service.idService = Personnel.idService
					where matricule not in ( 
												select matricule
												from Carte
											)
				'''

		curseur.execute( requete , () )
		
		enregistrements = curseur.fetchall()
		
		personnels = []
		for unEnregistrement in enregistrements :
			unPersonnel = {}
			unPersonnel[ 'matricule' ] = unEnregistrement[ 0 ]
			unPersonnel[ 'nom' ] = unEnregistrement[ 1 ]
			unPersonnel[ 'prenom' ] = unEnregistrement[ 2 ]
			unPersonnel[ 'nomService' ] = unEnregistrement[ 3 ]
			personnels.append( unPersonnel )
			
		curseur.close()
		return personnels
		
	except :
		return None
		
def getPersonnelsAvecCarte() :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select Personnel.matricule, solde, activee, nom , prenom , nomService, numeroCarte
					from Service
					inner join Personnel
					on Service.idService = Personnel.idService
					inner join Carte
					on Carte.matricule = Personnel.matricule
				'''

		curseur.execute( requete , () )
		
		enregistrements = curseur.fetchall()
		
		personnels = []
		for unEnregistrement in enregistrements :
			unPersonnel = {}
			unPersonnel[ 'matricule' ] = unEnregistrement[ 0 ]
			unPersonnel[ 'solde' ] = unEnregistrement[ 1 ]
			unPersonnel[ 'activee' ] = unEnregistrement[ 2 ]
			unPersonnel[ 'nom' ] = unEnregistrement[ 3 ]
			unPersonnel[ 'prenom' ] = unEnregistrement[ 4 ]
			unPersonnel[ 'nomService' ] = unEnregistrement[ 5 ]
			unPersonnel[ 'numeroCarte' ] = unEnregistrement[ 6 ]
			personnels.append( unPersonnel )
			
		curseur.close()
		return personnels
		
	except :
		return None
		
def activerCarte( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set activee = 1
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
	
	except :
		return None
	
def bloquerCarte( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set activee = 0
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None
		

def crediterCarte( numeroCarte , somme ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set solde = solde + %s
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( somme , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None


def reinitialiserMdp( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set mdpCarte = (
				select year( dateNaissance )
				from Personnel
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None


def modifierMdpUsager( numeroCarte , nouveauMdp) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set mdpCarte = %s
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( nouveauMdp , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None
		
		
def getNaissance( numeroCarte ):
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			select year( dateNaissance )
			from Personnel
			where matricule = %s
			'''
			
		curseur.execute( requete , ( numeroCarte ) )
		sauve = curseur.fetchone()
		for row in sauve :
			ddn = row
		curseur.close()
		
		return ddn
		
	except :
		return None


def getMdp( numeroCarte ):
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			select mdpCarte
			from Carte
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte ) )
		sauve = curseur.fetchone()
		for row in sauve :
			mdp = row
		curseur.close()
		
		return mdp
		
	except :
		return None

def creerCarte( matricule , activee  ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			insert into Carte
			values(NULL,(select year(dateNaissance) from Personnel where matricule = %s ),0.0,CURRENT_DATE,%s,%s)
			'''
			
		curseur.execute( requete , ( matricule , activee , matricule ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None


def enregistrerReservation( numeroCarte , dateReservation ):
	try:
		curseur = getConnexionBD().cursor()

		requete = '''
			insert into Reservation( dateResa , numeroCarte )
			values( %s , %s )
			'''

		curseur.execute(requete, ( dateReservation , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()

		return nbTuplesTraites

	except:
		return None


def annulerReservation( numeroCarte , dateReservation ):
	try:
		curseur = getConnexionBD().cursor()

		requete = '''
			delete from Reservation
			where numeroCarte = %s
			and dateResa = %s
			'''

		curseur.execute(requete, ( numeroCarte , dateReservation ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()

		return nbTuplesTraites

	except:
		return None


def getReservationsCarte( numeroCarte , dateDebut , dateFin ):
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select dateResa
					from Reservation
					where numeroCarte = %s
					and dateResa >= %s
					and dateResa <= %s 
				'''

		curseur.execute(requete, ( numeroCarte , dateDebut , dateFin ) )

		enregistrements = curseur.fetchall()

		dates = []
		for unEnregistrement in enregistrements:
			
			uneDate = '%04d-%02d-%02d' % ( unEnregistrement[0].year , unEnregistrement[0].month , unEnregistrement[0].day )
			
			dates.append( uneDate )

		curseur.close()
		return dates

	except:
		return None


def getHistoriqueReservationsCarte( numeroCarte ) :
	try:
		curseur = getConnexionBD().cursor()
		requete = '''
					select dateResa
					from Reservation
					where numeroCarte = %s
					order by dateResa DESC
				'''

		curseur.execute(requete, ( numeroCarte , ) )

		enregistrements = curseur.fetchall()

		dates = []
		for unEnregistrement in enregistrements:
			
			uneDate = '%04d-%02d-%02d' % ( unEnregistrement[0].year , unEnregistrement[0].month , unEnregistrement[0].day )
			
			dates.append( uneDate )

		curseur.close()
		return dates

	except:
		return None

	
def getReservationsDate( dateResa ) :
	try :
		curseur = getConnexionBD().cursor()
		requete = '''
					select Carte.numeroCarte , Personnel.nom , Personnel.prenom , Service.nomService
					from Reservation
					inner join Carte
					on Carte.numeroCarte = Reservation.numeroCarte
					inner join Personnel
					on Personnel.matricule = Carte.matricule
					inner join Service
					on Service.idService = Personnel.idService
					where Reservation.dateResa = %s
				'''

		curseur.execute( requete , ( dateResa , ) )
		
		enregistrements = curseur.fetchall()
		
		reservations = []
		for unEnregistrement in enregistrements :
			uneReservation = {}
			uneReservation[ 'numeroCarte' ] = unEnregistrement[ 0 ]
			uneReservation[ 'nom' ] = unEnregistrement[ 1 ]
			uneReservation[ 'prenom' ] = unEnregistrement[ 2 ]
			uneReservation[ 'nomService' ] = unEnregistrement[ 3 ]
			reservations.append( uneReservation )
			
		curseur.close()
		return reservations
		
	except :
		return None


	
def debiterSolde( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set solde = solde - (
				select tarifRepas
				from Fonction
				inner join Personnel
				on Personnel.idFonction = Fonction.idFonction
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites

	except :
		return None
		
	
def crediterSolde( numeroCarte ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte as c
			set solde = solde + (
				select tarifRepas
				from Fonction
				inner join Personnel
				on Personnel.idFonction = Fonction.idFonction
				where c.matricule = Personnel.matricule
				and c.numeroCarte = %s
			)
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( numeroCarte , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites

	except :
		return None
		
		
def debiterCarte( numeroCarte , somme ) :
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			update Carte
			set solde = solde - %s
			where numeroCarte = %s
			'''
			
		curseur.execute( requete , ( somme , numeroCarte ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None

def supprimerCarte( numeroCarte ) :
	
	try :
		curseur = getConnexionBD().cursor()
		
		requete = '''
			delete from Carte
			where numeroCarte = %s 
			'''
			
		curseur.execute( requete , (  numeroCarte , ) )
		connexionBD.commit()
		nbTuplesTraites = curseur.rowcount
		curseur.close()
		
		return nbTuplesTraites
		
	except :
		return None
		
def estJoursFeries(date) :
	try :
		annee = date[0] + date[1] + date[2] + date[3]
		mois = date[6]
		jour = date[8] + date[9]
		curseur = getConnexionBD().cursor()
		requete = '''
						select jours, mois, annee
						from JoursFeries
						where jours = %s
						and mois = %s
						and annee = %s
				'''
		curseur.execute(requete , ( jour , mois , annee )) 
		enregistrement = curseur.fetchall()
		if len(enregistrement) == 0 :
		 return False
		else :
		 return True

		curseur.close()

	except :
		return None
		 
def getJoursFeries() :
	
		jours = []
		curseur = getConnexionBD().cursor()
		requete = '''
						select * 
						from JoursFeries
						order by mois 
						
				'''
		curseur.execute( requete )
		save = curseur.fetchall()
		for row in save :
			jours.append({ 'jours' : row[0] , 'mois' : row[1] , 'annee' : row[2] , 'libelle' : row[3] })
		return jours
		curseur.close()
	
		
def setJoursFeries(jour , mois, libelle) :

		curseur = getConnexionBD().cursor()
		requete = '''
					insert into JoursFeries values( %s , %s , YEAR(current_date()) , %s)
			'''
		curseur.execute( requete , ( jour , mois ,  libelle ))
		return True
		curseur.close()
		
def suppJoursFeries( jour , mois ) :
	
		curseur = getConnexionBD().cursor()
		requete = '''
					delete from JoursFeries
					where jours = %s
					and mois = %s
			'''
		curseur.execute( requete , ( jour , mois ))
		return True
		curseur.close()
		
def getService() :
		
		service = []
		curseur = getConnexionBD().cursor()
		requete = '''
						select *
						from Service
				'''
		curseur.execute( requete )
		save = curseur.fetchall()
		for row in save :
			service.append({ 'idService' : row[0] , 'nomService' : row[1] })
		curseur.close()
		return service
		
def getFonction() :
		
		fonction = []
		curseur = getConnexionBD().cursor()
		requete = '''
						select *
						from Fonction
				'''
		curseur.execute( requete )
		save = curseur.fetchall()
		for row in save :
			fonction.append({ 'idFonction' : row[0] , 'nomFonction' : row[1] })
		curseur.close()
		return fonction

def getMatricule() :
		
		matricule = []
		curseur = getConnexionBD().cursor()
		requete = '''
						select *
						from Personnel
				'''
		curseur.execute( requete )
		save = curseur.fetchall()
		for row in save :
			matricule.append(row[0])
		curseur.close()
		return matricule
		
def addPersonnel( matricule , nom , prenom , naissance , service , fonction ) :
	
		curseur = getConnexionBD().cursor()
		requete = '''
						insert into Personnel values( %s , %s , %s , %s , %s , %s )
				'''
		curseur.execute( requete , ( matricule , nom , prenom , naissance , fonction , service ) )
		return True
		curseur.close()
		
def delPersonnel( matricule ) :
	
		curseur = getConnexionBD().cursor()
		requete = '''
						delete from Personnel where matricule = %s
				'''
		curseur.execute( requete , ( matricule , ) )
		return True
		curseur.close()

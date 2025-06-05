import requests
from sqlalchemy import func,text
from geoalchemy2 import functions
from geoalchemy2.shape import from_shape
from shapely import wkb

from app import app  
from models import Erp,Stationnement,Troncon_cheminement,Travaux, db


with app.app_context():

    #requête permettant de récupérer les données présente dans les tables temporaires
    result = db.session.execute(text("SELECT equipement, type_equipement, (numero_rue||' '||nom_rue) as adresse, code_postal, accessible, geom FROM accessibilite.erp_tmp"))

    #pour chaque ligne du résultat de la requête SQL on crée un éléments de la classe d'entité correspondante
    for row in result:
        #adaptation de la géométrie au bon format pour pouvoir facilement créer notre geojson par la suite
        shapely_geom = wkb.loads(row[5])

        if shapely_geom:
            geo = f"SRID=2154;{shapely_geom.wkt}"

            erp = Erp(
                name=row[0],
                erptype=row[1],
                adresse=row[2],
                codepostal=row[3],
                accessible=row[4],
                location=geo
            )
            db.session.add(erp)
            #Amélioration : il serait plus propre que le commit soit en dehors de la boucle FOR mais nous avions des problèmes de conflits
            db.session.commit()
    
    #On répète ces opérations pour toute nos couches
    result = db.session.execute(text("SELECT largeur, longueur, absence_marq_sol, devers, hcp_tous, geom FROM accessibilite.pmr_tmp"))

    for row in result:
        shapely_geom = wkb.loads(row[5])

        if shapely_geom:
            geo = f"SRID=2154;{shapely_geom.wkt}"

            pmr = Stationnement(
                largeur=row[0],
                longueur=row[1],
                marquagesol=row[2],
                devers=row[3],
                accessible=row[4],
                location=geo
            )
            db.session.add(pmr)
            db.session.commit()

    result = db.session.execute(text("SELECT distance, accessible, geom FROM accessibilite.cheminement_tmp"))

    for row in result:
        shapely_geom = wkb.loads(row[2])

        if shapely_geom:
            geo = f"SRID=2154;{shapely_geom.wkt}"

            cheminement = Troncon_cheminement(
                distance=row[0],
                accessible=row[1],
                location=geo
            )
            db.session.add(cheminement)
            db.session.commit()

    result = db.session.execute(text("SELECT duree, numero,voie,commune,entreprise,datedebut,datefin,commentaire,circulation, geom FROM travaux.travaux_tmp"))

    for row in result:
        shapely_geom = wkb.loads(row[9])

        if shapely_geom:
            geo = f"SRID=2154;{shapely_geom.wkt}"

            chantier = Travaux(
                duree=row[0],
                numero=row[1],
                voie=row[2],
                commune=row[3],
                entreprise=row[4],
                datedebut=row[5],
                datefin=row[6],
                commentaire=row[7],
                circulation=row[8],
                location=geo
            )
            db.session.add(chantier)
            db.session.commit()


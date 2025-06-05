from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry,functions
from flask import Flask
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from sqlalchemy import Integer, String, Float,Date , Text
import json

#on utilise le modèle  SQLAlchemy pour la création de classe python représentant des tables de la base de données
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class Erp(db.Model):
    __tablename__ = 'erp'   #Définition du nom de la table
    __table_args__ = {'schema': 'accessibilite'}    #Schéma de la base dans lequel la table sera stockée

    #définition des différents attributs
    iderp = db.Column(db.BigInteger, primary_key=True)  
    name = db.Column(db.String(250))
    erptype = db.Column(db.String(250))
    adresse = db.Column(db.String(250))
    codepostal = db.Column(db.String(10))
    accessible=db.Column(db.String(250))
    location = db.Column(Geometry("POINT", srid=2154), nullable=False)

    #création de la fonction permettant de traduire les données de la base au format geojson
    def to_geojson(self):
        x = db.session.query(functions.ST_X(self.location)).scalar()
        y = db.session.query(functions.ST_Y(self.location)).scalar()
        
        return {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [x,y]},
            "properties": {
                "iderp": self.iderp,
                "name": self.name,
                "erptype": self.erptype,
                "adresse": self.adresse,
                "codepostal": self.codepostal,
                "accessible": self.accessible,
            },
        }

class Stationnement(db.Model):
    __tablename__ = 'stationnement'
    __table_args__ = {'schema': 'accessibilite'} 

    idstationnement = db.Column(db.BigInteger, primary_key=True) 
    largeur = db.Column(db.String(250))
    longueur = db.Column(db.String(250))
    marquagesol = db.Column(db.String(250))
    devers = db.Column(db.String(250))
    accessible=db.Column(db.String(250))
    location = db.Column(Geometry("POINT", srid=2154), nullable=False)

    def to_geojson(self):
        x = db.session.query(functions.ST_X(self.location)).scalar()
        y = db.session.query(functions.ST_Y(self.location)).scalar()
        
        return {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [x,y]},
            "properties": {
                "idstationnement":self.idstationnement,
                "largeur": self.largeur,
                "longueur": self.longueur,
                "marquagesol": self.marquagesol,
                "devers": self.devers,
                "accessible": self.accessible,
            },
        }

class Troncon_cheminement(db.Model):
    __tablename__ = 'troncon_cheminement'
    __table_args__ = {'schema': 'accessibilite'} 

    idtroncon = db.Column(db.BigInteger, primary_key=True)  
    distance = db.Column(db.Float)
    accessible = db.Column(db.String(250))
    location = db.Column(Geometry("LINESTRING", srid=2154), nullable=False)

    def to_geojson(self):
        geom = db.session.scalar(functions.ST_AsGeoJSON(self.location))
        geom_json = json.loads(geom)
        geom = {"type": geom_json["type"],"coordinates":geom_json["coordinates"]}

        return {
            "type": "Feature",
            "geometry": geom,
            "properties": {
                "distance": self.distance,
                "accessible": self.accessible
            },
        }

class Travaux(db.Model):
    __tablename__ = 'travaux'
    __table_args__ = {'schema': 'travaux'} 

    idtravaux = db.Column(db.BigInteger, primary_key=True)
    duree = db.Column(db.Integer)
    numero = db.Column(db.String(20))
    voie = db.Column(db.Text)
    commune = db.Column(db.String(250))
    entreprise = db.Column(db.String(250))
    datedebut = db.Column(db.Date)
    datefin = db.Column(db.Date)
    commentaire = db.Column(db.Text)
    circulation = db.Column(db.Text)
    location = db.Column(Geometry("POLYGON", srid=2154), nullable=False)

    def to_geojson(self):
        geom = db.session.scalar(functions.ST_AsGeoJSON(self.location))
        geom_json = json.loads(geom)
        geom = {"type": geom_json["type"],"coordinates":geom_json["coordinates"]}

        return {
            "type": "Feature",
            "geometry": geom,
            "properties": {
                "idtravaux": self.idtravaux,
                "duree": self.duree,
                "numero": self.numero,
                "voie": self.voie,
                "commune": self.commune,
                "entreprise": self.entreprise,
                "datedebut": self.datedebut.isoformat() if self.datedebut else None,
                "datefin": self.datefin.isoformat() if self.datefin else None,
                "commentaire": self.commentaire,
                "circulation": self.circulation
            },
        }
        
class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'identification'} 

    id_user = db.Column(db.BigInteger, primary_key=True) 
    identifiant = db.Column(db.Text)
    mdp = db.Column(db.Text)


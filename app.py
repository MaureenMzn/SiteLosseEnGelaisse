# Import préalable des différents extentions sur la machine virtuelle
from flask import Flask, render_template,jsonify,request, redirect, url_for
from sqlalchemy import text
from datetime import datetime

from models import db,Erp,Stationnement,Troncon_cheminement,Travaux,User
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)


# Configuration de la base PostgreSQL distante
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://georeader:winniepeg@localhost:15432/postgres"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Création de la base de données
with app.app_context():
    db.create_all()

#Définition des différentes pages du site et de leurs chemins
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/carto")
def carto():
    return render_template("carto.html")

@app.route("/lib")
def lib():
    return render_template("lib_carto.html")

@app.route("/trajet")
def trajet():
    return render_template("itineraire.html")

#fonction permettant le hachage des mots de passe avant enregistrement   
def multi_hash(password, rounds=5):
    hashed = password.encode()
    for _ in range(rounds):
        hashed = hashlib.sha512(hashed).hexdigest().encode()
    return hashed.decode()

#les méthodes nous permettent de récupérer les identifiants et mots de passe indiqués par les utilisateurs
@app.route('/connexion', methods=['GET', 'POST'])

#fonction permettant l'ajout d'un nouvel utilisateur dans la table User
def authentification():
    #on récupères les mot de passe de l'identifiant indiqués par l'utilisateur
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp_clair = request.form['mdp']
        mdp_hash = multi_hash(mdp_clair, rounds=7)  # hashé 7 fois

        nouvel_utilisateur = User(identifiant=identifiant, mdp=mdp_hash)
        db.session.add(nouvel_utilisateur)
        db.session.commit()

        utilisateurs = User.query.all()

        #affiche la liste des utlisateurs contenu dans la base : cela permet uniquement de montrer que les mot de passe sont bien enregisté en haché (sécurité)
        return render_template("liste_user.html", utilisateurs=utilisateurs)

    return render_template("connexion.html")    


@app.route("/erp_json")
def erp_json():
    #on récupère nos données à partir de leur classe pour ensuite les passer au format geojson
    erps= Erp.query.all()
    return jsonify(
        {
            "type":"FeatureCollection",
            "features":[erp.to_geojson() for erp in erps],
        }
    )

@app.route("/pmr_json")
def pmr_json():
    pmrs= Stationnement.query.all()
    return jsonify(
        {
            "type":"FeatureCollection",
            "features":[pmr.to_geojson() for pmr in pmrs],
        }
    )

@app.route("/cheminement_json")
def cheminement_json():
    cheminements= Troncon_cheminement.query.all()
    return jsonify(
        {
            "type":"FeatureCollection",
            "features":[cheminement.to_geojson() for cheminement in cheminements],
        }
    )


@app.route("/travaux_json")
def travaux_json():
    travaux= Travaux.query.all()
    return jsonify(
        {
            "type":"FeatureCollection",
            "features":[chantier.to_geojson() for chantier in travaux],
        }
    )
    

#Cette route est utilisée pour créer un geojson sur les travaux correspondant au filtre de date demandé par l'utilisateur sur la page "Création cartographique"
@app.route('/travaux_date_json/<date_str>')
def travaux_date_json(date_str):
    # la chaîne de date est converti en objet date Python
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

    # Exécution de la requête SQL pour obtenir les travaux correspondant à la date
    try:
        result = db.session.execute(
            text("""
                SELECT jsonb_build_object(
                    'type',     'FeatureCollection',
                    'features', jsonb_agg(
                        jsonb_build_object(
                            'type',       'Feature',
                            'geometry',   ST_AsGeoJSON(location)::jsonb,
                            'properties', jsonb_build_object(
                                'idtravaux', idtravaux,
                                'duree', duree,
                                'numero', numero,
                                'voie', voie,
                                'commune', commune,
                                'entreprise', entreprise,
                                'datedebut', datedebut,
                                'datefin', datefin,
                                'commentaire', commentaire,
                                'circulation', circulation
                            )
                        )
                    )
                )
                FROM travaux.travaux
                WHERE :p_date BETWEEN datedebut AND datefin
            """),
            {"p_date": date_obj}  # On passe la date dans la requête
        )

        geojson_data = result.fetchone()[0]  # On récupère le GeoJSON formé
        return jsonify(geojson_data)

    except Exception as e:
        # Log l'erreur exacte pour pouvoir la diagnostiquer
        app.logger.error(f"Error executing query: {e}")
        return jsonify({"error": "An error occurred while processing the request"}), 500

#cette route permet de créer le geojson correspondant au trajet le plus court vers une place PMR depuis l'ERP séléctionnée par l'utilisateur
@app.route('/trajet_erp/<int:iderp>') #chemin récupérant l'id de l'ERP choisie
def trajet_erp(iderp):
    with app.app_context():
        #La fonction pour générer le cheminement le plus court à été préalablement crée avec PGadmin
        result = db.session.execute(
            text("""
                SELECT jsonb_build_object(
                    'type',     'FeatureCollection',
                    'features', jsonb_agg(
                        jsonb_build_object(
                            'type',       'Feature',
                            'geometry',   ST_AsGeoJSON(location)::jsonb,
                            'properties', jsonb_build_object(
                                'seq', seq,
                                'node', node,
                                'edge', edge,
                                'origine', origine
                            )
                        )
                    )
                )
                FROM accessibilite.f_trajet_erp(:erp_id)
            """),
            {"erp_id": iderp}
        )

        geojson_data = result.fetchone()[0]  # On récupère l'objet JSON construit
        return jsonify(geojson_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)


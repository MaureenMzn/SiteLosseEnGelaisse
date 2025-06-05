# 🌐 Application Web – Accessibilité à Losse-en-Gelaisse

> Étude de cas – Diplôme de Chef de Projet Géomatique  
> Développé dans le cadre d’un projet pédagogique  

🔗 **Site en ligne :** [http://151.80.27.28:5003/](http://151.80.27.28:5003/)

---

## 🧭 Présentation du projet

Ce dépôt contient le **code source** d’une application web développée dans le cadre d’une étude de cas pour notre formation de **Chef de Projet Géomatique**. L’objectif principal est de proposer un outil interactif de **cartographie et de consultation de données géographiques**, avec un accent particulier sur l’**accessibilité urbaine** dans la commune fictive de **Losse-en-Gelaisse**.

Le site permet d’explorer des données thématiques (ERP, cheminements, travaux, etc.), de générer des cartes personnalisées, de consulter un itinéraire et d’accéder à une **librairie cartographique**, dans une interface responsive et évolutive.

---

## ⚙️ Technologies utilisées

- 🐍 **Python 3**
  - Flask
  - SQLAlchemy
  - GeoAlchemy
- 🗺️ **PostgreSQL/PostGIS**
  - pgRouting
- 🧭 **OpenLayers**
- 🐳 **Docker / Docker Compose**
- 🎨 **HTML / CSS / JavaScript**

---

## 📁 Structure du dépôt

| Fichier / Dossier        | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `app.py`                 | Application principale Flask, routes et logique serveur                     |
| `models.py`              | Définition des classes ORM (modèle de données basé sur le MCD)              |
| `overpass.py`            | Script d'import et de traitement des données via Overpass API               |
| `Dockerfile`             | Image personnalisée PostGIS avec support pgRouting                         |
| `docker-compose.yaml`    | Définition des services (base, app, pgAdmin...)                              |
| `/templates/`            | Pages HTML dynamiques (Jinja2)                                              |
| `/static/`               | Ressources statiques (CSS, images, icônes...)                               |
| `/static/css/`           | Fichiers de styles spécifiques à chaque page ou couche                      |
| `/static/img/`           | Images de navigation et pictogrammes                                       |

---

## 🔒 Accessibilité & RGAA

Le projet vise une **accessibilité partielle conforme au RGAA**, avec plusieurs fonctionnalités intégrées ou prévues :
- Texte alternatif (attribut `alt`)
- Affichage adapté (mode daltonien)
- Compatibilité responsive (web & mobile)
- Navigation clavier
- Plan du site

Évaluation via l’outil [WAVE Accessibility Tool](https://wave.webaim.org/).

---

## 🚧 Améliorations envisagées

- Ajout d’un serveur **WSGI** (comme Gunicorn) pour la mise en production
- Mise en place d’un **proxy inverse sécurisé**
- **Séparation des utilisateurs finaux** par profils : consultation, prestataire, élu, etc.
- **Catalogue de données téléchargeables**
- Description détaillée des itinéraires (distance, direction)
- Personnalisation avancée des cartes (légendes dynamiques, styles personnalisés)

---

## 👥 Auteurs

Projet réalisé par une équipe d’étudiants dans le cadre du diplôme de **Chef de Projet Géomatique** – 2025  
Encadré par l’équipe pédagogique d'IdGeo



# sirs_import

Outil Python pour importer des désordres dans le système SIRS
Python tool for importing damages into the SIRS information system

---

## Description / Description

**FR :**
`sirs_import` permet de valider, transformer et importer des données de désordres, observations et photographies dans SIRS, à partir de fichiers GeoPackage (GPKG) et d’arbres de photos.
Il assure la vérification des colonnes, l’application des fallbacks, la cohérence temporelle et la construction d’un JSON final compatible SIRS.

**EN :**
`sirs_import` validates, transforms and imports damage/inspection/photo data into SIRS using GeoPackage (GPKG) input and photo directories.
It verifies field structures, applies fallback logic, enforces temporal consistency, and produces a final SIRS-compatible JSON.

---

## Installation / Installation

### A) Mode développement local / Local development mode

Pour modifier ou inspecter le code. / For developers or contributors:

git clone [https://github.com/USERNAME/sirs_import](https://github.com/USERNAME/sirs_import)
cd sirs_import
pip install -e .

### B) Installation via pip (future) / Installation via pip (future)

pip install sirs_import

Ensuite / Then:

sirs_import

---

## Utilisation / Usage

### Mode par défaut / Default mode

sirs_import

### Extraction linearId uniquement / Extract-only mode

sirs_import --extract

### Import complet vers CouchDB / Full import into CouchDB

sirs_import --upload

---

## Fichier de configuration / Configuration file

Un fichier `config_sirs.toml` doit être placé dans le répertoire projet.
A `config_sirs.toml` file must be located in the project directory.

Un exemple commenté est fourni / A documented example provided:
config_sirs.example.toml

---

## Données attendues / Expected data format

**FR :** Les colonnes liées aux désordres peuvent être spécifiées directement dans le fichier de configuration.
**EN :** Disorder-related columns can be specified directly in the configuration file.

### Observations

**FR :** automatiquement détectées via le schéma `prefixe1_suffixe`
**EN :** automatically detected using `prefix1_suffix` patterns

obs1_date
obs1_observateurId
...

### Photos

**FR :** automatiquement détectées via le schéma `prefixe1_prefixe2_suffixe`
**EN :** automatically detected using `prefix1_prefix2_suffix` patterns

obs1_pho1_chemin
obs1_pho1_photographeId
...

### Photos dans le répertoire / Pictures expected under:

./folder_name/

**FR :** Le script peut restructurer les répertoires et renommer les photos si nécessaire.
**EN :** The script can reorganize directories and rename pictures if needed.


---

## Export JSON / JSON output

Le script génère / The script produces: <layername>.json

---

## Licence / License

**FR :** Utilisation strictement NON COMMERCIALE. Voir `LICENSE` pour les termes complets.
**EN :** Strictly NON-COMMERCIAL use only. See `LICENSE` for legal terms.

---

## Dépendances / Dependencies

* Python ≥ 3.10
* pandas
* fiona
* shapely
* requests
* tomllib / tomli
* wcwidth

---

## Avertissements / Warnings

**FR :** Ce programme manipule des données opérationnelles sensibles. Vérifiez manuellement les données exportées avant tout import en production.
**EN :** This tool processes operational and potentially critical data. Always manually review exported data before mass ingestion into production.

---

## Statut du projet / Project status

**FR :** Projet en développement, API et comportement susceptibles d’évoluer.
**EN :** Project under active development; API and behavior may change.

---

## Support / Contact

**FR :** Ce projet est publié pour usage public. Les signalements de bugs et suggestions sont bienvenus. Les contributions externes pourront être examinées et intégrées si elles sont pertinentes et cohérentes avec l’objectif du projet.

**EN :** This project is publicly available. Bug reports and suggestions are welcome. External contributions may be reviewed and merged if they are relevant and aligned with the direction of the project.

**FR :** Pour tout retour, bug ou suggestion, contactez l’auteur.
**EN :** For any issue or suggestion, please contact the author.


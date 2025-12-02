```
# sirs_import

Outil Python pour importer des désordres dans SIRS à partir d'un fichier GeoPackage (GPKG)

# Description

`sirs_import` permet de valider, transformer et importer des données de désordres, observations et photographies dans SIRS, à partir de fichiers GeoPackage (GPKG) et d’un dossier photos.

Le système effectue :
- détection automatique des colonnes
- application des valeurs de repli (fallback)
- validation des UUID
- vérification temporelle
- normalisation des références
- génération finale du JSON pour l’import SIRS

# Installation

## Installation via PyPI

```

pip install sirs_import

```

## Développement local

```

git clone [https://github.com/jln-codes/sirs_import.git](https://github.com/jln-codes/sirs_import.git)
cd sirs_import
pip install -e .

```

# Utilisation

## Mode par défaut

```

cd path/to/data
sirs_import

```

## Extraction linearId et contactId uniquement

```

cd chemin/vers/données
sirs_import --extract

```

Crée les fichiers `<layer_name>_linearId.txt` et `<layer_name>_contactId.txt`

## Import complet vers CouchDB

```

cd path/to/data
sirs_import --upload

```

# Fichier de configuration

Un fichier `config_sirs.toml` doit être présent dans le répertoire projet.  
On peut aussi utiliser :

```

sirs_import --config chemin/vers/config.toml

```

Exemple fourni : [config_sirs.example.toml](https://github.com/jln-codes/sirs_import/blob/main/sirs_import/config_sirs.example.toml)

# Données attendues

## Désordres

Les colonnes liées aux désordres peuvent avoir n’importe quel nom et doivent être définies dans le fichier de configuration.

## Observations

Exemple (avec préfixe `obs1`) :

```

obs1_date                # obligatoire
obs1_evolution
obs1_suite
obs1_designation
obs1_observateurId
obs1_suiteApporterId
obs1_nombreDesordres
obs1_urgenceId

```

L’existence du champ obligatoire (suffixe `date`) détermine l’existence de l’élément.

## Photos

Exemple (prefix `obs1_pho1`) :

```

obs1_pho1_chemin              # obligatoire
obs1_pho1_photographeId
obs1_pho1_date
obs1_pho1_designation
obs1_pho1_libelle
obs1_pho1_orientationPhoto
obs1_pho1_coteId

```

## Répertoire photos

Restructuration possible selon SIRS :

```

./folder_name/
TRONCON_A/
TRONCON_B/
TRONCON_C/

```

# Nomenclature SIRS

Certaines valeurs acceptent soit une valeur entière, soit une forme préfixée.

Exemples :

`positionId`, `coteId`, `sourceId`, `categorieDesordreId`,  
`typeDesordreId`, `urgenceId`, `suiteApporterId`,  
`orientationPhoto`, `nombreDesordres`

Ces champs sont normalisés automatiquement.

# Valeurs statiques et fallbacks

Certaines variables peuvent être :
- un nom de colonne à lire dans GPKG
- une valeur statique
- une valeur par défaut (fallback)

Exemple :

```

COL_POSITION_ID = "pos"   → lu depuis colonne `pos`
COL_POSITION_ID = 7       → appliqué à toutes les entrées

```

# Export JSON

Le fichier `nom_couche.json` généré peut ensuite être importé dans SIRS via :

```

sirs_import --upload

```

La validation garantit :
- conformité CouchDB
- conformité SIRS

Mais pas l’adéquation métier.

# Licence

Utilisation strictement NON COMMERCIALE.  
Voir :
https://github.com/jln-codes/sirs_import/blob/main/LICENSE

# Dépendances

* Python 3.10 ou 3.11 uniquement  
* pandas  
* geopandas  
* fiona  
* shapely  
* requests  
* wcwidth  
* tomli (pour Python < 3.11)  
* numpy < 2  
* numexpr >= 2.8.4  
* bottleneck >= 1.3.6  

# Avertissements

Ce programme manipule des données sensibles et modifie les fichiers sources.  
Sauvegardez les données originales.

Certaines relations entre champs ne sont pas vérifiées.  
La responsabilité de la cohérence métier vous incombe.

# Statut du projet

Développement actif — l’API reste susceptible d’évoluer.

# Support / Contact

Contribution et signalement d’anomalies via :  
https://github.com/jln-codes/sirs_import/issues

---

# English version

Full English documentation available at:  
https://github.com/jln-codes/sirs_import/blob/main/README.en.md
```

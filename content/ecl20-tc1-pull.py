from os import system
from pathlib import Path
from pprint import pprint
import requests
from sys import exit

TOKEN = 'mJrJBPaEssicHiaN462p'
API = f'https://gitlab.ec-lyon.fr/api/v4/%s?private_token={TOKEN}&%s'

# Chargement du nom du TD et de la liste des étudiants
nom_td = 'inf-tc1/test'
etudiants = [
	'traffail'
]

# Récupération des informations de l'enseignant
r = requests.get(API % ('user', ''))
if r.status_code != 200:
	exit('Échec de la récupération des données enseignant: ' + r.json()['message'])
print('Données enseignant obtenues')
enseignant = r.json()

# Récupération de la liste des projets de l'enseignant
r = requests.get(API % ('projects', 'membership=true'))
if r.status_code != 200:
	exit('Échec de la récupération de la liste des projets: ' + r.text)
print('Liste des projets obtenue')
projets = r.json()

# Itération et sélection des projets forkés depuis nom_td et possédés par les étudiants
for p in projets:
	if not 'forked_from_project' in p or p['forked_from_project']['path_with_namespace'] != nom_td:
		continue
	etudiant = p['namespace']['path']
	if not etudiant in etudiants:
		continue
	depot = p["path_with_namespace"]
	print(f'Téléchargement du dépôt {depot}')
	
	# Récupère la version courante du projet valide dans le dossier [etudiant]/[nom_td]
	try:
		dossier = Path(depot).mkdir(parents=True)
		system(f'git clone https://gitlab-ci-token:{TOKEN}@gitlab.ec-lyon.fr/{depot}.git {depot} --quiet')
	except FileExistsError:
		system(f'git -C {depot} pull --quiet')

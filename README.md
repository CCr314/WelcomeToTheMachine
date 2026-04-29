# WelcomeToTheMachine

## Installation
### Installer Python
- Installer Python3 `sudo apt install python3`
- Installer pip3 `sudo apt install pip3` 

### Créer l'environnement
`$ python3 -m venv venv`

### installer les librairies
activer l'environnement
`$ source venv\bin\activate`

`$ pip install pygame pymediainfo ffmpeg requests fpdf2 dotenv`

### paramétrer les liens entre les composants de la machine
copier le fichier env.exemple en .env

`$ nano .env`
laisser comme ils sont en test
URI_Convecteur="http://localhost:8080"
URI_Pupitre="http://localhost:8080"

activer les caméras ou pas
ISCAMERA1="ON"
ISCAMERA2="OFF"

activer l'impression ou pas 
ISPRINT="OFF"

Mettre en FullScreen par défaut
ISFULLSCREEN="OFF"



## Lancement

### lancer le bouchon de simulation des ESP
Ouvrir une fenetre terminal (cmd.exe)
se déplacer dans le répertoire du projet
activer l'environnement 

`$ source venv\bin\activate`

lancer le bouchon

`$ python bouchonEsp.py`

### lancer le moteur principal
Ouvrir une fenetre terminal (cmd.exe)
se déplacer dans le répertoire du projet

activer l'environnement 

`$ source venv\bin\activate`

lancer le moteur

`$ python main.py`

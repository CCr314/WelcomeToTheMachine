# http client
import urllib.request

# paramétrage
import os
from dotenv import load_dotenv

load_dotenv()

URI_Convecteur= os.getenv("URI_Convecteur")
URI_Pupitre=os.getenv("URI_Pupitre")

def Neon(no):
    try:
        if no==0:
            print("eteint Néon")
            urllib.request.urlopen(URI_Convecteur + "/neon/off")

        else:
            print("allume neon",no)
            urllib.request.urlopen(URI_Convecteur + "/neon/" + str(no) + "/on")

    except Exception:
        print("erreur appel http")

    return True
def NeonOff(no):
    try:
        print("etient neon",no)
        urllib.request.urlopen(URI_Convecteur + "/neon/" + str(no) + "/off")

    except Exception:
        print("erreur appel http")
    return True
def Color(couleur):
    try:
        print("color")
        urllib.request.urlopen(URI_Convecteur + "/color/" + couleur)
    except Exception:
        print("erreur appel http")
    return True

def Ventilo(on):
    try:
        if on:
            print("ventilo on")
            urllib.request.urlopen(URI_Convecteur + "/ventilo/av/on")

        else:
            print("ventilo off")
            urllib.request.urlopen(URI_Convecteur + "/ventilo/av/off")

    except Exception:
        print("erreur appel http")
    return True

def Voltmetre(action):
    try:
        if action==0:
            print("arret voltmetre")
            print(URI_Pupitre + "/stop")
            urllib.request.urlopen(URI_Pupitre + "/stop")

        elif action==1:
            print("demarrage voltmetre")
            urllib.request.urlopen(URI_Pupitre + "/start")

        elif action==2:
            print("voltmetre on")
            urllib.request.urlopen(URI_Pupitre + "/run")

    except Exception:
        print("erreur appel http")
    return True

def Convecteur(action):
    try:
        if action==0:
            print("arret Convecteur")
            urllib.request.urlopen(URI_Convecteur + "/stop")

        elif action==1:
            print("demarrage Convecteur")
            urllib.request.urlopen(URI_Convecteur + "/start")

        elif action==2:
            print("Convecteur on")
            urllib.request.urlopen(URI_Convecteur + "/run")

    except Exception:
        print("erreur appel http")
    return True

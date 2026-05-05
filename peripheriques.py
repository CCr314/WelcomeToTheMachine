# http client
import urllib.request

# paramétrage
import os
from dotenv import load_dotenv

load_dotenv()

URI_Convecteur= os.getenv("URI_Convecteur")
URI_Pupitre=os.getenv("URI_Pupitre")

def Neon(no):
    if no==0:
        print("eteint Néon")
        contents = urllib.request.urlopen(URI_Convecteur + "/neon/off").read()
        print(contents)
    else:
        print("allume neon",no)
        contents = urllib.request.urlopen(URI_Convecteur + "/neon/" + str(no) + "/on").read()
        print(contents)
    return True
def NeonOff(no):
    print("etient neon",no)
    contents = urllib.request.urlopen(URI_Convecteur + "/neon/" + str(no) + "/off").read()
    print(contents)
    return True

def Ventilo(on):
    if on:
        print("ventilo on")
        contents = urllib.request.urlopen(URI_Convecteur + "/ventilo/on").read()
        print(contents)
    else:
        print("ventilo off")
        contents = urllib.request.urlopen(URI_Convecteur + "/ventilo/off").read()
        print(contents)
    return True

def Voltmetre(action):
    if action==0:
        print("arret voltmetre")
        contents = urllib.request.urlopen(URI_Pupitre + "/voltmetre/stop").read()
        print(contents)
    elif action==1:
        print("demarrage voltmetre")
        contents = urllib.request.urlopen(URI_Pupitre + "/voltmetre/start").read()
        print(contents)
    elif action==2:
        print("voltmetre on")
        contents = urllib.request.urlopen(URI_Pupitre + "/voltmetre/run").read()
        print(contents)
    return True

def Convecteur(action):
    if action==0:
        print("arret Convecteur")
        contents = urllib.request.urlopen(URI_Convecteur + "/stop").read()
        print(contents)
    elif action==1:
        print("demarrage Convecteur")
        contents = urllib.request.urlopen(URI_Convecteur + "/start").read()
        print(contents)
    elif action==2:
        print("Convecteur on")
        contents = urllib.request.urlopen(URI_Convecteur + "/run").read()
        print(contents)
    return True

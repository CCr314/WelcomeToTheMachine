#pyGame
import pygame
import pygame.camera
from pygame.locals import *

# httpserver
import threading
import requests

# http client
import urllib.request


from http.server import HTTPServer, BaseHTTPRequestHandler

# variables
from dotenv import load_dotenv
import os

#video
from pyvidplayer import Video



# FPDF
from fpdf import FPDF

# initialisation des composants
print("initialisation des objets")
pygame.init()
pygame.camera.init()

pygame.joystick.init()

isJoystick=os.getenv("ISJOSTICK")=="ON"
if isJoystick:
    joystick=pygame.joystick.Joystick(0)
    joystick.init()

pygame.mixer.init()

MODEANNEE=0
MODEQUIZ=1

mode=MODEANNEE


# vairables d'environnement
load_dotenv()

isCamera1 = os.getenv("ISCAMERA1")=="ON"
isCamera2 = os.getenv("ISCAMERA2")=="ON"
isCamera=isCamera1 or isCamera2
isImprimante = os.getenv("ISPRINT")=="ON"
URI_Convecteur= os.getenv("URI_Convecteur")
URI_Pupitre=os.getenv("URI_Pupitre")



if isCamera:
    camlist = pygame.camera.list_cameras()
    print(camlist)
    if isCamera1:
        cam1 = pygame.camera.Camera("/dev/video0",(640,480))
        cam1.start()
    if isCamera2:
        cam2 = pygame.camera.Camera("/dev/video2",(640,480))
        cam2.start()


def Neon(no):
    if no==0:
        print("eteint Néon")
        contents = urllib.request.urlopen(URI_Convecteur + "/neon/off").read()
        print(contents)
    else:
        print("alume neon %d",no)
        contents = urllib.request.urlopen(URI_Convecteur + "/neon/" + str(no) + "/on").read()
        print(contents)

def Ventillo(on):
    if on:
        print("ventillo on")
        contents = urllib.request.urlopen(URI_Convecteur + "/ventillo/on").read()
        print(contents)
    else:
        print("ventillo off")
        contents = urllib.request.urlopen(URI_Convecteur + "/ventillo/off").read()
        print(contents)

def Voltmetre(action):
    if action==0:
        print("arret voltmettre")
        contents = urllib.request.urlopen(URI_Pupitre + "/voltmetre/stop").read()
        print(contents)
    elif action==1:
        print("demarrage voltmetre")
        contents = urllib.request.urlopen(URI_Pupitre + "/voltmetre/start").read()
        print(contents)
    elif action==2:
        print("Arret voltmetre")
        contents = urllib.request.urlopen(URI_Pupitre + "/voltmetre/run").read()
        print(contents)


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
        print("Arret Convecteur")
        contents = urllib.request.urlopen(URI_Convecteur + "/run").read()
        print(contents)

            # neon, Ventillo, Voltmetre, Convecteur, noEvent, video,boucle,image, son
actionSequence=[[0,0,0,0,-1,None,False,"Sequence1.jpg", None],  # seq 0 -all bouton
                [0,0,0,0,1,"THE MACHINE Intro Complete.mp4",True,None, None],  # seq 1
                [1,0,1,1,5,None,False,"AttenteDemarreur.jpg", None],  # seq 2 démarrage
                [0,0,0,0,6,None,False,"Demarreur.jpg", None],  # seq 3
                [0,0,0,0,5,None,False,"AttenteDemarreur.jpg", None],  # seq 4
                [0,0,0,0,6,None,False,"Demarreur.jpg", None],  # seq 5
                [0,0,0,0,5,None,False,"AttenteDemarreur.jpg", None],  # seq 6
                [0,0,0,0,1,None,False,"DemarreurOK.jpg", None],  # seq 7
                [0,0,0,0,1,None,False,"vide.jpg", None],  # seq 8
                [0,0,0,0,1,None,False,"vide.jpg", None],  # seq 9
                [0,0,0,0,1,None,False,"vide.jpg", None],  # seq 10
                [0,0,0,0,1,None,False,"vide.jpg", None],  # seq 11
                [0,0,0,0,1,None,False, None, "Back To The Future - Overture.mp3"],  # seq 12
                [0,0,0,0,1,None,False,"vide.jpg", None]]  # seq 13

actionQuiz=[[0,0,0,0,-1,None,False,"QUIZ de Garde 1.jpg"],  # seq 0 -all bouton
                [0,0,0,0,5,None,True,"QUIZ de Garde 2.jpg"],  # seq 1
                [1,0,1,1,5,None,False,"masque.jpg"],  # seq 2 démarrage
                [0,0,0,0,1,None,False,"vide.jpg"]]  # seq 3

equipes=[1965,1976,1981,1998,2000,2011]

scoreEquipe=[0,0,0,0,0,0]

class Sequence():
    no=0
    vid=None
    vidBoucle=False
    img=None
    son=None
    event=0
    noEquipe=0
    def next(self):
        self.no = self.no + 1
        self.action()
    def prev(self):
        self.no=self.no-1
        if self.no < 0:
            self.no=0
        self.action()
    def raz(self):
        self.no=0
        self.noEquipe=0
        self.action()
    def value():
        return self.no
    def flush(self):
        # sauvegarde l'état du jeu
        print("sauvegarde point de reprise")
        #enregistre score equipes
        #enregistre no sequence
    def action(self):
        print("Go sequence %d",self.no)
        Neon(actionSequence[self.no][0])
        Ventillo(actionSequence[self.no][1])
        Voltmetre(actionSequence[self.no][2])
        Convecteur(actionSequence[self.no][3])
        self.event=actionSequence[self.no][4]
        if actionSequence[self.no][5] == None:
            self.vid=None
            self.vidBoucle=False
        else:
            self.vid=Video("./videos/" + actionSequence[self.no][5])
            self.vidBoucle=actionSequence[self.no][6]
        if actionSequence[self.no][7] == None:  # image
            self.img=None
        else:
            self.img=pygame.image.load("./images/" + actionSequence[self.no][7])

        if actionSequence[self.no][8] != None:  # son
            pygame.mixer.music.load('./sons/' + actionSequence[self.no][8])
            pygame.mixer.music.play()


        # actions spécifiques
        if self.no==8 and isCamera1:  # prise des photos
            image1 = cam1.get_image()
            pygame.image.save(image1, "./images/photo1.png")

        if self.no==8 and isCamera2:  # prise des photos
            image2 = cam2.get_image()
            pygame.image.save(image2, "./images/photo2.png")

        if self.no==12:
            impression()

        if self.no==13:
            #fin du jeu : on passe à l'équipe suivante
            self.no=0
            self.noEquipe = self.noEquipe + 1

        #elif self.no==1:
        #elif self.no==2:
        #elif self.no==3:
        #else:

        self.flush()

seq=Sequence()


class Quiz:
    no=0
    vid=None
    vidBoucle=False
    img=None
    event=0
    noEquipe=0
    def next(self):
        self.no = self.no + 1
        self.action()
    def prev(self):
        self.no=self.no-1
        if self.no < 0:
            self.no=0
        self.action()
    def raz(self):
        self.no=0
        self.action()
        self.noEquipe=0
    def value():
        return self.no
    def flush(self):
        # sauvegarde l'état du jeu
        print("sauvegarde point de reprise")
        #enregistre score equipes
        #enregistre no sequence
    def action(self):
        print("Go sequence %d",self.no)
        Neon(actionQuiz[self.no][0])
        Ventillo(actionQuiz[self.no][1])
        Voltmetre(actionQuiz[self.no][2])
        Convecteur(actionQuiz[self.no][3])
        self.event=actionQuiz[self.no][4]
        if actionQuiz[self.no][5] == None:
            self.vid=None
            self.vidBoucle=False
        else:
            self.vid=Video("./videos/" + actionQuiz[self.no][5])
            self.vidBoucle=actionQuiz[self.no][6]
        if actionQuiz[self.no][7] == None:
            self.img=None
        else:
            self.img=pygame.image.load("./images/" + actionSequence[self.no][7])

        if self.no==13:
            #fin du jeu : on passe à l'équipe suivante
            self.no=0
            self.noEquipe = self.noEquipe + 1

quiz = Quiz()

# serveur HTTP endPoint
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

       print(self.path)
       retour = True  # par defaut

       if self.path == '/info':
           self.send_response(200)
           self.send_header('Access-Control-Allow-Origin', '*')
           self.send_header('Access-Control-Allow-Methods', '*')
           self.send_header('Access-Control-Allow-Headers', '*')
           self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
           self.send_header('Content-type','text/plain; charset=utf-8')
           self.end_headers()
           self.wfile.write(b"{'mode':'0', 'seq':'0', 'equipe':'0'}")

       elif self.path == '/getEquipes':
           self.send_response(200)
           self.send_header('Access-Control-Allow-Origin', '*')
           self.send_header('Access-Control-Allow-Methods', '*')
           self.send_header('Access-Control-Allow-Headers', '*')
           self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
           self.send_header('Content-type','text/plain; charset=utf-8')
           self.end_headers()
           self.wfile.write(b"{'equipes[]'}")

       elif self.path =='/modeAnnee':
           print("passe en mode année")
           mode=MODEANNEE
           seq.raz()
       elif self.path =='/modeQuiz':
           print("passe en mode Quiz")
           mode=MODEQUIZ
           quiz.raz()
       elif self.path == '/setEquipe':
           if mode==MODEQUIZ:
               quiz.noEquipe=123
           else :
               seq.noEquipe=123

       elif self.path == '/':
           print("Ne doit pas arriver")
           retour=False
       elif self.path == '/quit':
           retour=True
           my_event = pygame.event.Event(QUIT)
           pygame.event.post(my_event)
       elif self.path == '/next':
           if mode==MODEQUIZ:
               quiz.next()
           else:
                seq.next()
       elif self.path == '/prev':
           if mode==MODEQUIZ:
               quiz.prev()
           else:
                seq.prev()
       elif self.path == '/raz':
           if mode==MODEQUIZ:
               quiz.raz()
           else:
               seq.raz()

       if retour:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', '*')
                self.send_header('Access-Control-Allow-Headers', '*')
                self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                self.send_header('Content-type','text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"OK")
       else:
                self.send_response(400)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', '*')
                self.send_header('Access-Control-Allow-Headers', '*')
                self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                self.send_header('Content-type','text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"KO")


def impression():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("BTTF","","./font/BTTF.ttf")
    pdf.set_font('BTTF', size=12)
    with pdf.rotation(angle=10, x=20, y=30):
        pdf.text(10,10,"Welcome to the Machine")
    if isCamera1:
        pdf.image("images/photo1.png", x=50, y=60)
    pdf.output("./temp/test.pdf")
    if isImprimante:
        print("lancement de l'impression")

print("Préparation WebServer")
def lanceHttpServ():
    print("lancement serveur HTTP port 8081")
    httpd = HTTPServer(('localhost',8081),Serv)
    httpd.serve_forever()

loop_thread = threading.Thread(target=lanceHttpServ)
loop_thread.start()


def boucleParadoxeTemporel():
    loop=True
    vid=Video("./videos/ParadoxeTemporel.mp4")
    #vid.set_volume(100)
    if seq.vid != None:
        seq.vid.pause()

    while loop:
        clock.tick(30)
        pygame.display.update()
        vid.draw(fenetre, (500,400), force_draw=False)

        if vid.isEnd():
            vid.close()
            loop=False

    if seq.vid != None:
        seq.vid.resume()


def checkEvent(event):
    value = 0
    if (event.type == KEYDOWN and event.key == 97) or (event.type == JOYBUTTONDOWN and event.button == 2):
        value = 1  # choix A
    if (event.type == KEYDOWN and event.key == 98) or (event.type == JOYBUTTONDOWN and event.button == 0):
        value = 2 # choix B
    if (event.type == KEYDOWN and event.key == 99) or (event.type == JOYBUTTONDOWN and event.button == 3):
        value = 3 # choix C
    if (event.type == KEYDOWN and event.key == 100) or (event.type == JOYBUTTONDOWN and event.button == 4):
        value = 4 # choix D
    if (event.type == KEYDOWN and event.key == 13) or (event.type == JOYBUTTONDOWN and event.button == 1):
        value = 5 # demarreur on
    if (event.type == KEYUP and event.key == 13) or (event.type == JOYBUTTONDOWN and event.button == 1):
        value = 6 # demarreur off
    if (event.type == KEYDOWN and event.key == 1073741904) or (event.type == JOYAXISMOTION and event.axis == 1 and event.value > 0.5):
        value = 7 # gauche
    if (event.type == KEYDOWN and event.key == 1073741903) or (event.type == JOYAXISMOTION and event.axis == 1 and event.value < -0.5):
        value = 8 # droite
    if (event.type == KEYDOWN and event.key == 1073741906) or (event.type == JOYAXISMOTION and event.axis == 0 and event.value < -0.5):
        value = 9 # haut
    if (event.type == KEYDOWN and event.key == 1073741905) or (event.type == JOYAXISMOTION and event.axis == 0 and event.value > 0.5):
        value = 10 # bas
    return value


print("lancement boucle")
loop=True
nbErreur=0
clock = pygame.time.Clock()
if os.getenv("ISFULLSCREEN")=="ON":
    fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    fenetre = pygame.display.set_mode((1200, 860))

fenetre.fill((120, 120, 120))
pygame.display.flip()

seq.raz()
quiz.raz()


while loop:
    # gestion des evenements
    for event in pygame.event.get():
        eventno=checkEvent(event)
        if eventno > 0:
            print(eventno)

            if mode==MODEQUIZ:
                if quiz.event==-1:  # all event
                    quiz.next()
                elif quiz.event==eventno:
                    quiz.next()
                else:
                    # erreur de bouton
                    if nbErreur > 2:
                        boucleParadoxeTemporel()
                        nbErreur=0  # réinitialise le compteur
                    else:
                        pygame.mixer.music.load('./sons/Klaxon enrhumé.mp3')
                        pygame.mixer.music.play()
                        nbErreur=nbErreur+1
            else:  # MODEANNEE

                if seq.event==-1:  # all event
                    seq.next()
                elif seq.event==eventno:
                    seq.next()
                else:
                    # erreur de bouton
                    if nbErreur > 2:
                        boucleParadoxeTemporel()
                        nbErreur=0  # réinitialise le compteur
                    else:
                        pygame.mixer.music.load('./sons/Klaxon enrhumé.mp3')
                        pygame.mixer.music.play()
                        nbErreur=nbErreur+1

        if event.type == QUIT:
            print("exit")
            loop=False



    clock.tick(30)
    pygame.display.update()

    if seq.vid != None:
        seq.vid.draw(fenetre, (0,0), force_draw=False)

        if seq.vid.isEnd():
            seq.vid.close()
            EnCours = False

    if seq.img != None:
        fenetre.blit(seq.img, (0,0))

pygame.quit()

print("fin normale du progamme")

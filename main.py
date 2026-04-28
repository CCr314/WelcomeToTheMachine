#pyGame
import pygame
import pygame.camera
from pygame.locals import *

#images
from PIL import Image
import drawtext

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

# FPDF et Images
from fpdf import FPDF
masquePhoto = Image.open('./images/masquePhotoEcran.png').convert('RGBA')

# initialisation des composants
print("initialisation des objets")
pygame.init()
pygame.camera.init()

pygame.joystick.init()

font=pygame.font.Font("./font/BTTF.ttf", 40)

isJoystick=os.getenv("ISJOYSTICK")=="ON"
if isJoystick:
    joystick=pygame.joystick.Joystick(0)
    joystick.init()

pygame.mixer.init()

MODEANNEE=0
MODEQUIZ=1

# evenements synchro
EVENT_MODE=pygame.USEREVENT + 1
EVENT_PREV=pygame.USEREVENT + 2
EVENT_NEXT=pygame.USEREVENT + 3
EVENT_RAZ=pygame.USEREVENT + 4
EVENT_EQUIPE=pygame.USEREVENT + 5
EVENT_TEXTE=pygame.USEREVENT + 6

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
        cam1 = pygame.camera.Camera("/dev/video0",(1270,700))
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
        print("voltmetre on")
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
        print("Convecteur on")
        contents = urllib.request.urlopen(URI_Convecteur + "/run").read()
        print(contents)

            # neon, Ventillo, Voltmetre, Convecteur, noEvent, video,boucle,image, son, texte, timer
actionSequence=[[0,0,0,0,-1,"Teasing 60 v3.1.mp4",False,None, None, "Appuyez sur un bouton",0],  # seq 0 -all bouton - boucle d'attente
                [0,0,0,0,5,"THE MACHINE Intro Complete.mp4",True,None, None, None,0],  # seq 1 - intro
                [1,0,1,1,5,"Les Fous du Volant (démarreur 1).mp4",False,None, None, None,0],  # seq 2 - demarreur 1
                [1,0,1,1,5,"THE TIME MACHINE (démarreur 2).mp4",False,None, None, None,0],  # seq 3- demarreur 2
                [1,0,2,2,0,"Retour vers le futur (démarreur 3).mp4",False,None, None, None,0],  # seq 4 - demarreur 3
                [0,0,2,2,1,"ChoixAnneeAvantTirage.mp4",False,None, None,"Appuyez sur le bouton A",4],  # seq 5 - intro photo
                [2,1,2,2,1,None,False,"masqueCamera.png", None, "A pour prendre la photo",4],  # seq 6
                [2,0,2,2,2,None,False,"impression.png", None, "A pour reprendre la photo, B pour poursuivre",3],  # seq 7  TODO gestion du Retry
                [3,0,2,2,3,"ChoixAnneeAvantTirage.mp4",True,None, None, "Appuyez sur le bouton C",2],  # seq 8 - intro choix annéee
                [3,0,2,2,4,"LA MACHINE Année 1976.avi",False,None, None, None,0],  # seq 9 - choix année
                [4,0,2,2,-1,None,False,"impression.png", "Back To The Future - Overture.mp3", "Prendre la carte et la fiche mission",2],  # seq 10 - impression de la mission
                [0,0,0,0,-1,None,False,None, None, "Fin de la mission",0]]  # seq 11 - fin est retour au debut

actionQuiz=[[0,0,0,0,-1,None,False,"QUIZ de Garde 1.jpg",False,None, None, "Appuyez sur un bouton"],  # seq 0 -all bouton
            [0,0,1,1,5,None,True,"QUIZ de Garde 2.jpg",False,None, None, "Demarrez"],  # seq 1
            [1,0,2,2,5,None,False,"masque.jpg",False,None, None, None],  # seq 2 - question
            [2,0,2,2,5,None,False,"masque.jpg",False,None, None, None],  # seq 3 - reponse OK
            [3,1,2,2,5,None,False,"masque.jpg",False,None, None, None],  # seq 4 - reponse KO
            [4,0,2,2,-1,None,False,"score.jpg",False,None, None, None],  # seq 5 - score
            [0,0,0,0,-1,None,False,"vide.jpg",False,None, None, "Fin du quiz"]]  # seq 6 - fin

equipes=["1965","1998","1976","1981","2011","2000"]

scoreEquipe=[0,0,0,0,0,0]

def photo(noEquipe):
    image1 = cam1.get_image()
    pygame.image.save(image1, "./images/photo_" + equipes[noEquipe] + ".jpg")
    # compose le résultat
    #background = Image.open('./images/fondEcran.jpg').convert('RGBA')
    background =Image.new('RGBA', (1920,1080), color=(255,255,255))
    #annee = Image.open('./images/' + equipes[noEquipe] + '.png').convert('RGBA')
    photo = Image.open('./images/photo_' + equipes[noEquipe] + '.jpg')

    background.paste(photo,(400,375))
    background.alpha_composite(masquePhoto)
    #background.alpha_composite(annee,(850,120))
    background.save("./images/impression.png")
    background.save("./images/impression_" + equipes[noEquipe] + ".png")


class Sequence():
    no=0
    vid=None
    vidBoucle=False
    img=None
    son=None
    texte=None
    event=0
    noEquipe=0
    global actionSequence
    actionTable=actionSequence  # par defaut

    def clear(self):  # néttoye la séquence précédente
        if self.vid != None :
            self.vid.close()
        pygame.mixer.music.stop()
        fenetre.fill((120, 120, 120))
        pygame.display.flip()

    def next(self):
        self.clear()
        self.no = self.no + 1
        self.action()
    def prev(self):
        self.clear()
        self.no=self.no-1
        if self.no < 0:
            self.no=0
        self.action()
    def raz(self):
        self.clear()
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
        print("Go sequence",self.no)
        print(self.actionTable)
        Neon(self.actionTable[self.no][0])
        Ventillo(self.actionTable[self.no][1])
        Voltmetre(self.actionTable[self.no][2])
        Convecteur(self.actionTable[self.no][3])
        self.event=self.actionTable[self.no][4]

        if self.actionTable[self.no][5] == None:
            self.vid=None
            self.vidBoucle=False
        else:
            if self.no == 9:   # choix année
                self.vid=Video("./videos/La Machine Année " + equipes[self.noEquipe] + " mp4.mp4")
                self.vid.set_volume(0.5)

            else:
                self.vid=Video("./videos/" + self.actionTable[self.no][5])
                self.vid.set_volume(0.5)
                self.vid.set_size((1920,1080))
                print("video = " + self.actionTable[self.no][5])
            self.vidBoucle=self.actionTable[self.no][6]
        if self.actionTable[self.no][7] == None:  # image
            self.img=None
        else:
            self.img=pygame.image.load("./images/" + self.actionTable[self.no][7])

        if self.actionTable[self.no][8] != None:  # son
            pygame.mixer.music.load('./sons/' + self.actionTable[self.no][8])
            pygame.mixer.music.play()


        if self.actionTable[self.no][10] > 0:   # texte
            self.texte = None
            pygame.time.set_timer(EVENT_TEXTE,self.actionTable[self.no][10]*1000)
        else:
            self.texte = self.actionTable[self.no][9]
        # actions spécifiques
        if self.no==7 and isCamera1:  # prise des photos
            photo(self.noEquipe)

        if self.no==7 and isCamera2:  # prise des photos
            image2 = cam2.get_image()
            pygame.image.save(image2, "./images/photo2.jpg")

        if self.no==10:
            impression(equipes[self.noEquipe])

        if self.no==11:
            #fin du jeu : on passe à l'équipe suivant
            self.noEquipe = self.noEquipe + 1
            self.clear()
            self.no=0
            self.action()

        #elif self.no==1:
        #elif self.no==2:
        #elif self.no==3:
        #else:

        self.flush()

seq=Sequence()

# serveur HTTP endPoint
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

       print(self.path)
       #query = urlparse(self.path).query
       #print(query)
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

       elif self.path =='/modeAnnee':
           print("passe en mode année")
           evt = pygame.event.Event(EVENT_MODE, noMode=MODEANNEE)
           pygame.event.post(evt)
           #mode=MODEANNEE
           #seq.raz()
       elif self.path =='/modeQuiz':
           print("passe en mode Quiz")
           evt = pygame.event.Event(EVENT_MODE, noMode=MODEQUIZ)
           pygame.event.post(evt)

       elif self.path == '/setEquipe':
           evt = pygame.event.Event(EVENT_EQUIPE, no=123)
           pygame.event.post(evt)
       elif self.path == '/':
           print("Ne doit pas arriver")
           retour=False
       elif self.path == '/quit':
           retour=True
           my_event = pygame.event.Event(QUIT)
           pygame.event.post(my_event)
       elif self.path == '/next':
           evt = pygame.event.Event(EVENT_NEXT)
           pygame.event.post(evt)
       elif self.path == '/prev':
           evt = pygame.event.Event(EVENT_PREV)
           pygame.event.post(evt)
       elif self.path == '/raz':
           evt = pygame.event.Event(EVENT_RAZ)

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


def impression(annee):
    pdf = FPDF(orientation="P", unit="mm", format=(150,100))
    pdf.add_page()

    pdf.image("images/impression_" + annee + ".png", x=0, y=0, w=150, h=100)

    pdf.output("./temp/impression" + annee + ".pdf")
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
    vid.set_volume(1)
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
    #if (event.type == KEYUP and event.key == 13) or (event.type == JOYBUTTONDOWN and event.button == 1):
    #    value = 6 # demarreur off
    if (event.type == KEYDOWN and event.key == 1073741904) or (event.type == JOYAXISMOTION and event.axis == 1 and event.value > 0.5):
        value = 7 # gauche
    if (event.type == KEYDOWN and event.key == 1073741903) or (event.type == JOYAXISMOTION and event.axis == 1 and event.value < -0.5):
        value = 8 # droite
    if (event.type == KEYDOWN and event.key == 1073741906) or (event.type == JOYAXISMOTION and event.axis == 0 and event.value < -0.5):
        value = 9 # haut
    if (event.type == KEYDOWN and event.key == 1073741905) or (event.type == JOYAXISMOTION and event.axis == 0 and event.value > 0.5):
        value = 10 # bas
    if (event.type == KEYDOWN and event.key == 110):
        value = 11 # avance
    return value


print("lancement boucle")
try:
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

    while loop:
        # gestion des evenements
        for event in pygame.event.get():
            if event.type == EVENT_MODE:
                mode=event.noMode
                if mode==MODEANNEE:
                    seq.actionTable = actionSequence
                else:
                    seq.actionTable = actionQuiz

                seq.raz()
            elif event.type==  EVENT_PREV:
                seq.prev()
            elif event.type==  EVENT_NEXT:
                seq.next()
            elif event.type==  EVENT_RAZ:
                seq.raz()
            elif event.type== EVENT_EQUIPE:
                seq.noEquipe=event.noEquipe
            elif event.type==EVENT_TEXTE:
                seq.texte = seq.actionTable[seq.no][9]
            elif event.type == QUIT:
                print("exit")
                loop=False
            else:
                eventno=checkEvent(event)
                if eventno > 0:
                    print(eventno)
                    if seq.event==-1 or eventno==11:  # all event ou n
                        seq.next()
                    elif seq.event==eventno:
                        seq.next()
                    elif seq.no==7 and eventno==1:
                        seq.prev()
                    elif eventno != 6:   # par d'erreur au relachement du démarreur
                        # erreur de bouton
                        if nbErreur > 2:
                            boucleParadoxeTemporel()
                            nbErreur=0  # réinitialise le compteur
                        else:
                            pygame.mixer.music.load('./sons/Klaxon enrhumé.mp3')
                            pygame.mixer.music.play()
                            pygame.mixer.music.set_volume(1)
                            nbErreur=nbErreur+1

        clock.tick(30)
        pygame.display.update()

        if seq.vid != None:
            seq.vid.draw(fenetre, (0,0), force_draw=False)

            if seq.vid.isEnd():
                if seq.vidBoucle:
                    seq.vid.restart()
                else:
                    seq.vid.close()
                    seq.next()

        if seq.no == 6 and isCamera1:
            image = cam1.get_image()
            image = pygame.transform.scale(image, (1050,620))
            fenetre.blit(image, (220,100))

        if seq.img != None:
            fenetre.blit(seq.img, (0,0))
        if seq.texte != None:
            textRect = pygame.Rect(100, 1080-150, 1920-200,1080-50)
            drawtext.drawText(fenetre, seq.texte, (255,255,255), textRect, font, drawtext.textAlignCenter, True)



except ValueError as e:
    print("erreur : ", e)
    pass

pygame.quit()

print("fin normale du progamme")

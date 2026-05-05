#pyGame
import pygame
import json
import pygame.camera
from pygame.locals import *
import serveurweb

import constantes as const

import peripheriques

#images
from PIL import Image
import drawtext

# httpserver
import threading


# variables
from dotenv import load_dotenv
import pickle
import os

#video
from pyvidplayer import Video

# FPDF et Images
from fpdf import FPDF
masquePhoto = Image.open('./images/masquePhotoEcran.png').convert('RGBA')
masquePhoto2 = Image.open('./images/quiz2026/masqueCamera.png').convert('RGBA')

cadreOK = pygame.image.load('./images/quiz/cadreOK.png')
cadreKO = pygame.image.load('./images/quiz/cadreKO.png')
cadreReponse = pygame.image.load('./images/quiz/cadreReponse.png')

# initialisation des composants
print("initialisation des objets")
pygame.init()
pygame.camera.init()

pygame.joystick.init()

font=pygame.font.Font("./font/BTTF.ttf", 40)

fontQuiz=pygame.font.Font("./font/BTTF.ttf", 30)
fontQuiz2=pygame.font.Font("./font/GODOFWAR.TTF", 30)
fontQuiz3=pygame.font.Font("./font/GrimeSlime-Regular.ttf", 50)



isJoystick=os.getenv("ISJOYSTICK")=="ON"
if isJoystick:
    joystick=pygame.joystick.Joystick(0)
    joystick.init()

pygame.mixer.init()

# vairables d'environnement
load_dotenv()

isCamera1 = os.getenv("ISCAMERA1")=="ON"
isCamera2 = os.getenv("ISCAMERA2")=="ON"
isCamera=isCamera1 or isCamera2
isImprimante = os.getenv("ISPRINT")=="ON"

if isCamera:
    camlist = pygame.camera.list_cameras()
    print(camlist)
    if isCamera1:
        cam1 = pygame.camera.Camera("/dev/video0",(1300,700))
        cam1.start()
    if isCamera2:
        cam2 = pygame.camera.Camera("/dev/video2",(640,480))
        cam2.start()


            # neon, Ventilo, Voltmetre, Convecteur, noEvent, video,boucle,image, son, texte, timer
actionSequence=[[0,0,0,0,-1,"Teasing 60 v3.1.mp4",True,None, None, "Appuyez sur un bouton",0],  # seq 0 -all bouton - boucle d'attente
                [0,0,0,0,5,"THE MACHINE Intro Complete.mp4",True,None, None, "Demarrez",70],  # seq 1 - intro
                [1,0,1,1,5,"Les Fous du Volant (démarreur 1).mp4",False,None, None, "Echec Demarrage : réésayez",20],  # seq 2 - demarreur 1
                [1,0,1,1,5,"THE TIME MACHINE (démarreur 2).mp4",False,None, None, "Echec Demarrage : réésayez",20],  # seq 3- demarreur 2
                [1,0,2,2,0,"Retour vers le futur (démarreur 3).mp4",False,None, None, "Demarrage Machine OK",3],  # seq 4 - demarreur 3
                [0,0,2,2,1,"LA MACHINE FIXE 2026 avant tirage.mp4",False,None, "PINK FLOYD Time.mp3","Appuyez sur le bouton A",3],  # seq 5 - intro photo
                [2,1,2,2,1,None,False,"masqueCamera.png", None, "A pour prendre la photo",3],  # seq 6
                [2,0,2,2,2,None,False,"impression_%a.png", None, "A pour reprendre la photo, B pour poursuivre",3],  # seq 7  TODO gestion du Retry
                [3,0,2,2,3,"LA MACHINE FIXE 2026 avant tirage.mp4",True,None, None, "Appuyez sur le bouton C",2],  # seq 8 - intro choix annéee
                [3,0,2,2,4,"tirage1976.mp4",False,None, None, "Appuyez sur le bouton D",8],  # seq 9 - choix année
                [4,0,2,2,-1,None,False,"impression_%a_annee.png", "Back To The Future - Overture.mp3", "Prendre la carte et la fiche mission",2],  # seq 10 - impression de la mission
                [0,0,0,0,-1,None,False,None, None, "Fin de la mission",0]]  # seq 11 - fin est retour au debut


actionQuiz=[[0,0,0,0,-1,"Teasing 60 v3.1.mp4",True,None, None, "Appuyez sur un bouton",0],  # seq 0 -all bouton - boucle d'attente
            [0,0,0,0,-1,None,False,"quiz/QUIZ de Garde 1.png", None, "Appuyez sur un bouton",0],  # seq 1 -all bouton
            [0,0,1,1,5,None,True,"quiz/QUIZ de Garde 2.png", None, "Demarrez",0],  # seq 2
            [1,0,2,2,0,None,False,"quiz/QUIZ Masque.png",None,None, 0],  # seq 3 - question
            [2,0,2,2,8,None,False,"quiz/QUIZ Masque OK.png",None,"Allez vers la droite", 3],  # seq 4 - reponse OK
            [3,1,2,2,8,None,False,"quiz/QUIZ Masque KO.png",None,"Allez vers la droite", 3],  # seq 5 - reponse KO
            [4,0,2,2,-1,None,False,"quiz/QUIZ de score.png",None,"Appuyez sur un bouton",10],  # seq 6 - score
            [0,0,0,0,-1,None,False,"vide.jpg",None, "Fin du quiz",0]]  # seq 7 - fin

# neon, Ventilo, Voltmetre, Convecteur, noEvent, video,boucle,image, son, texte, timer
actionQuiz2026=[[0,0,0,0,-1,"IntroQuizPhilippe.mp4",True,None, None, "Appuye sur un bouton",0],  # seq 0 -all bouton - boucle d'attente
            [0,0,0,0,-1,None,False,"quiz2026/QUIZ de Garde 1.png", None, "Demarre",0],  # seq 1 - demarreur
            [0,0,1,1,-1,"LA MACHINE FIXE 2026 avant tirage.mp4",False,"quiz2026/QUIZ Masque.png", None, None,0],  # seq 2 - photo ou video de la question
            [1,0,2,2,5,None,False,"quiz2026/QUIZ Masque.png",None,None, 0],  # seq 3 - question
            [2,0,2,2,8,None,False,"quiz2026/QUIZ Masque OK.png",None,"Va vers la droite", 3],  # seq 4 - reponse OK
            [3,1,2,2,8,None,False,"quiz2026/QUIZ Masque KO.png",None,"Va vers la droite", 3],  # seq 5 - reponse KO
            [4,0,2,2,-1,None,False,"quiz2026/QUIZ de score.png",None,"Appuye sur un bouton",2],  # seq 6 - score
            [2,1,2,2,1,None,False,"quiz2026/masqueCamera.png", None, "A pour prendre la photo",3],  # seq 7
            [2,0,2,2,2,None,False,"impression_%a.png", None, "A pour reprendre la photo, B pour poursuivre",3],  # seq 8  TODO gestion du Retry
            [0,0,0,0,-1,None,False,"fin.jpg","Back To The Future - Overture.mp3", "Fin du quiz",0]]  # seq 9 - fin

equipes=["1998","1965","1976","2011","1981","2000","2026"]
mode=const.MODEANNEE

scoreEquipe=[0,0,0,0,0,0,0]

def photo(noEquipe):
    print("prise de photo et composition images pour ecran")
    image1 = cam1.get_image()
    if noEquipe==6:
        image1 = pygame.transform.scale(image1, (1920,1080))
    pygame.image.save(image1, "./images/photo_" + equipes[noEquipe] + ".jpg")
    background =Image.new('RGBA', (1920,1080), color=(255,255,255))

    if noEquipe==6:
        photo = Image.open('./images/photo_' + equipes[noEquipe] + '.jpg')
        background.paste(photo,(0,0))
        background.alpha_composite(masquePhoto2)
        background.save("./images/impression_" + equipes[noEquipe] + ".png")
        background.save("./images/impression_" + equipes[noEquipe] + "_annee.png")
    else:
        annee = Image.open('./images/' + equipes[noEquipe] + '.png').convert('RGBA')
        photo = Image.open('./images/photo_' + equipes[noEquipe] + '.jpg')

        background.paste(photo,(400,375))
        background.alpha_composite(masquePhoto)
        background.save("./images/impression_" + equipes[noEquipe] + ".png")
        background.alpha_composite(annee,(950,60))
        background.save("./images/impression_" + equipes[noEquipe] + "_annee.png")


class Sequence():
    no=0
    vid=None
    vidBoucle=False
    img=None
    son=None
    texte=None
    event=0
    noEquipe=0

    noQuestion=-1
    noReponse=-1
    global actionSequence
    actionTable=actionSequence  # par defaut
    version=1
    questions=None # table des questions d'une equipe
    question=None  # question en cours
    imgEquipe=None

    def clear(self):  # néttoye la séquence précédente
        if self.vid != None:   # sauf pur le tirage de l"année
            self.vid.close()
        pygame.mixer.music.stop()
        fenetre.fill((0,0,0))
        pygame.display.flip()

    def go(self,cible):
        self.clear()
        self.no = cible
        self.action()

    def next(self):
        if self.no!= 8:  # pas de néttoyage pour le choix de l'année
            self.clear()
        if self.no >= len(self.actionTable)-1:
            self.no=0
        else:
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
        if mode==const.MODEQUIZ and self.version==2:
            self.noEquipe=6
        else:
            self.noEquipe=0

        self.noQuestion=-1

        self.action()
    def value():
        return self.no
    def flush(self):
        # sauvegarde l'état du jeu
        print("sauvegarde point de reprise")
        f = open('./temp/store.pckl', 'wb')
        pickle.dump([mode,scoreEquipe,seq.no,seq.noQuestion,seq.noEquipe],f)
        f.close()
        #enregistre score equipes
        #enregistre no sequence
    def action(self):
        print("Go sequence",self.no)
        peripheriques.Neon(self.actionTable[self.no][0])
        peripheriques.Ventilo(self.actionTable[self.no][1])
        peripheriques.Voltmetre(self.actionTable[self.no][2])
        peripheriques.Convecteur(self.actionTable[self.no][3])
        self.event=self.actionTable[self.no][4]


        if mode==const.MODEANNEE:
            # actions spécifiques : doit être fait avant (notament pour les photos) l'affichage du contenu de l'écran
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

            if self.actionTable[self.no][5] == None:
                self.vid=None
                self.vidBoucle=False
            else:
                if self.no == 9:   # choix année
                    self.vid=Video("./videos/tirage" + equipes[self.noEquipe] + ".mp4")
                    #self.vid.set_volume(0.5)

                else:
                    self.vid=Video("./videos/" + self.actionTable[self.no][5])
                    #self.vid.set_volume(0.5)
                    self.vid.set_size((1920,1080))
                    print("video = " + self.actionTable[self.no][5])
                self.vidBoucle=self.actionTable[self.no][6]

        elif mode==const.MODEQUIZ:
            if self.no==1:
                # charge les données
                if self.version==1:
                    print("charge les données de " +equipes[self.noEquipe])
                    with open("dataQuiz/table"+equipes[self.noEquipe]+".json") as f:
                        self.questions = json.load(f)
                    self.imgEquipe = pygame.image.load('./images/' + equipes[self.noEquipe] + '.png')
                else:
                    print("charge les données de version 2")
                    with open("dataQuiz/table2026.json") as f:
                        self.questions = json.load(f)
                    self.imgEquipe = None
                    print(len(self.questions ))
            elif self.no==7 and isCamera1:  # prise des photos
                photo(6)
            elif self.version==1 and self.no==3:
                self.noQuestion = self.noQuestion + 1
                self.question = self.questions[self.noQuestion]
            elif self.version==2 and self.no==2:
                self.noQuestion = self.noQuestion + 1
                self.question = self.questions[self.noQuestion]
            elif self.no==6:
                self.question=None
                self.noQuestion = -1
            elif self.no==7 and version==1:   # Fin
                print("fin")
                # todo gerer la fin pour les différents mode
                if self.noEquipe >=6:
                    print("fin du jeu")
                    #todo gérer la fin du game
                else:
                    print("on passe à l'équipe suivante")
                    self.noEquipe = self.noEquipe + 1
                    self.clear()
                    self.no=0
                    self.action()
            elif self.no==9 and self.version==2:   # Fin

                #todo : imprime la photo
                print("fin du jeu")

            # video
            if self.actionTable[self.no][5] == None:
                self.vid=None
                self.vidBoucle=False
            else:
                if mode==const.MODEQUIZ and self.version==2 and self.no==2:
                    if seq.question['video'] != None:
                        print("lance video " + seq.question['video'])
                        self.vid=Video("./videos/quiz2026/" + seq.question['video'])
                        self.vid.set_size((1920,1080))
                        seq.img=None
                else:
                    self.vid=Video("./videos/" + self.actionTable[self.no][5])
                    #self.vid.set_volume(0.5)
                    self.vid.set_size((1920,1080))
                    print("video = " + self.actionTable[self.no][5])

                self.vidBoucle=self.actionTable[self.no][6]


        if self.actionTable[self.no][7] == None:  # image
            self.img=None
        else:
            if mode==const.MODEQUIZ and self.version==2 and self.no==2:
                if seq.question['image'] != None:
                    print("lance image " + seq.question['image'])
                    self.img=pygame.image.load("./videos/quiz2026/" + seq.question['image'])
                    pygame.time.set_timer(const.EVENT_NEXT,const.TPSIMAGES*1000,True)
                    self.vid=None
            else:
                print("image question " + self.actionTable[self.no][7])
                self.img=pygame.image.load("./images/" + self.actionTable[self.no][7].replace("%a",equipes[self.noEquipe] ))

        if self.actionTable[self.no][8] != None:  # son
            pygame.mixer.music.load('./sons/' + self.actionTable[self.no][8])
            pygame.mixer.music.play()


        if self.actionTable[self.no][10] > 0:   # texte
            self.texte = None
            pygame.time.set_timer(const.EVENT_TEXTE,self.actionTable[self.no][10]*1000,True)
        else:
            self.texte = self.actionTable[self.no][9]

        self.flush()

seq=Sequence()


def impression(annee):
    pdf = FPDF(orientation="P", unit="mm", format=(150,100))
    pdf.add_page()

    pdf.image("images/impression_" + annee + ".png", x=0, y=0, w=150, h=100)

    pdf.output("./temp/impression" + annee + ".pdf")
    if isImprimante:
        print("lancement de l'impression")

print("Préparation WebServer")
loop_thread = threading.Thread(target=serveurweb.lanceHttpServ)
loop_thread.start()

def boucleParadoxeTemporel():
    loop=True
    if mode== const.MODEQUIZ and seq.version==2:
        vid=Video("./videos/Lamemoirequiflanche.mp4")
    else:
        vid=Video("./videos/ParadoxeTemporel.mp4")
    #vid.set_volume(1)
    if seq.vid != None:
        seq.vid.pause()

    while loop:
        clock.tick(30)
        pygame.display.update()
        vid.draw(fenetre, (200,200), force_draw=False)

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
    if (event.type == KEYDOWN and event.key == 110):  # spécifique recette pour avancer vite
        value = 11 # avance
    if (event.type == KEYDOWN and event.key == 113):  # spécifique recette pour lancer le mode quiz
        value = 12 # quiz
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

    fenetre.fill((0,0,0))
    pygame.display.flip()

    # recupere les variables
    #try:
#        f = open('./temp/store.pckl', 'rb')
#        mode,scoreEquipe,seq.no,seq.noQuestion,seq.noEquipe = pickle.load(f)
#        f.close()
#        print("demarrage sequence " + str(seq.no))
#        seq.go(seq.no)
#    except FileNotFoundError:
#        print("pas de fichier de récupération")
#    except EOFError:
#        print("fichier de récupération incorrect")
#    finally:
#        print("démarrage au début")
#

    seq.raz()
    while loop:

        # gestion des evenements
        for event in pygame.event.get():
            if event.type == const.EVENT_MODE:
                print("change Mode")
                mode=event.noMode
                nbErreur=0
                seq.version=1
                if mode==const.MODEANNEE:
                    seq.actionTable = actionSequence
                    nbErreur=0
                elif mode==const.MODEQUIZ:
                    seq.actionTable = actionQuiz
                    seq.version=1
                    nbErreur=0

                elif mode==const.MODEQUIZ2026:
                    print("mode 2026")
                    nbErreur=0
                    seq.noEquipe=6 # 2026 est la 7 ième equipe
                    fontQuiz=fontQuiz2
                    seq.actionTable = actionQuiz2026
                    mode=const.MODEQUIZ
                    seq.version=2
                seq.raz()
            elif event.type==  const.EVENT_PREV:
                seq.prev()
            elif event.type==  const.EVENT_NEXT:
                seq.next()
            elif event.type==  const.EVENT_RAZ:
                seq.raz()
            elif event.type== const.EVENT_EQUIPE:
                print("affecte equipe " + str(event.no))
                seq.noEquipe=event.no
                nbErreur=0
            elif event.type==const.EVENT_TEXTE:
                seq.texte = seq.actionTable[seq.no][9]
            elif event.type == QUIT:
                print("exit")
                loop=False
            else:
                eventno=checkEvent(event)
                if eventno > 0:
                    print(eventno)

                    if eventno==12:   # mode quiz
                        mode=const.MODEQUIZ
                        seq.actionTable = actionQuiz
                        nbErreur=0
                        print("go Quiz")
                        seq.raz()
                    elif seq.event==-1 or eventno==11:  # all event ou 'n'
                        seq.next()
                    elif mode==const.MODEQUIZ and seq.no>=4 and seq.no<=5 and eventno==8:  # réponse à la question
                        print("question suivante")
                        if seq.noQuestion >= len(seq.questions)-1:
                            seq.go(6)
                        else:
                            if seq.version==1:
                                seq.go(3)
                            else:
                                seq.go(2)

                    elif seq.event==eventno:
                        seq.next()
                    elif mode==const.MODEQUIZ and seq.no==3 and eventno>=1 and eventno<=4:  # réponse à la question
                        print("réponse à la question")
                        seq.noReponse=eventno-1
                        if seq.question['reponse']==seq.noReponse:
                            scoreEquipe[seq.noEquipe]=scoreEquipe[seq.noEquipe]+1
                            seq.next()
                        else:
                            if nbErreur > 2:
                                boucleParadoxeTemporel()
                                nbErreur=0  # réinitialise le compteur
                                seq.go(5)
                            else:
                                seq.go(5)
                                pygame.mixer.music.load('./sons/Klaxon enrhumé.mp3')
                                pygame.mixer.music.play()
                                #pygame.mixer.music.set_volume(1)
                                nbErreur=nbErreur+1

                    elif mode==const.MODEANNEE and seq.no==7 and eventno==1:  # reprendre la photo
                        seq.prev()
                    elif mode==const.MODEQUIZ and seq.version==2 and seq.no==8 and eventno==1:  # reprendre la photo
                        seq.prev()
                    elif eventno != 6:   # pas d'erreur au relachement du démarreur
                        # erreur de bouton
                        if nbErreur > 2:
                            boucleParadoxeTemporel()
                            nbErreur=0  # réinitialise le compteur
                        else:
                            pygame.mixer.music.load('./sons/Klaxon enrhumé.mp3')
                            pygame.mixer.music.play()
                            #pygame.mixer.music.set_volume(1)
                            nbErreur=nbErreur+1



        # traitements spécifiques
        if mode==const.MODEANNEE:
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

        elif mode==const.MODEQUIZ:


            if seq.vid != None:
                seq.vid.draw(fenetre, (0,0), force_draw=False)

                if seq.vid.isEnd():
                    if seq.vidBoucle:
                        seq.vid.restart()
                    else:
                        seq.vid.close()
                        seq.next()

            if seq.no == 7 and isCamera1:
                image = cam1.get_image()
                image = pygame.transform.scale(image, (1920,1080))
                fenetre.blit(image, (0,0))

            if seq.img != None:  # affiche l'image de fond
                fenetre.blit(seq.img, (0,0))

            if seq.question != None and seq.imgEquipe!=None:
                # année
                fenetre.blit(seq.imgEquipe, (660,140))

            if seq.question != None and seq.no!=2:
                # question
                textRect = pygame.Rect(300, 320, 1920-600, 600)
                if seq.version==2:
                    drawtext.drawText(fenetre, seq.question['question'], (30,30,30), textRect, fontQuiz3, drawtext.textAlignCenter, True)
                else:
                    drawtext.drawText(fenetre, seq.question['question'], (30,30,30), textRect, fontQuiz, drawtext.textAlignCenter, True)

                taille=(700,160)
                for n in range(4):
                    textRect = pygame.Rect(const.posQuestions[n],taille)
                    if seq.version==2:
                        drawtext.drawText(fenetre, seq.question['choix'][n], (30,30,30), textRect, fontQuiz3, drawtext.textAlignLeft , True)
                    else:
                        drawtext.drawText(fenetre, seq.question['choix'][n], (30,30,30), textRect, fontQuiz, drawtext.textAlignLeft , True)
                if seq.no==4:  # bonne reponse
                    fenetre.blit(cadreOK, const.posCadre[seq.question['reponse']])
                elif seq.no==5:  # mauvaise reponse
                    fenetre.blit(cadreReponse, const.posCadre[seq.question['reponse']])
                    fenetre.blit(cadreKO, const.posCadre[seq.noReponse])
            if seq.no==6: # score
                scoreEquipe[seq.noEquipe]
                textRect = pygame.Rect(620, 750, 600,114 )
                if seq.version==2:
                    drawtext.drawText(fenetre, "ton score : " + str(scoreEquipe[seq.noEquipe]) + "/" + str(len(seq.questions)), (0,0,0), textRect, fontQuiz2, drawtext.textAlignCenter, True)
                else:
                    drawtext.drawText(fenetre, "Votre score : " + str(scoreEquipe[seq.noEquipe]) + "/" + str(len(seq.questions)), (0,0,0), textRect, font, drawtext.textAlignCenter, True)


            if seq.texte != None:
                textRect = pygame.Rect(100, 1080-100, 1920-200,1080-20)
                if seq.version==2:
                    drawtext.drawText(fenetre, seq.texte, (30,30,30), textRect, fontQuiz2, drawtext.textAlignCenter, True)
                else:
                    drawtext.drawText(fenetre, seq.texte, (30,30,30), textRect, font, drawtext.textAlignCenter, True)

        clock.tick(30)
        pygame.display.update()


except ValueError as e:
    print("erreur : ", e)
    pass

pygame.quit()

print("fin normale du progamme")
exit(0)

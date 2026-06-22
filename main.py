#pyGame
import pygame
import json

from pygame.locals import *
import serveurweb

import constantes as const
import impression as impr

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

cadreOK = pygame.image.load('./images/quiz/cadreOK.png')
cadreKO = pygame.image.load('./images/quiz/cadreKO.png')
cadreReponse = pygame.image.load('./images/quiz/cadreReponse.png')

# initialisation des composants
print("initialisation des objets")
pygame.init()


pygame.joystick.init()

font=pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 50)
fontQuiz=pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 65)
fontQuiz2=pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 95)


isJoystick=os.getenv("ISJOYSTICK")=="ON"
if isJoystick:
    joystick=pygame.joystick.Joystick(0)
    joystick.init()

pygame.mixer.init()

# vairables d'environnement
load_dotenv()

            # neon, Ventilo, Voltmetre, Convecteur, noEvent, video,boucle,image, son, texte, timer
actionSequence=[]  # seq 11 - fin est retour au debut


actionQuiz=[[0,0,1,1,5,None,True,"quiz/Quizz de garde.png", "Realm of Tranquil Eternity - Disc 1 Sakura and Violet Thunder｜Genshin Impact.mp3", "Demarrez",10],  # seq 0
            [1,0,2,2,0,None,False,"quiz/Quizz Masque.png",None,None, 0],  # seq 1 - question
            [2,0,2,2,8,None,False,"quiz/Quizz Masque OK.png",None,"Allez vers la droite", 3],  # seq 2 - reponse OK
            [3,1,2,2,8,None,False,"quiz/Quizz Masque KO.png",None,"Allez vers la droite", 3],  # seq 3 - reponse KO
            [4,0,2,2,-1,None,False,"quiz/Quizz de Score.jpg",None,"Appuyez sur un bouton",10],  # seq 4 - score
            [0,0,0,0,-1,None,False,"fin.jpg",None, "Fin du quiz",0]]  # seq 5 - fin

equipes=["A","B"]
mode=const.MODEQUIZ

scoreEquipe=[0,0]

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
    global actionQuiz
    actionTable=actionQuiz  # par defaut
    version=1
    questions=None # table des questions d'une equipe
    question=None  # question en cours

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
        if self.no!= 1:  # pas de néttoyage pour la réponse à la question
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
        self.noEquipe=0

        self.noQuestion=-1

        self.action()
    def value():
        return self.no

    def action(self):
        print("Go sequence",self.no)
        peripheriques.Neon(self.actionTable[self.no][0])
        peripheriques.Ventilo(self.actionTable[self.no][1])
        peripheriques.Voltmetre(self.actionTable[self.no][2])
        peripheriques.Convecteur(self.actionTable[self.no][3])
        self.event=self.actionTable[self.no][4]


        if mode==const.MODEANNEE:
            # actions spécifiques : doit être fait avant l'affichage du contenu de l'écran
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
                print("charge les données de " +equipes[self.noEquipe])
                with open("dataQuiz/table"+equipes[self.noEquipe]+".json") as f:
                    self.questions = json.load(f)
                self.noQuestion = self.noQuestion + 1
                self.question = self.questions[self.noQuestion]
            elif self.no==4:   # fin des questions
                self.question=None
                self.noQuestion = -1
            elif self.no==5:   # Fin
                print("fin")
                # todo gerer la fin pour les différents mode
                if self.noEquipe >=1:
                    print("fin du jeu")
                else:
                    print("on passe à l'équipe suivante")
                    self.noEquipe = self.noEquipe + 1
                    self.clear()
                    self.no=0
                    self.action()

            # video
            if self.actionTable[self.no][5] == None:
                self.vid=None
                self.vidBoucle=False
            else:
                if mode==const.MODEQUIZ and self.no==2:   # réponse
                    if seq.question['video'] != None:
                        print("lance video " + seq.question['video'])
                        self.vid=Video("./dataQuiz/" + seq.question['video'])
                        self.vid.set_size((1920,1080))
                        seq.img=None
                    elif seq.question['image'] != None:
                        print("affiche image " + seq.question['image'])
                        seq.img=pygame.image.load("./dataQuiz/" + seq.question['image'])
                else:
                    self.vid=Video("./videos/" + self.actionTable[self.no][5])
                    #self.vid.set_volume(0.5)
                    self.vid.set_size((1920,1080))
                    print("video = " + self.actionTable[self.no][5])

                self.vidBoucle=self.actionTable[self.no][6]


        if self.actionTable[self.no][7] == None:  # image
            self.img=None
        else:
            if mode==const.MODEQUIZ and self.no==2:
                if seq.question['image'] != None:
                    print("lance image " + seq.question['image'])
                    self.img=pygame.image.load("./images/" + seq.question['image'])
                    #pygame.time.set_timer(const.EVENT_NEXT,const.TPSIMAGES*1000,True)
                    self.vid=None
                elif seq.question['video'] != None:
                    print("lance video " + seq.question['video'])
                    self.vid=Video("./videos/" + seq.question['video'])
                    #self.vid.set_volume(0.5)
                    self.vid.set_size((1920,1080))
                    self.img=None
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

seq=Sequence()


print("Préparation WebServer")
loop_thread = threading.Thread(target=serveurweb.lanceHttpServ)
loop_thread.start()

def boucleParadoxeTemporel():
    loop=True
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
                seq.go(0)
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
                    elif mode==const.MODEQUIZ and seq.no>=2 and seq.no<=3 and eventno==8:  # réponse à la question

                        if seq.noQuestion >= len(seq.questions)-1:
                            print("fin du Quizz")
                            seq.go(4)
                        else:
                            print("question suivante")
                            if seq.version==1:
                                seq.go(1)
                            else:
                                seq.go(1)

                    elif seq.event==eventno:
                        seq.next()
                    elif mode==const.MODEQUIZ and seq.no==1 and eventno>=1 and eventno<=4:  # réponse à la question
                        print("réponse à la question : ", eventno)
                        seq.noReponse=eventno
                        if seq.question['reponse']==seq.noReponse:
                            print("play OK")
                            pygame.mixer.music.load('./sons/Bonne_reponse.mp3')
                            pygame.mixer.music.play()
                            scoreEquipe[seq.noEquipe]=scoreEquipe[seq.noEquipe]+1
                            seq.next()
                        else:
                            print("play KO")
                            pygame.mixer.music.load('./sons/Mauvaise_reponse.mp3')
                            pygame.mixer.music.play()
                            #pygame.mixer.music.set_volume(1)
                            nbErreur=nbErreur+1
                            #seq.go(3)
                            seq.next()

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
                        seq.go(1)

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
                        seq.go(1)

            if seq.img != None:  # affiche l'image de fond
                fenetre.blit(seq.img, (0,0))

            if seq.question != None and seq.no==1:
                # question
                textRect = pygame.Rect(300, 150, 1920-600, 600)
                if seq.version==2:
                    drawtext.drawText(fenetre, seq.question['question'], (255,228,194), textRect, fontQuiz3, drawtext.textAlignCenter, True)
                else:
                    drawtext.drawText(fenetre, seq.question['question'], (255,228,194), textRect, fontQuiz, drawtext.textAlignCenter, True)

                taille=(800,320)
                for n in range(4):
                    textRect = pygame.Rect(const.posQuestions[n],taille)
                    if seq.version==2:
                        drawtext.drawText(fenetre, seq.question['choix'][n], (255,228,194), textRect, fontQuiz3, drawtext.textAlignLeft , True)
                    else:
                        drawtext.drawText(fenetre, chr(65+n) + " - " + seq.question['choix'][n], (255,228,194), textRect, fontQuiz, drawtext.textAlignLeft , True)
                if seq.no==2:  # bonne reponse
                    fenetre.blit(cadreOK, const.posCadre[seq.question['reponse']])
                elif seq.no==3:  # mauvaise reponse
                    fenetre.blit(cadreReponse, const.posCadre[seq.question['reponse']])
                    fenetre.blit(cadreKO, const.posCadre[seq.noReponse])

            if seq.no==4: # score
                scoreEquipe[seq.noEquipe]
                textRect = pygame.Rect(620, 750, 600,114 )
                if seq.version==2:
                    drawtext.drawText(fenetre, "ton score : " + str(scoreEquipe[seq.noEquipe]) + "/" + str(len(seq.questions)), (255,228,194), textRect, fontQuiz2, drawtext.textAlignCenter, True)
                else:
                    drawtext.drawText(fenetre, "Votre score : " + str(scoreEquipe[seq.noEquipe]) + "/" + str(len(seq.questions)),(255,4,45), textRect, fontQuiz, drawtext.textAlignCenter, True)


            if seq.texte != None:
                textRect = pygame.Rect(100, 1080-100, 1920-200,1080-20)
                if seq.version==2:
                    drawtext.drawText(fenetre, seq.texte, (255,228,194), textRect, fontQuiz2, drawtext.textAlignCenter, True)
                else:
                    drawtext.drawText(fenetre, seq.texte, (255,228,194), textRect, font, drawtext.textAlignCenter, True)

        clock.tick(30)
        pygame.display.update()


except ValueError as e:
    print("erreur : ", e)
    pass

pygame.quit()

print("fin normale du progamme")
exit(0)

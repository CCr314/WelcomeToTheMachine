# definition des constantes
import pygame

MODEANNEE=0
MODEQUIZ=1
MODEQUIZ2026=2

# evenements synchro
EVENT_MODE=pygame.USEREVENT + 1
EVENT_PREV=pygame.USEREVENT + 2
EVENT_NEXT=pygame.USEREVENT + 3
EVENT_RAZ=pygame.USEREVENT + 4
EVENT_EQUIPE=pygame.USEREVENT + 5
EVENT_TEXTE=pygame.USEREVENT + 6
EVENT_VERSION=pygame.USEREVENT + 7

TPSIMAGES=2   # TODO remettre à 10 

posCadre=[(160,550),(990,550),(160,740),(990,740)]
posQuestions=[(300,650),(1130,650),(300,830),(1130,830)]

#pyGame
import pygame
import pygame.camera
from pygame.locals import *

# httpserver
import threading
import requests

from http.server import HTTPServer, BaseHTTPRequestHandler

# variables
from dotenv import load_dotenv
import os

# FPDF
from fpdf import FPDF

# initialisation des composants
print("initialisation des objets")
pygame.init()
pygame.camera.init()

# vairables d'environnement
load_dotenv()

isCamera = os.getenv("ISCAMERA")=="ON"

if isCamera:
    cam = pygame.camera.Camera("/dev/video0",(640,480))
    cam.start()
    image = cam.get_image()

class Sequence():
    no=0
    def next():
        no = no+1
    def prev()
        no=no-1
        if no < 0:
            no=0
    def value():
        return no

seq=Sequence()

# serveur HTTP endPoint
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
       print(self.path)
       if self.path == '/':
           self.send_response(200)
           self.send_header('Content-type','text/plain; charset=utf-8')
           self.end_headers()
           self.wfile.write(b"OK")
       if self.path == '/quit':
           self.send_response(200)
           self.wfile.write(b"OK")
           self.send_header('Content-type','text/plain; charset=utf-8')
           self.end_headers()
           my_event = pygame.event.Event(QUIT)
           pygame.event.post(my_event)


print("Lancement WebServer")
httpd = HTTPServer(('localhost',8081),Serv)

print("lancement boucle")
loop=True
clock = pygame.time.Clock()
fenetre = pygame.display.set_mode([1280, 720])
fenetre.fill((120, 120, 120))
pygame.display.flip()
while loop:
    # gestion des evenements
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            print("keydown")
            response = requests.get(os.getenv("URI_Convecteur") + "/convecteur/start",timeout=1)
            print(response.text)
            #API ESP pupitre
            #/volt/start
            #/volt/stop
            #/volt/run

            #API convecteur
            #/convecteur/start
            #/convecteur/stop
            #/convecteur/run
            #/convecteur/error
            #/relay/<no>/[On|Off]
        if event.type == QUIT:
            print("exit")
            loop=False
    
    clock.tick(30)
    httpd.handle_request()

pygame.quit()

print("fin normale du progamme")

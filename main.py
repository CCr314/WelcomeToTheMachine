#pyGame
import pygame
import pygame.camera
from pygame.locals import *

# httpserver
import threading
import requests

from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
import os

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

# serveur HTTP endPoint
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
       if self.path == '/':
           self.send_response(200)
           self.send_header('Content-type','text/plain; charset=utf-8')
           self.end_headers()
           self.wfile.write(b"OK")
       if self.path == '/quit':
           my_event = pygame.event.Event(QUIT)
           pygame.event.post(my_event)
           self.wfile.write(b"OK")
           self.send_response(200)

def startWebServeur():
    print("Lancement WebServer")
    httpd = HTTPServer(('localhost',8081),Serv)

loop_thread = threading.Thread(target=startWebServeur)
loop_thread.start()

print("lancement boucle")
loop=True
clock = pygame.time.Clock()
fenetre = pygame.display.set_mode([1280, 720])
fenetre.fill((120, 120, 120))
pygame.display.flip()
while loop:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            print("keydown")
            response = requests.get(os.getenv("URI_Convecteur") + "/convecteur/start")
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




            print(response.text)
        if event.type == QUIT:
            print("exit")
            loop=False
    clock.tick(10)

pygame.quit()
print("fin normale du progamme")

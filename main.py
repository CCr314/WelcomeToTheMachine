#pyGame
import pygame
import pygame.camera
from pygame.locals import *

# httpserver
import threading
import requests

from http.server import HTTPServer, BaseHTTPRequestHandler


# initialisation des composants
print("initialisation des objets")
pygame.init()
pygame.camera.init()

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
    httpd = HTTPServer(('localhost',8080),Serv)

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
            response = requests.get("http://localhost:8080")
            #API ESP pupitre
            #VoltDemarrage
            #VoltArret
            #VoltTestOn
            #VoltTestOff
            #CamTangage?Value=x
            #CamLacet?Value=x



            print(response.text)
        if event.type == QUIT:
            print("exit")
            loop=False
    clock.tick(10)

pygame.quit()
print("fin normale du progamme")

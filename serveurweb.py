import pygame
import requests
import pickle
from http.server import HTTPServer, BaseHTTPRequestHandler
import constantes as const


# serveur HTTP endPoint
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        print(self.path)
        #query = urlparse(self.path).query
        #print(query)
        retour = True  # par defaut

        if self.path == '/info':
            try:
                f = open('./temp/store.pckl', 'rb')
                mode,scoreEquipe,no,noQuestion,noEquipe = pickle.load(f)
                f.close()
            except FileNotFoundError:
                print("pas de fichier de récupération")
            except EOFError:
                print("fichier de récupération incorrect")

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.send_header('Content-type','text/plain; charset=utf-8')
            self.end_headers()
            reponse = "{'mode':'" + str(mode) + "', 'seq':'" + str(no) + "', 'equipe':'" + str(noEquipe) + "'}"
            print(reponse)
            self.wfile.write(reponse.encode())
        else:

           if self.path =='/modeAnnee':
               print("passe en mode année")
               evt = pygame.event.Event(const.EVENT_MODE, noMode=const.MODEANNEE)
               pygame.event.post(evt)
           elif self.path =='/modeQuiz':
               print("passe en mode Quiz")
               evt = pygame.event.Event(const.EVENT_MODE, noMode=const.MODEQUIZ)
               pygame.event.post(evt)
           elif self.path =='/modeQuiz2026':
               print("passe en mode Quiz 2026")
               evt = pygame.event.Event(const.EVENT_MODE, noMode=const.MODEQUIZ2026)
               pygame.event.post(evt)
           elif self.path == '/setEquipe/0':
               evt = pygame.event.Event(const.EVENT_EQUIPE, no=0)
               pygame.event.post(evt)
           elif self.path == '/setEquipe/1':
               evt = pygame.event.Event(const.EVENT_EQUIPE, no=1)
               pygame.event.post(evt)
           elif self.path == '/setEquipe/2':
               evt = pygame.event.Event(const.EVENT_EQUIPE, no=2)
               pygame.event.post(evt)
           elif self.path == '/setEquipe/3':
               evt = pygame.event.Event(const.EVENT_EQUIPE, no=3)
               pygame.event.post(evt)
           elif self.path == '/setEquipe/4':
               evt = pygame.event.Event(const.EVENT_EQUIPE, no=4)
               pygame.event.post(evt)
           elif self.path == '/setEquipe/5':
               evt = pygame.event.Event(const.EVENT_EQUIPE, no=5)
               pygame.event.post(evt)
           elif self.path == '/':
               print("Ne doit pas arriver")
               retour=False
           elif self.path == '/quit':
               retour=True
               my_event = pygame.event.Event(const.QUIT)
               pygame.event.post(my_event)
           elif self.path == '/next':
               evt = pygame.event.Event(const.EVENT_NEXT)
               pygame.event.post(evt)
           elif self.path == '/prev':
               evt = pygame.event.Event(const.EVENT_PREV)
               pygame.event.post(evt)
           elif self.path == '/raz':
               evt = pygame.event.Event(const.EVENT_RAZ)
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


def lanceHttpServ():
    print("lancement serveur HTTP port 8081")
    httpd = HTTPServer(('localhost',8081),Serv)
    httpd.serve_forever()

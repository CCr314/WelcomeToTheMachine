import threading
import pygame
import pygame.freetype

number=25
pygame.init()

EVENT_EQUIPE = pygame.USEREVENT + 1

screen_resolution = (1024, 768)
screen = pygame.display.set_mode(size=screen_resolution)

while True:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
       if event.type == EVENT_EQUIPE:
           print(event.no)
       if event.type == pygame.KEYDOWN and event.key==97:
         evt = pygame.event.Event(EVENT_EQUIPE, no=number)
         pygame.event.post(evt)
       if event.type == pygame.KEYDOWN and event.key==98:

           number=26
           print(number)

       pygame.display.flip()

pygame.quit()

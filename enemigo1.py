import pygame
import random
from laser import Laser
from pygame.sprite import Group


class Enemigo(pygame.sprite.Sprite):
# se crea la clase enemigo, la cual hereda la clase Sprite del modulo pygame.sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('asteroide.png')
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()

    def movimiento(self):
# el enemigo se va a mover de a 1 pixel
        self.rect.y += 1
    
    def bordes(self):
#en esta funcion se limitan los bordes del rect del enemigo, pero en el caso de que llegue hasta abajo de todo, va a
# aparecer en una posicion random de 0 a 600 en el eje x
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 600:
            self.rect.right = 600
        if self.rect.top <= 0:
            self.rect.y = 0
        if self.rect.bottom >= 650:
            self.rect.y = 0
            self.rect.x = random.randint(0,600)
    
    def update(self):
# se carga el movimiento y el limite de bordes del enemigo para su correcto funcionamiento en el main
        self.bordes()
        self.movimiento()        
        





    # def generar_asteroides(self,cantidad):
    #     lista_asteroides = []
    #     for i in range(cantidad):
    #         x = random.randrange(0,600,20)
    #         y = 0
    #         lista_asteroides.append(Enemigo(self.pantalla,x,y))
    #     return lista_asteroides
    
    
# def generar(self,x,y):
#     image = pygame.Surface((10,10))
#     image = pygame.image.load('enemigo1.png')
#     rect = self.image.get_rect()
#     rect.x = x
#     rect.y = y
#     dic_enemigo1 = {}
#     dic_enemigo1['imagen'] = image
#     dic_enemigo1['rect'] = rect
#     dic_enemigo1['visible'] = True
#     return dic_enemigo1



# 
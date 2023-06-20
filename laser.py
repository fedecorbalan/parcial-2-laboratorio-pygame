import pygame
from pygame.sprite import Group

class Laser(pygame.sprite.Sprite):
# se define la clase Laser, la cual hereda la clase Sprite del modulo pygame.sprite y se le pasa por parametro
# la posicion del rect en el centro, la velocidad(movimiento de pixeles) y el alto de la pantalla, que va a ser el borde
# hasta donde llega el laser
    def __init__(self,pos,velocidad,alto_pantalla):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image = pygame.image.load('laser.png')
        self.image = pygame.transform.scale(self.image,(35,50))
        self.rect = self.image.get_rect(center = pos)
        self.velocidad = velocidad
        self.altura_borde = alto_pantalla

    def destruir(self):
# si el laser sobrepasa el limite, se utiliza la funcion .kill, que elimina el sprite del grupo.
        if self.rect.y <= -50 or self.rect.y >= self.altura_borde + 50:
            self.kill()

    def update(self):
# el laser se va a mover a la velocidad que se le pase por parametro
        self.rect.y += self.velocidad


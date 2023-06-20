import pygame
from laser import Laser


class Jugador(pygame.sprite.Sprite):
# la clase jugador hereda la clase Sprite del modulo pygame.sprite y luego se inicializa con un super y se le ingresa
# por parametro a si mismo, la posicion su rect, el borde (limite) y la velocidad(pixeles que se mueve)
    def __init__(self,pos,borde,velocidad):
        super().__init__()
        self.image = pygame.image.load('nave.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.velocidad = velocidad
        self.maximo_borde = borde
        self.preparado = True
        self.tiempo_laser = 0
        self.cooldown = 300
        self.lasers = pygame.sprite.Group()
    
    def movimiento(self):
# se declara la variable keys que detecta las teclas presionadas y si se presiona la A ira hacia la derecha o a la izquierda
# si se presiona D. y cuando se presione la barra espacuadora, se dispara el laser 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.velocidad
        elif keys[pygame.K_a]:
            self.rect.x -= self.velocidad
            
        if keys[pygame.K_SPACE] and self.preparado:
            self.disparar_laser()
            self.preparado = False
            self.tiempo_laser = pygame.time.get_ticks()
            pygame.mixer_music.load('disparosfx.mp3')
            pygame.mixer_music.play()
            pygame.mixer_music.set_volume(5)

    def recarga(self):
# previamente se declara una flag llamada self.preparado que esta en true y en la variable tiempo actual, se almacena
# el tiempo transcurrido del juego, y si este restado al tiempo que pasa si se dispara el laser es menor o igual a 
# el cooldown del laser (600), se va a poder disparar
        if not self.preparado:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_laser >= self.cooldown:
                self.preparado = True

    def bordes(self):
# en esta funcion se limitan los bordes del rect del jugador
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.maximo_borde:
            self.rect.right = self.maximo_borde
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.maximo_borde:
            self.rect.bottom = self.maximo_borde
    
    def disparar_laser(self):
# Se utiliza la funcion .add de sprite.Group y se añade un laser al grupo(lista)
        self.lasers.add(Laser(self.rect.center,-10,self.rect.bottom))

    def update(self):
# se llaman a las funciones necesarias para que el objeto funcione correctamente
        self.movimiento()
        self.bordes()
        self.recarga()
        self.lasers.update()
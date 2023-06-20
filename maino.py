# Federico Corbalán 1-J
import pygame, sys
from pygame.locals import *
from personaje import Jugador 
from laser import Laser
from enemigo1 import Enemigo
import colores
import random
import sqlite3
from biblioteca import * 


class Juego:
# se define la clase juego, la cual contiene diversas funciones que se van a ir corriendo en el main
# 
    def __init__(self):
        # setup del jugador
        sprite_jugador = Jugador((ANCHO / 2,ALTO - 10), 600 ,5)
        self.jugador = pygame.sprite.GroupSingle(sprite_jugador)

        self.vidas = 3
        self.superficie_vidas = pygame.image.load('nave.png').convert_alpha()
        self.posicion_x_vidas = ANCHO - (self.superficie_vidas.get_size()[0] * 2 + 20)

        self.score = 0
        self.fuente = pygame.font.Font('C:\\Users\\User\\Documents\\programacion_I\\fuenteretro.ttf',20)

        self.game_over = False
        self.flag_input = False

        self.texto_usuario = ''

        self.ruta = 'C:\\Users\\User\\Documents\\programacion_I\\tabla_scores.db'

    def colisiones(self):
# si la bandera del game over se encuentra en false y si se disparo un laser, se entra a un for en el cual se verifica
# la colision del spirete del sprite con el asteroide.
# y luego a partir de la linea 48 se verifica la colision de los asteroides con la nave
        if self.game_over == False:
            if self.jugador.sprite.lasers:
                for laser in self.jugador.sprite.lasers:
                    if pygame.sprite.spritecollide(laser ,lista_asteroide, True):
                        laser.kill()
                        pygame.mixer_music.load('explosionsfx.mp3')
                        pygame.mixer_music.play()
                        pygame.mixer_music.set_volume(1)
                        self.score += 100
        
            if lista_asteroide:
                for asteroide in lista_asteroide:
                    if pygame.sprite.spritecollide(asteroide,juego.jugador,False):
                        asteroide.kill()
                        self.vidas -= 1
                        if self.vidas <= 0:
                            self.game_over = True
                            self.flag_input = True
                            if juego.score > 0:
                                guardar_score(juego.ruta,juego.texto_usuario,juego.score)
                                juego.texto_usuario = ''


    def display_vidas(self):
# se entra a un for en el rango de las vidas - 1 y en funcion de la cantidad de vidas se imprime una superficie que
# las representa
        for vida in range(self.vidas - 1):
            x = self.posicion_x_vidas + (vida * (self.superficie_vidas.get_size()[0] + 10))
            pantalla.blit(self.superficie_vidas,(x,8))

    def display_score(self):
# Se muestra en pantalla el score
        superficie_score = self.fuente.render('Score:{0}'.format(self.score),False,colores.GRAY69)
        rect_score = superficie_score.get_rect(topleft =(10,10))
        pantalla.blit(superficie_score,rect_score)
        
    def correr(self):
# esta funcion llama a las funciones que se quieren ejecutar en el while
        self.jugador.update()
        self.jugador.sprite.lasers.draw(pantalla)
        self.jugador.draw(pantalla)
        self.colisiones()
        self.display_vidas()
        self.display_score()
        

if __name__ == '__main__':
# cuando un archivo de Python se ejecuta directamente, es decir, se llama directamente desde la
# línea de comandos o se hace doble clic en él, la variable especial __name__ se establece en el valor '__main__'. 
# esto indica que el archivo se está ejecutando como el programa principal.
# Se inicializa pygame y el mixer, se crea el display, la base de datos, variables con imagenes y 
# se llama a los constructores
    pygame.init()
    pygame.mixer.init()
    ANCHO = 600
    ALTO = 600
    pantalla = pygame.display.set_mode((ANCHO,ALTO))
    pygame.display.set_caption('Galaxia')
    imagen_space = pygame.image.load('space fondo.jpg')
    imagen_space = pygame.transform.scale(imagen_space,(ANCHO,ALTO))

    reloj = pygame.time.Clock()
    juego = Juego()

    creacion_tabla_scores(juego.ruta)

    txt = juego.fuente.render('Click para Continuar', True,colores.WHITE)
    txt_ingreso_nombre = juego.fuente.render('Ingrese un nombre:',True,colores.WHITE)
    txt_x = (ANCHO // 2) - (txt.get_width() // 2)
    txt_y = 50

    input_usuario = pygame.Rect((ANCHO/2 - 100),110,200,40)

    background = pygame.image.load('fondomenu.jpg').convert_alpha()
    background = pygame.transform.scale(background,(ANCHO,ALTO))

    lista_asteroide = pygame.sprite.Group()

    musica = pygame.mixer.Sound('maintheme.wav')
    musica.set_volume(0.9)
    pygame.mixer.Sound.play(musica, -1)    

    flag_correr = True
    while flag_correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                # ingreso usuario
                if juego.flag_input == True:
                    if evento.key == K_BACKSPACE:
                        juego.texto_usuario = juego.texto_usuario[:-1]
                    else:
                        juego.texto_usuario += evento.unicode

        if juego.game_over == True:
            juego.flag_input = True
        # en el caso de game over, se va a remover el jugador de la pantalla y va 
        # a devolver a la pantalla en donde se ingresa el nombre del usuario y se muestran los scores
            juego.jugador.remove()
            pantalla.blit(background,background.get_rect())
            pantalla.blit(txt,(txt_x,txt_y))

            pantalla.blit(txt_ingreso_nombre,(input_usuario.x - 5,input_usuario.y - 25))
            pygame.draw.rect(pantalla,colores.WHITE,input_usuario,2)
            superficie_txt_usuario = juego.fuente.render(juego.texto_usuario,True,colores.WHITE)
            pantalla.blit(superficie_txt_usuario,(input_usuario.x + 5, input_usuario.y + 5))

            if evento.type == pygame.MOUSEBUTTONDOWN:
            # cuando se haga click en la panalla, se reinicia el juego, el score y las vidas y se generan 20
            # asteroides mas
                juego.score = 0
                juego.vidas = 3
                for i in range(20):
                    asteroide = Enemigo()
                    asteroide.rect.x = random.randrange(ANCHO)
                    asteroide.rect.y = random.randint(0,400)
                    lista_asteroide.add(asteroide)
                juego.game_over = False
                juego.flag_input = False

            lista_ranking = devolver_lista_scores(juego.ruta)
            for i in range(len(lista_ranking)):
            # se imprimen los rankings ya ordenados.
                texto = "{0}º {1}".format(i, lista_ranking[i]["nombre"])
                if i == 0:
                    color = colores.BLACK
                    tamaño = 24
                    texto = lista_ranking[i]["nombre"]
                else:
                    color = colores.WHITE
                    tamaño = 24 - i

                texto_nombre = juego.fuente.render(texto, True, color)
                pantalla.blit(texto_nombre,(150, 230+(i*30)))

                texto_tiempo = juego.fuente.render(str(lista_ranking[i]["score"]), True, color)
                pantalla.blit(texto_tiempo,(400, 230+(i*30)))
        else:
            # se corre el juego y si se rompen todos los asteroides, se pasa a game over y se dibujan 40 asteroides
                pantalla.blit(imagen_space, imagen_space.get_rect())
                lista_asteroide.draw(pantalla)    
                lista_asteroide.update()
                juego.correr()
                
                if len(lista_asteroide) == 0:
                    juego.game_over = True
                    for i in range(40):
                        asteroide = Enemigo()
                        asteroide.rect.x = random.randrange(ANCHO)
                        asteroide.rect.y = random.randint(0,400)
                        lista_asteroide.add(asteroide)
                    if juego.score > 0:
                        guardar_score(juego.ruta,juego.texto_usuario,juego.score)
                        juego.texto_usuario = ''
        # se muestran los cambios en el display y se limitan los fps a 60
        pygame.display.flip()
        reloj.tick(60)

# Galaxy✨
![image](https://github.com/fedecorbalan/parcial-2-laboratorio-pygame/assets/123754871/b490a399-f6b1-42ae-af8d-ade082e253f0)

## Alumno: Federico Corbalán, División 1-J

### Caracteristicas:
-La nave propia se mueve de izquierda a derecha o viceversa,
nunca hacia adelante y hacia atrás y dispara laseres.

-Se generan asteroides en posiciones aleatorias en el eje X

-Al final de cada partida se guarda el SCORE junto con el nombre
de usuario. 

-Se elabora un ranking ordenado de mayor a menor puntuación, mostrando su respectivo nombre y puntuación.

### Incluye:
⚪ Archivos.

⚪ POO.

⚪ Texto para ir mostrando el SCORE.

⚪ Eventos.

⚪ Colisiones.

⚪ Manejo de rectángulo.

⚪ Temporizador.

⚪ Imágenes.

⚪ Audios.

⚪ Ranking de puntuaciones

## Imagen del juego
![image](https://github.com/fedecorbalan/parcial-2-laboratorio-pygame/assets/123754871/75d571f3-acf7-4318-96a6-74290d2349e4)

## Codigo Principal
```python
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
                for i in range(25):
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

```
## Clase Jugador
```python
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
``` 
## Clase Asteroide
```python
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
```
## Clase Laser
```python
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
```
## Biblioteca
```python
import sqlite3

def creacion_tabla_scores(ruta):
    # se ingresa la ruta por parametro y se crea la tabla scores en el caso 
    # de que no exista y si existe, se imprime en la consola que ya existe esa tabla.
    with sqlite3.connect(ruta) as conexion:
        try:
            sentencia = ''' create table scores
            (
            id integer primary key autoincrement,
            nombre text,
            score integer
            )
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla scores")    

        except sqlite3.OperationalError:
            print("La tabla scores ya existe")

def devolver_lista_scores(ruta):
# se ingresa por parametro la ruta y se abre la base de datos, en donde se hace un select de los scores y se 
# ordena de mayor a menor, y luego se entra a un for en donde se crea un diccionario con las keys id, nombre y score
# y por ultimo, se agrega el dict a la lista y al final se retornan 10 elementos en la lista.
    with sqlite3.connect(ruta) as conexion:
        cursor = conexion.execute("SELECT * FROM scores ORDER BY score DESC")
        lista_ranking = [{"ID": 0, "nombre": "NOMBRE", "score": "SCORE"}]
        for fila in cursor:
            dict_jugador = {}
            dict_jugador["id"] = fila[0]
            dict_jugador["nombre"] = fila[1]
            dict_jugador["score"] = fila[2]
            lista_ranking.append(dict_jugador)
        return lista_ranking[0:11]

def guardar_score(ruta, nombre, score):
# se ingresa por parametro la ruta, el nombre y el score, y estos datos se insertan en la base de datos, en el 
# caso de que no sea asi, se imprimira un error en consola.
    with sqlite3.connect(ruta) as conexion:
            try:
                conexion.execute("INSERT INTO scores(nombre,score) VALUES (?,?)", (nombre, score))
                conexion.commit()
            except sqlite3.OperationalError as error:
                print(error)

```


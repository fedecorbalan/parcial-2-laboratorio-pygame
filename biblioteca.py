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

















# def insertar_elementos_a_lista(ruta,nombre,score):
#     with sqlite3.connect(ruta) as conexion:
#         try:
#             conexion.execute("INSERT INTO scores (nombre, score) VALUES (?,?)", (nombre,score))
#             conexion.commit()
#             print('datos insertados a la base')
#         except:
#             print('error1')

# def seleccionar_datos(ruta):
#     with sqlite3.connect(ruta) as conexion:
#         try:
#             respuesta = conexion.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 5")
#             datos_jugadores = respuesta.fetchall()
#             print('datos seleccionados')
#             return datos_jugadores
#         except:
#             print('error2')

# def mostrar_datos(fuente,datos:list,pantalla):
#     posicion_y = 300  # Posición vertical inicial para mostrar los datos
#     for i, (nombre, score) in enumerate(datos):
#         superficie_jugador = fuente.render(f'{nombre}: {score}', True, (255,255,255))
#         rect_jugador = superficie_jugador.get_rect(topleft=(100, posicion_y + i * 30))
#         pantalla.blit(superficie_jugador, rect_jugador)

# class Player:
#     def __init__(self,nombre,puntaje) -> None:
#         self._nombre = nombre
#         self._puntaje = puntaje

#     @property
#     def get_nombre(self):
#         return self._nombre
#     @property
#     def get_puntaje(self):
#         return self._puntaje
#     @property
    
#     def retornar_dic(self):
#         dic = {}
#         dic["nombre"] = self.get_nombre
#         dic["puntaje"] = self.get_puntaje
#         return dic
    






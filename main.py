# Importar la libreria para leer los archivos csv
import csv

##################################################################################################
# CLASES
##################################################################################################
# Estructura para el indice invertido
class NodoIndice:
    def __init__(self, numero_id):
        self.numero = numero_id
        self.next = None

# Nuevas clases de amigos (Lista de Adyacencia)
class FriendNode:
    def __init__(self, friend_id):
        self.friend_id = friend_id
        self.next = None

class FriendList:
    def __init__(self):
        self.head = None

    def insert(self, friend_id):
        nuevo_nodo = FriendNode(friend_id)
        if self.head is None:
            self.head = nuevo_nodo
        else:
            current = self.head
            while current is not None:
                if current.friend_id == friend_id:
                    return # Evita agregar amigos duplicados
                if current.next is None:
                    break
                current = current.next
            current.next = nuevo_nodo

    def print(self):
        current = self.head
        if current is None:
            print("No tiene amigos registrados.")
            return
        while current is not None:
            print(current.friend_id, end=" ")
            current = current.next
        print("")

# Clase usuario (lista enlazada simple)
class User:
    def __init__(self, number, friends, tweets, sentiment):
        self.number = number
        self.friends = friends # Ahora recibe una instancia de FriendList
        self.tweets = tweets
        self.sentiment = sentiment
        self.next = None

# Clase tweet (lista enlazada simple)
class Tweet:
    def __init__(self, number, description, posted_by, likes, liked_by):
        self.number = number
        self.description = description
        self.posted_by = posted_by
        self.likes = likes
        self.liked_by = liked_by
        self.next = None

# Lista de usuarios y sus funciones
class UserList:
    def __init__(self):
        self.head = None
        
    def print(self):
        current = self.head
        while current is not None:
            print(current.number, end=" ")
            current = current.next
        print("")
        
    def buscar(self, number):
        current = self.head
        while current is not None:
            if current.number == number:
                return 1
            current = current.next
        return 0

    # ver atributos del nodo
    def obtener_usuario(self, number):
        current = self.head
        while current is not None:
            if current.number == number:
                return current
            current = current.next
        return None

    def insert(self, user):
        if self.head is None:
            self.head = user
        else:
            existe = self.buscar(user.number)
            if existe == 0:
                current = self.head
                while current.next is not None:
                    current = current.next
                current.next = user
    # NUEVO!!! ENTREGA II
    def crearAmistad (self, idUser1, idUser2):
        user1 = self.obtener_usuario(idUser1)
        user2 = self.obtener_usuario(idUser2)

        # En caso de que los usuarios ingresados no existan
        if user1 is None or user2 is None:
            print ("Uno de los amigos especificados no existe")
            return
        
        if idUser1 == idUser2:
            print ("Un usuario no puede ser su propio amigo")
            return
        
        # En caso de que salga todo bien
        user1.friends.insert(idUser2)
        user2.friends.insert(idUser1)
        print("Amistad creada") # Mensaje de log para verificar que funcione
    
    def gradosSeparacion(self, root_id):
        # Se verifica que el usuario raiz exista
        root_user = self.obtener_usuario(root_id)
        if root_user is None:
            print ("El usuario ingresado no existe")
            return
        # Se inicializa la estructura auxiliar de BFS (cola)
        visitados = set()
        cola = []

        # Para separar los resultados
        resultados = {1:[], 2:[], 3:[]}
        
        # Caso base
        cola.append ((root_id, 0))
        visitados.add(root_id)

        # Ciclo BFS
        while len(cola) > 0:
            currentId, currentGrado = cola.pop(0)
            # Si es grado 1, 2 o 3 se añade en la respectiva lista
            if currentGrado > 0:
                resultados[currentGrado].append(currentId)
            
            # Si se esta procesando a uno de grado 3 se abandona el ciclo
            if currentGrado == 3:
                continue
            
            # Se recorren los amigos del usuario actual
            current_user = self.obtener_usuario(currentId)
            if current_user is not None and current_user.friends.head is not None:
                # Se recorre la friendlist de la entrega I
                amigoNodo = current_user.friends.head
                while amigoNodo is not None:
                    amigoId = amigoNodo.friend_id

                    # Si aun no se descrubre el amigo, se marca y se encola
                    if amigoId not in visitados:
                        visitados.add(amigoId)
                        cola.append((amigoId, currentGrado + 1))
                    amigoNodo = amigoNodo.next
        print(f"--- Red de contactos usuario {root_id} ---")
        print(f"1° Grado: {resultados[1]}")
        print(f"2° Grado: {resultados[2]}")
        print(f"3° Grado: {resultados[3]}")


# Lista de tweets y sus funciones
class TweetList:
    def __init__(self):
        self.head = None

    def print(self):
        current = self.head
        while current is not None:
            print(current.numero, end=" ") 
            current = current.next
        print("")

    def buscar(self, number):
        current = self.head
        while current is not None:
            if current.numero == number: 
                return 1
            current = current.next
        return 0
        
    def insert(self, number_id):
        nuevo_nodo = NodoIndice(number_id)
        if self.head is None:
            self.head = nuevo_nodo
        else:
            existe = self.buscar(number_id)
            if existe == 0:
                current = self.head
                while current.next is not None:
                    current = current.next
                current.next = nuevo_nodo

##################################################################################################
# FUNCIONES
##################################################################################################
# Funcion para borrar stopwords
def borrarStopwords(tweet):
    lista_stopwords = ["a", "in", "my"]
    tweet_sin_sw = ""

    # Para separar la frase por espacios y verificar que cada palabra no sea SW
    for palabra in tweet.split():
         if palabra not in lista_stopwords:
            tweet_sin_sw = tweet_sin_sw  + palabra + " "
    return tweet_sin_sw.strip() # .strip() elimina el espacio final sobrante

##################################################################################################
# CARGA Y PROCESAMIENTO DE DATOS
##################################################################################################
# Leer archivo y guardar sus datos en una lista
data_list = []
try:
    with open('tweet_sentiment.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data_list.append(row)
except FileNotFoundError:
    # Agrego este bloque para que no falle prueba si no esta el archivo a mano
    print("Aviso: 'tweet_sentiment.csv' no encontrado. Se usarán datos simulados para la prueba.\n")
    data_list = [
        {"tweet": "I hate bugs", "sentiment": "negative"},
        {"tweet": "found a raccoon in my house", "sentiment": "neutral"},
        {"tweet": "I hate traffic", "sentiment": "negative"},
        {"tweet": "I like python", "sentiment": "positive"},
        {"tweet": "hate late trains", "sentiment": "negative"},
        {"tweet": "another tweet to trigger user 2", "sentiment": "neutral"}
    ]

user_list = UserList()
user_number = 1
contador = 0

##################################################################################################
# INDICE INVERTIDO (ENTREGA I)
##################################################################################################
indiceInvertidoPalabras = {}

for data in data_list:
    # Modificado: Instanciamos la nueva clase de lista de amigos
    friend_list = FriendList()
    tweet_list = TweetList()
    
    tweet_original = str(data.get("tweet")).lower()
    sentiment = data.get("sentiment")
    
    tweet_limpio = borrarStopwords(tweet_original)
    palabras_sueltas = tweet_limpio.split()
    
    for palabra in palabras_sueltas:
        if palabra not in indiceInvertidoPalabras:
            nueva_lista = TweetList()
            nueva_lista.insert(user_number)
            indiceInvertidoPalabras[palabra] = nueva_lista
        else:
            lista_recuperada = indiceInvertidoPalabras[palabra]
            lista_recuperada.insert(user_number)
            
    user = User(user_number, friend_list, tweet_list, sentiment)
    user_list.insert(user)
    
    contador = contador + 1
    if contador >= 5:
        user_number = user_number + 1
        contador = 0

##################################################################################################
# PRUEBAS
##################################################################################################
while True:
    print("\n" + "="*50)
    print("--- MENÚ DE PRUEBAS - ESTRUCTURAS DE DATOS ---")
    print("="*50)
    print("1. Mostrar usuarios")
    print("2. Limpieza de stopwords")
    print("3. Busqueda palabra simple")
    print("4. Búsqueda de frase múltiple")
    print("5. Ver Grafo No Dirigido (Amigos del Usuario 1 y 2)")
    print("6. Ver Grados de Separación (BFS)")
    print("0. Salir")
    print("="*50)
    
    opcion = input("Elige una opción: ")

    if opcion == "1":
        print("\nLista de usuarios:")
        user_list.print()

    elif opcion == "2":
        tweet = "found a raccoon in my house"
        print(f"\nOriginal: {tweet}")
        print(f"Limpio:   {borrarStopwords(tweet)}")

    elif opcion == "3":
        palabraBuscada = input("\nPalabra a buscar (ej. hate): ").lower()
        if palabraBuscada in indiceInvertidoPalabras:
            print(f"La palabra '{palabraBuscada}' está en los siguientes IDs:")
            indiceInvertidoPalabras[palabraBuscada].print()
        else:
            print(f"La palabra '{palabraBuscada}' no se encontró.")

    elif opcion == "4":
        fraseBuscada = input("\nFrase a buscar (ej. sick of this): ")
        fraseLimpia = borrarStopwords(fraseBuscada.lower())
        palabrasSeparadas = fraseLimpia.split()

        if len(palabrasSeparadas) == 0:
            print("La búsqueda está vacía o solo contiene stopwords.")
        else:
            todasExisten = True
            for palabra in palabrasSeparadas:
                if palabra not in indiceInvertidoPalabras:
                    todasExisten = False
                    break
            
            if not todasExisten:
                print(f"No hay posts que contengan todas las palabras de: '{fraseBuscada}'")
            else:
                print(f"Los IDs que contienen todas las palabras son:")
                lista_base = indiceInvertidoPalabras[palabrasSeparadas[0]]
                current = lista_base.head
                encontrado_al_menos_uno = False
                
                while current is not None:
                    id_actual = current.numero
                    esta_en_todas = True
                    for i in range(1, len(palabrasSeparadas)):
                        if indiceInvertidoPalabras[palabrasSeparadas[i]].buscar(id_actual) == 0:
                            esta_en_todas = False
                            break
                    if esta_en_todas:
                        print(id_actual, end=" ")
                        encontrado_al_menos_uno = True
                    current = current.next
                
                if not encontrado_al_menos_uno:
                    print("Las palabras existen, pero no en un mismo post.")
                print("")

    elif opcion == "5":
        print("\n--- Prueba de Grafo no dirigido ---")
        user_list.crearAmistad(1,1)
        user_list.crearAmistad(1,2)
        user_list.crearAmistad(2,4)
        user_list.crearAmistad(4,5)
        user_list.crearAmistad(5,6)
        
        print("Amigos del usuario 1:")
        user1 = user_list.obtener_usuario(1)
        if user1: user1.friends.print()
        
        print("Amigos del usuario 2:")
        user2 = user_list.obtener_usuario(2)
        if user2: user2.friends.print()

    elif opcion == "6":
        print("\n--- Prueba Grados de separacion ---")
        # Nos aseguramos de tener la red creada antes del BFS
        user_list.crearAmistad(1,2)
        user_list.crearAmistad(2,4)
        user_list.crearAmistad(4,5)
        user_list.crearAmistad(5,6)
        
        id_raiz = int(input("Ingresa el ID del usuario raíz (ej. 1): "))
        user_list.gradosSeparacion(id_raiz)

    elif opcion == "0":
        print("\nSaliendo del programa...")
        break

    else:
        print("\nOpción inválida. Intenta nuevamente.")

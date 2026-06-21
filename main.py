# Importar la libreria para leer los archivos csv
import csv

##################################################################################################
# CLASES
##################################################################################################
# Estructura para el indice invertido
class NodoIndice:
    def __init__(self, numeroId):
        self.numero = numeroId
        self.next = None

# Nuevas clases de amigos (Lista de Adyacencia)
class FriendNode:
    def __init__(self, friendId):
        self.friendId = friendId
        self.next = None

class FriendList:
    def __init__(self):
        self.head = None

    def insert(self, friendId):
        nuevoNodo = FriendNode(friendId)
        if self.head is None:
            self.head = nuevoNodo
        else:
            current = self.head
            while current is not None:
                if current.friendId == friendId:
                    return # Evita agregar amigos duplicados
                if current.next is None:
                    break
                current = current.next
            current.next = nuevoNodo

    def print(self):
        current = self.head
        if current is None:
            print("No tiene amigos registrados.")
            return
        while current is not None:
            print(current.friendId, end=" ")
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
    def __init__(self, number, description, postedBy, likes, likedBy):
        self.number = number
        self.description = description
        self.postedBy = postedBy
        self.likes = likes
        self.likedBy = likedBy
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
    def obtenerUsuario(self, number):
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
        user1 = self.obtenerUsuario(idUser1)
        user2 = self.obtenerUsuario(idUser2)

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
    
    def gradosSeparacion(self, rootId):
        # Se verifica que el usuario raiz exista
        rootUser = self.obtenerUsuario(rootId)
        if rootUser is None:
            print ("El usuario ingresado no existe")
            return
        # Se inicializa la estructura auxiliar de BFS (cola)
        visitados = set()
        cola = []

        # Para separar los resultados
        resultados = {1:[], 2:[], 3:[]}
        
        # Caso base
        cola.append ((rootId, 0))
        visitados.add(rootId)

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
            currentUser = self.obtenerUsuario(currentId)
            if currentUser is not None and currentUser.friends.head is not None:
                # Se recorre la friendlist de la entrega I
                amigoNodo = currentUser.friends.head
                while amigoNodo is not None:
                    amigoId = amigoNodo.friendId

                    # Si aun no se descrubre el amigo, se marca y se encola
                    if amigoId not in visitados:
                        visitados.add(amigoId)
                        cola.append((amigoId, currentGrado + 1))
                    amigoNodo = amigoNodo.next
        print(f"--- Red de contactos usuario {rootId} ---")
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
        
    def insert(self, numberId):
        nuevoNodo = NodoIndice(numberId)
        if self.head is None:
            self.head = nuevoNodo
        else:
            existe = self.buscar(numberId)
            if existe == 0:
                current = self.head
                while current.next is not None:
                    current = current.next
                current.next = nuevoNodo

# NUEVO !!!! CLASE HASH
class TablaHashFrecuencias:
    def __init__(self, tamanoM):
        self.M = tamanoM
        # Creamos un arreglo vacío de tamaño M
        self.tabla = [None] * tamanoM 
        self.totalColisiones = 0 # Métrica requerida por la rúbrica

    def insertar(self, palabra):
        # 1. Calcular el índice en el arreglo
        indice = djb2(palabra) % self.M
        
        # 2. Si la casilla está vacía, se inserta el primer nodo
        if self.tabla[indice] is None:
            self.tabla[indice] = NodoFrecuencia(palabra)
            return

        # 3. Si hay colisión (ya existe algo ahí), recorremos la lista enlazada
        current = self.tabla[indice]
        
        while current is not None:
            # Si la palabra ya existe, solo aumentamos su frecuencia
            if current.palabra == palabra:
                current.frecuencia += 1
                return
            
            # Si llegamos al final de la lista encadenada sin hallarla, la insertamos
            if current.next is None:
                self.totalColisiones += 1 # Hubo un choque real
                current.next = NodoFrecuencia(palabra)
                return
                
            current = current.next
    
    def obtenerTopN(self, n):
        todosLosTerminos = []
        
        # Recorremos cada casilla del arreglo (de 0 a M-1)
        for i in range(self.M):
            current = self.tabla[i]
            # Si hay datos (y colisiones), recorremos la lista enlazada
            while current is not None:
                todosLosTerminos.append((current.palabra, current.frecuencia))
                current = current.next
                
        # Ordenamos la lista de tuplas por la frecuencia (el elemento 1), de mayor a menor
        todosLosTerminos.sort(key=lambda x: x[1], reverse=True)
        
        # Retornamos solo los primeros N elementos
        return todosLosTerminos[:n]


##################################################################################################
# FUNCIONES
##################################################################################################
# Funcion para borrar stopwords
def borrarStopwords(tweet):
    listaStopwords = ["a", "in", "my"]
    tweetSinSw = ""

    # Para separar la frase por espacios y verificar que cada palabra no sea SW
    for palabra in tweet.split():
         if palabra not in listaStopwords:
            tweetSinSw = tweetSinSw  + palabra + " "
    return tweetSinSw.strip() # .strip() elimina el espacio final sobrante

# NUEVO!!!! FUNCION HASH
def djb2(palabra):
    hashVal = 5381
    for char in palabra:
        # El & 0xFFFFFFFF es OBLIGATORIO en Python según el PDF para truncar a 32 bits
        hashVal = ((hashVal * 33) + ord(char)) & 0xFFFFFFFF
    return hashVal


# Nodo para la lista enlazada de colisiones (Encadenamiento separado)
class NodoFrecuencia:
    def __init__(self, palabra):
        self.palabra = palabra
        self.frecuencia = 1
        self.next = None


##################################################################################################
# CARGA Y PROCESAMIENTO DE DATOS
##################################################################################################
# Leer archivo y guardar sus datos en una lista
dataList = []
try:
    with open('tweet_sentiment.csv', mode='r', encoding='utf-8') as file:
        csvReader = csv.DictReader(file)
        for row in csvReader:
            dataList.append(row)
except FileNotFoundError:
    # Agrego este bloque para que no falle prueba si no esta el archivo a mano
    print("Aviso: 'tweet_sentiment.csv' no encontrado. Se usarán datos simulados para la prueba.\n")
    dataList = [
        {"tweet": "I hate bugs", "sentiment": "negative"},
        {"tweet": "found a raccoon in my house", "sentiment": "neutral"},
        {"tweet": "I hate traffic", "sentiment": "negative"},
        {"tweet": "I like python", "sentiment": "positive"},
        {"tweet": "hate late trains", "sentiment": "negative"},
        {"tweet": "another tweet to trigger user 2", "sentiment": "neutral"}
    ]

userList = UserList()
userNumber = 1
contador = 0

##################################################################################################
# INDICE INVERTIDO (ENTREGA I)
##################################################################################################
indiceInvertidoPalabras = {}
tablaFrecuencias = TablaHashFrecuencias(97)

for data in dataList:
    # Modificado: Instanciamos la nueva clase de lista de amigos
    friendList = FriendList()
    tweetList = TweetList()
    tweetOriginal = str(data.get("tweet")).lower()
    sentiment = data.get("sentiment")
    
    tweetLimpio = borrarStopwords(tweetOriginal)
    palabrasSueltas = tweetLimpio.split()
    
    for palabra in palabrasSueltas:
        tablaFrecuencias.insertar(palabra)
        if palabra not in indiceInvertidoPalabras:
            nuevaLista = TweetList()
            nuevaLista.insert(userNumber)
            indiceInvertidoPalabras[palabra] = nuevaLista
        else:
            listaRecuperada = indiceInvertidoPalabras[palabra]
            listaRecuperada.insert(userNumber)
            
    user = User(userNumber, friendList, tweetList, sentiment)
    userList.insert(user)
    
    contador = contador + 1
    if contador >= 5:
        userNumber = userNumber + 1
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
    print("7. Ver Estadísticas de Tabla Hash (Top N)")
    print("0. Salir")
    print("="*50)
    
    opcion = input("Elige una opción: ")

    if opcion == "1":
        print("\nLista de usuarios:")
        userList.print()

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
                listaBase = indiceInvertidoPalabras[palabrasSeparadas[0]]
                current = listaBase.head
                encontradoAlMenosUno = False
                
                while current is not None:
                    idActual = current.numero
                    estaEnTodas = True
                    for i in range(1, len(palabrasSeparadas)):
                        if indiceInvertidoPalabras[palabrasSeparadas[i]].buscar(idActual) == 0:
                            estaEnTodas = False
                            break
                    if estaEnTodas:
                        print(idActual, end=" ")
                        encontradoAlMenosUno = True
                    current = current.next
                
                if not encontradoAlMenosUno:
                    print("Las palabras existen, pero no en un mismo post.")
                print("")

    elif opcion == "5":
        print("\n--- Prueba de Grafo no dirigido ---")
        userList.crearAmistad(1,1)
        userList.crearAmistad(1,2)
        userList.crearAmistad(2,4)
        userList.crearAmistad(4,5)
        userList.crearAmistad(5,6)
        
        print("Amigos del usuario 1:")
        user1 = userList.obtenerUsuario(1)
        if user1: user1.friends.print()
        
        print("Amigos del usuario 2:")
        user2 = userList.obtenerUsuario(2)
        if user2: user2.friends.print()

    elif opcion == "6":
        print("\n--- Prueba Grados de separacion ---")
        # Nos aseguramos de tener la red creada antes del BFS
        userList.crearAmistad(1,2)
        userList.crearAmistad(2,4)
        userList.crearAmistad(4,5)
        userList.crearAmistad(5,6)
        
        idRaiz = int(input("Ingresa el ID del usuario raíz (ej. 1): "))
        userList.gradosSeparacion(idRaiz)

    elif opcion == "7":
        print("\n--- Estadísticas de la Tabla Hash (Entrega III) ---")
        topN = int(input("Indique cantidad de palabras frecuentes (Ej. 5): "))
        
        resultadosTop = tablaFrecuencias.obtenerTopN(topN)
        print(f"\nTop {topN} palabras más usadas:")
        for posicion, (palabra, frecuencia) in enumerate(resultadosTop, start=1):
            print(f"{posicion}. '{palabra}' (Aparece {frecuencia} veces)")
            
        print("\n--- Métricas Técnicas ---")
        print(f"Tamaño del Vocabulario (N): {len(indiceInvertidoPalabras)}")
        print(f"Tamaño de la Tabla Hash (M): {tablaFrecuencias.M}")
        print(f"Total de Colisiones detectadas: {tablaFrecuencias.totalColisiones}")

    elif opcion == "0":
        print("\nSaliendo del programa...")
        break

    else:
        print("\nOpción inválida. Intenta nuevamente.")

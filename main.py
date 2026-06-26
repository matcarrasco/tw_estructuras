# Importar la libreria para leer los archivos csv
import csv

# CLASES

# Nodo generico
class NodoIndice:
    def __init__(self, numero_id):
        self.numero = numero_id
        self.next = None

# Nodo amigo
class FriendNode:
    def __init__(self, friend_id):
        self.friend_id = friend_id
        self.next = None

# Funciones para lista de amigos
class FriendList:    
    # Inicializar lista
    def __init__(self):
        self.head = None
    
    # Insertar amigo al final de la lista
    def insert(self, friend_id):
        nuevo_nodo = FriendNode(friend_id)
        if self.head is None:
            self.head = nuevo_nodo
        else:
            current = self.head
            # Recorrer lista hasta el final
            while current is not None:
                # Evita agregar amigos duplicados
                if current.friend_id == friend_id:
                    return
                # Si no tiene siguiente, es el ultimo nodo de la lista
                # entonces terminamos el ciclo
                if current.next is None:
                    break
                current = current.next
            # Agregar nodo al final de la lista
            current.next = nuevo_nodo
    
    # Mostrar lista de amigos
    def print(self):
        current = self.head
        if current is None:
            print("No tiene amigos registrados.")
            return
        while current is not None:
            print(current.friend_id, end=" ")
            current = current.next
        print("")

# Nodo usuario
class User:
    # Inicializar nodo, friends y tweets son listas
    def __init__(self, number, friends, tweets, sentiment):
        self.number = number
        self.friends = friends 
        self.tweets = tweets
        self.sentiment = sentiment
        self.next = None

# Funciones para lista de usuarios
class UserList:
    # Inicializar
    def __init__(self):
        self.head = None
    
    # Mostrar lista de usuarios
    def print(self):
        current = self.head
        while current is not None:
            print(current.number, end=" ")
            current = current.next
        print("")
    
    # Buscar si existe un usuario por numero
    def buscar(self, number):
        current = self.head
        while current is not None:
            if current.number == number:
                return 1
            current = current.next
        return 0
    
    # Obtener usuario por numero
    def obtener_usuario(self, number):
        current = self.head
        while current is not None:
            if current.number == number:
                return current
            current = current.next
        return None
    
    # Insertar un usuario a la lista de usuarios
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
    
    # ENTREGA II
    
    # Crear amigo de usuario en la lista de usuarios
    def crearAmistad (self, idUser1, idUser2):
        # Buscar usuarios por id
        user1 = self.obtener_usuario(idUser1)
        user2 = self.obtener_usuario(idUser2)
        # Verificar que ambos usuarios existan
        if user1 is None or user2 is None:
            print ("Uno de los amigos especificados no existe")
            return
        # Verificar que ambos usuarios no sean el mismo
        if idUser1 == idUser2:
            print ("Un usuario no puede ser su propio amigo")
            return
        # Agregar a la lista de amigos de ambos usuarios
        user1.friends.insert(idUser2)
        user2.friends.insert(idUser1)
        print("Amistad creada")
    
    # Mostrar lista de amigos de un usuario hasta 3er grado
    def gradosSeparacion(self, root_id):
        # Verificar que el usuario raiz exista
        root_user = self.obtener_usuario(root_id)
        # Si no existe
        if root_user is None:
            print ("El usuario ingresado no existe")
            return
        # Inicializar algoritmo BFS con cola
        visitados = set()
        cola = []
        # Para separar los resultados
        resultados = {1:[], 2:[], 3:[]}
        # Nodo raiz es el usuario del que buscamos sus amistades
        cola.append((root_id, 0))
        visitados.add(root_id)
        # Ciclo BFS - Recorrer mientras hayan elementos en la cola
        while len(cola) > 0:
            currentId, currentGrado = cola.pop(0)
            # Si es de grado 1 o 2 se añade a la lista de resultados
            if currentGrado > 0:
                resultados[currentGrado].append(currentId)
            # Si es de grado 3 se abandona el ciclo
            if currentGrado == 3:
                continue
            # Se traen los datos del usuario
            current_user = self.obtener_usuario(currentId)  
            # Si el usuario existe y la lista de amigos no está vacía
            if current_user is not None and current_user.friends.head is not None:
                amigoNodo = current_user.friends.head       
                # Se recorre la lista de amigos hasta el final
                while amigoNodo is not None:
                    amigoId = amigoNodo.friend_id
                    # Si aun no se descubre el amigo, se marca y se encola
                    if amigoId not in visitados:
                        visitados.add(amigoId)
                        cola.append((amigoId, currentGrado + 1))
                    amigoNodo = amigoNodo.next
        print(f"--- Red de contactos usuario {root_id} ---")
        print(f"1° Grado: {resultados[1]}")
        print(f"2° Grado: {resultados[2]}")
        print(f"3° Grado: {resultados[3]}")

# Nodo tweet
class Tweet:
    def __init__(self, number, description, posted_by, likes, liked_by):
        self.number = number
        self.description = description
        self.posted_by = posted_by
        self.likes = likes
        self.liked_by = liked_by
        self.next = None

# Lista de tweets y sus funciones
class TweetList:
    def __init__(self):
        self.head = None
    
    # Mostrar tweets
    def print(self):
        current = self.head
        while current is not None:
            print(current.numero, end=" ") 
            current = current.next
        print("")
    
    # Verificar si existe el tweet
    def buscar(self, number):
        current = self.head
        while current is not None:
            if current.numero == number: 
                return 1
            current = current.next
        return 0
    
    # Insertar un tweet a la lista de tweets
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

# Nodo para la lista enlazada de colisiones
class NodoFrecuencia:
    def __init__(self, palabra):
        self.palabra = palabra
        self.frecuencia = 1
        self.next = None

# NUEVO !!!! CLASE HASH
class ListaFrecuencias:
    # Inicializar lista de frecuencias de cada palabra
    def __init__(self):
        # M sera el menor numero primo que cumpla con M > 1,5 * N
        self.M = 97
        # Creamos un arreglo vacío de tamaño M
        self.tabla = [None] * 97
        # Total de colisiones
        self.totalColisiones = 0 

    # Agregar frecuencia a la palabra de la lista usando hashing
    def insertar(self, palabra):
        # 1. Calcular el índice en el arreglo
        indice = djb2(palabra) % self.M

        # 2. Si la casilla está vacía, se inserta el primer nodo
        if self.tabla[indice] is None:
            self.tabla[indice] = NodoFrecuencia(palabra)
            return
        else:
            # 3. Si hay colisión (ya existe algo ahí), acumulamos colisiones y recorremos la lista enlazada
            self.totalColisiones = self.totalColisiones + 1
            current = self.tabla[indice]
            
            # Recorrer hasta el final de la lista
            while current is not None:
                # Si la palabra existe en la lista, aumentamos su frecuencia
                if current.palabra == palabra:
                    current.frecuencia = current.frecuencia + 1
                    return
                # Si estamos al final de la lista, insertamos la frecuencia
                if current.next is None:
                    current.next = NodoFrecuencia(palabra)
                    return
                current = current.next
    
    # Crear un top de tamaño n de frecuencias de palabras
    def obtenerTopN(self, n):
        # Sacar las palabras y frecuencias de la tabla hash y ponerlas en una lista
        listaFrecuencias = []       
        # Recorremos cada elemento de la tabla
        for i in range(self.M):
            nodoActual = self.tabla[i]   
            # Si hay palabras ahí (incluyendo las colisiones), las recorremos
            while nodoActual is not None:
                # Guardamos un pequeño arreglo con la palabra y su numero de repeticiones
                datos = [nodoActual.palabra, nodoActual.frecuencia]
                listaFrecuencias.append(datos)   
                # Pasamos al siguiente nodo en caso de que hayan chocado
                nodoActual = nodoActual.next
        # Ordenar de mayor a menor
        cantidadDePalabras = len(listaFrecuencias)  
        # Un ciclo para recorrer palabras
        for i in range(cantidadDePalabras):
            # Otro ciclo para comparar a un elemento con el siguiente
            for j in range(cantidadDePalabras - 1):
                frecuenciaActual = listaFrecuencias[j][1]
                frecuenciaSiguiente = listaFrecuencias[j + 1][1]
                
                # Si el actual es menor que el de la derecha, los intercambiamos
                if frecuenciaActual < frecuenciaSiguiente:
                    
                    # Intercambio usando una variable auxiliar
                    auxiliar = listaFrecuencias[j]
                    listaFrecuencias[j] = listaFrecuencias[j + 1]
                    listaFrecuencias[j + 1] = auxiliar
                    
        # Sacar solo las primeras N palabras pedidas
        resultadosTop = []

        # Validamos que no nos pidan más palabras de las que existen en total
        if n > cantidadDePalabras:
            n = cantidadDePalabras

        # Llenamos el top n
        for i in range(n):
            resultadosTop.append(listaFrecuencias[i])
            
        return resultadosTop

# FUNCIONES GLOBALES

# Funcion para borrar stopwords
def borrarStopwords(tweet):
    
    # Lista de stopwords
    lista_stopwords = ["a", "in", "my"]
    tweet_sin_sw = ""
    
    # Por cada palabra en el tweet
    for palabra in tweet.split():
        
        # Si la palabra no es SW, se acumula en tweet_sin_sw
        if palabra not in lista_stopwords:
            tweet_sin_sw = tweet_sin_sw  + palabra + " "
    
    # Devolver eliminando el espacio final sobrante
    return tweet_sin_sw.strip() 

# NUEVO!!!! FUNCION HASH
def djb2(palabra: str) -> int:
    hash_value = 5381
    for char in palabra:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value & 0xFFFFFFFF

# CARGA Y PROCESAMIENTO DE DATOS

# Leer archivo y guardar sus datos en una lista
data_list = []
try:
    # Abrir el archivo tweet_sentiment.csv y guardar datos en data_list
    with open('tweet_sentiment.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data_list.append(row)
except FileNotFoundError:
    # Si no existe el archivo
    print("Aviso: 'tweet_sentiment.csv' no encontrado. Se usarán datos simulados para la prueba.\n")
    data_list = [
        {"tweet": "I hate bugs", "sentiment": "negative"},
        {"tweet": "found a raccoon in my house", "sentiment": "neutral"},
        {"tweet": "I hate traffic", "sentiment": "negative"},
        {"tweet": "I like python", "sentiment": "positive"},
        {"tweet": "hate late trains", "sentiment": "negative"},
        {"tweet": "another tweet to trigger user 2", "sentiment": "neutral"}
    ]
# Crear una lista de Usuarios
user_list = UserList()
user_number = 1
contador = 0

# INDICE INVERTIDO (ENTREGA I)

# Lista de palabras
indiceInvertidoPalabras = {}
listaFrecuencias = ListaFrecuencias()
listaFrecuenciasUnica = ListaFrecuencias()

# Recorrer datos del archivo
for data in data_list:
    # Creamos lista de amigos y lista de tweets
    friend_list = FriendList()
    tweet_list = TweetList()
    # El tweet queda en minuscula
    tweet_original = str(data.get("tweet")).lower()
    # Obtener el sentimiento del tweet
    sentiment = data.get("sentiment")
    # Eliminar las SW del tweet
    tweet_limpio = borrarStopwords(tweet_original)
    # Eliminar el espacio al final del tweet
    palabras_sueltas = tweet_limpio.split()
    # Recorrer palabras en el tweet
    for palabra in palabras_sueltas:
        # Hashing
        listaFrecuencias.insertar(palabra)

        # Si la palabra no existe en el indice
        # Se agrega al final de la lista de tweets y de una lista de palabras
        if palabra not in indiceInvertidoPalabras:
            nueva_lista = TweetList()
            nueva_lista.insert(user_number)
            indiceInvertidoPalabras[palabra] = nueva_lista
        else:
            # Si existe en el indice, pasar
            lista_recuperada = indiceInvertidoPalabras[palabra]
            lista_recuperada.insert(user_number)
    # Crear usuario e insertar al final de la lista de usuarios          
    user = User(user_number, friend_list, tweet_list, sentiment)
    user_list.insert(user)
    # Cada 5 tweets cambiamos el id del usuario
    contador = contador + 1
    if contador >= 5:
        user_number = user_number + 1
        contador = 0

for palabra in indiceInvertidoPalabras:
    listaFrecuenciasUnica.insertar(palabra)

# PRUEBAS
# Menu principal
while True:
    print("--- MENÚ DE PRUEBAS - ESTRUCTURAS DE DATOS ---")
    print("1. Mostrar usuarios")
    print("2. Limpieza de stopwords")
    print("3. Busqueda palabra simple")
    print("4. Búsqueda de frase múltiple")
    print("5. Ver Grafo No Dirigido (Amigos del Usuario 1 y 2)")
    print("6. Ver Grados de Separación (BFS)")
    print("7. Ver Estadísticas de Tabla Hash (Top N)")
    print("0. Salir")
    print("")
    
    # Pedir opcion a usuario
    opcion = input("Elige una opción: ")
    
    # Mostrar lista de usuarios
    if opcion == "1":
        print("\nLista de usuarios:")
        user_list.print()
    
    # Limpiar las SW de un tweet
    elif opcion == "2":
        tweet = "found a raccoon in my house"
        print(f"\nOriginal: {tweet}")
        print(f"Limpio:   {borrarStopwords(tweet)}")
    
    # Buscar una palabra en la lista de palabras
    elif opcion == "3":
        palabraBuscada = input("\nPalabra a buscar (ej. hate): ").lower()
        if palabraBuscada in indiceInvertidoPalabras:
            print(f"La palabra '{palabraBuscada}' está en los siguientes IDs:")
            indiceInvertidoPalabras[palabraBuscada].print()
        else:
            print(f"La palabra '{palabraBuscada}' no se encontró.")
    
    # Buscar mas de una palabra en la lista de palabras
    elif opcion == "4":
        fraseBuscada = input("\nFrase a buscar (ej. sick of this): ")
        # Eliminamos stopwords de la palabra ingresada del usuario
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
    
    # Crear y mostrar amistades de dos usuarios
    elif opcion == "5":
        print("\n--- Prueba de Grafo no dirigido ---")
        user_list.crearAmistad(1,1)
        user_list.crearAmistad(1,2)
        user_list.crearAmistad(2,4)
        user_list.crearAmistad(4,5)
        user_list.crearAmistad(5,6)
        # Mostrar todas las amistades del usuario 1
        print("Amigos del usuario 1:")
        user1 = user_list.obtener_usuario(1)
        if user1: user1.friends.print()
        # Mostrar todas las amistades del usuario 2
        print("Amigos del usuario 2:")
        user2 = user_list.obtener_usuario(2)
        if user2: user2.friends.print()
    
    # Crear y mostrar amistades de un usuario, hasta tercer nivel
    elif opcion == "6":
        print("\n--- Prueba Grados de separacion ---")
        # Creamos amistades
        user_list.crearAmistad(1,2)
        user_list.crearAmistad(2,4)
        user_list.crearAmistad(4,5)
        user_list.crearAmistad(5,6)
        # Se pide el id de un usuario
        id_raiz = int(input("Ingresa el ID del usuario raíz (ej. 1): "))
        # Función que muestra las amistades del usuario hasta tercer grado
        user_list.gradosSeparacion(id_raiz)
    
    # Crear un top n de frecuencias de palabras en la lista de tweets
    elif opcion == "7":
        # Pedir n a usuario
        print("\n--- Estadísticas de la Tabla Hash (Entrega III) ---")
        topN = int(input("Indique N para top N (Ej. 5): "))  
        
        # Se obtiene el top n de palabras más frecuentes
        # Y se guarda en resultadosTop
        resultadosTop = listaFrecuencias.obtenerTopN(topN)
        print(f"\nTop {topN} palabras más usadas:")
        posicion = 1
        
        # Recorrer datos dentro de la lista resultadosTop
        for i in range(topN):
            print(f"{posicion}. '{resultadosTop[i][0]}' (Aparece {resultadosTop[i][1]} veces)")
            posicion = posicion + 1

        # Métricas de la lista de frecuencia
        print("\n--- Métricas Técnicas ---")
        print(f"Tamaño del Vocabulario (N): {len(indiceInvertidoPalabras)}")
        print(f"Tamaño de la Tabla Hash (M): {listaFrecuenciasUnica.M}")
        print(f"Total de Colisiones detectadas dataset: {listaFrecuencias.totalColisiones}")
        print(f"Total de Colisiones detectadas indice invertido: {listaFrecuenciasUnica.totalColisiones}")

    # Terminar ejecución del programa
    elif opcion == "0":
        print("\nSaliendo del programa...")
        break
    # Numero no valido para el menu
    else:
        print("\nOpción inválida. Intenta nuevamente.")
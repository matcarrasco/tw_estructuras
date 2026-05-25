# Importar la libreria para leer los archivos csv
import csv

# Estructura para el indice invertido
class NodoIndice:
    def __init__(self, numero_id):
        self.numero = numero_id
        self.next = None
        
# Función para borrar stopwords
def borrarStopwords(tweet):
    lista_stopwords = ["a", "in", "my"]
    tweet_sin_sw = ""

    # Para separar la frase por espacios y verificar que cada palabra no sea SW
    for palabra in tweet.split():
         if palabra not in lista_stopwords:
            tweet_sin_sw = tweet_sin_sw  + palabra + " "
    return tweet_sin_sw.strip() # .strip() elimina el espacio final sobrante

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

# Indice Invertido
indice_invertido_palabras = {}

for data in data_list:
    # Modificado: Instanciamos la nueva clase de lista de amigos
    friend_list = FriendList()
    tweet_list = TweetList()
    
    tweet_original = str(data.get("tweet")).lower()
    sentiment = data.get("sentiment")
    
    tweet_limpio = borrarStopwords(tweet_original)
    palabras_sueltas = tweet_limpio.split()
    
    for palabra in palabras_sueltas:
        if palabra not in indice_invertido_palabras:
            nueva_lista = TweetList()
            nueva_lista.insert(user_number)
            indice_invertido_palabras[palabra] = nueva_lista
        else:
            lista_recuperada = indice_invertido_palabras[palabra]
            lista_recuperada.insert(user_number)
            
    user = User(user_number, friend_list, tweet_list, sentiment)
    user_list.insert(user)
    
    contador = contador + 1
    if contador >= 5:
        user_number = user_number + 1
        contador = 0

### Pruebas ###
# Recorrer lista de usuarios
print("Lista de usuarios: ")
print("")
user_list.print()

# Borrar stopwords de un tweet
tweet = "found a raccoon in my house"
tweet = borrarStopwords(tweet)
print(tweet)

print("Busqueda")
# Palabra para buscar en el indice invertido
palabra_buscada = "hate"

if palabra_buscada in indice_invertido_palabras:
    print(f"La palabra '{palabra_buscada}' está en los siguientes IDs")
    indice_invertido_palabras[palabra_buscada].print()
else:
    print(f"La palabra '{palabra_buscada}' no se encontró en ningún post.")

# Agregar y Buscar Amigos
id_a_buscar = 1
usuario_encontrado = user_list.obtener_usuario(id_a_buscar)

if usuario_encontrado is not None:
    print(f"Usuario {id_a_buscar} encontrado exitosamente en la lista enlazada.")
    
    # Simulamos que le agregamos amigos (los ID de otros usuarios)
    print(f"Añadiendo amigos al Usuario {id_a_buscar}...")
    usuario_encontrado.friends.insert(2)
    usuario_encontrado.friends.insert(5)
    usuario_encontrado.friends.insert(10)
    
    print(f"IDs de los amigos del Usuario {id_a_buscar}:")
    usuario_encontrado.friends.print()
else:
    print(f"Error: El usuario {id_a_buscar} no se encontró en la base de datos.")

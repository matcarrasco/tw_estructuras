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
    return tweet_sin_sw

# Clase usuario - lista enlazada simple
class User:
    def __init__(self, number, friends, tweets, sentiment):
        self.number = number
        self.friends = friends
        self.tweets = tweets
        self.sentiment = sentiment
        self.next = None

# Clase tweet - lista enlazada simple
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
    # Funcion para recorrer la lista
    def print(self):
        current = self.head
        while current is not None:
            print(current.number, end=" ")
            print("")
            current = current.next
    # Funcion para evitar duplicidad de usuarios
    def buscar(self, number):
        current = self.head
        while current is not None:
            if current.number == number:
                return 1
            current = current.next
        return 0

    # Agregar usuario al final de la lista
    def insert(self, user):
        # Si la lista está vacia
        if self.head is None:
            self.head = user
        else:
            #Si no existe en la lista
            existe = self.buscar(user.number)
            if existe == 0:
                # Si no existe en la lista, agregar al final
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
            print("")
            current = current.next

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
with open('tweet_sentiment.csv', mode='r') as file:
    # Crear diccionario con la libreria csv
    csv_reader = csv.DictReader(file)
    # Inicializar lista de datos
    data_list = []
    # Cada fila se agregará en la lista de datos data_list
    for row in csv_reader:
        data_list.append(row)

user_list = UserList()
user_number = 1
contador = 0

# Indice Invertido
indice_invertido_palabras = {}
#Por cada 5 tweets en el data_list crear un usuario
for data in data_list:
    friend_list = UserList()
    tweet_list = TweetList()
    # Extraccion de datos
    tweet_original = str(data.get("tweet")).lower()
    sentiment = data.get("sentiment")
    # Filtrado de palabras SW
    tweet_limpio = borrarStopwords(tweet_original)
    palabras_sueltas = tweet_limpio.split()
    # Construccion del indice
    for palabra in palabras_sueltas:
        # Si la palabra no existe en el indice
        if palabra not in indice_invertido_palabras:
            nueva_lista = TweetList()
            nueva_lista.insert(user_number)
            indice_invertido_palabras[palabra] = nueva_lista
        # Si la palabra ya existe en el indice
        else:
            lista_recuperada = indice_invertido_palabras [palabra]
            lista_recuperada.insert (user_number)
    # Se crea el usuario con su informacion y listas vacias asociadas
    user = User(user_number, friend_list, tweet_list, sentiment)
    user_list.insert(user)
    contador = contador + 1
    # Cada 5 tweets se pasa al siguiente usuario
    if contador >= 5:
        # Siguiente usuario
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
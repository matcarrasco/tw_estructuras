# Importar la libreria para leer los archivos csv
import csv

# Función para borrar stopwords
def borrarStopwords(tweet):
    lista_stopwords = ["a", "in", "my"]
    tweet_sin_sw = ""

    for palabra in tweet.split():
         if palabra not in lista_stopwords:
            tweet_sin_sw = tweet_sin_sw  + palabra + " "
    return tweet_sin_sw

# Clase usuario - lista enlazada simple
class User:
    def __init__(self, number, friends, tweets, sentiment):
        self.number = number
        self.friends = friends
        self.tweet = tweet
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

    def print(self):
        current = self.head
        while current is not None:
            print(current.number, end=" ")
            print("")
            current = current.next

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

# Lista de usuarios y sus funciones
class TweetList:
    def __init__(self):
        self.head = None

    def print(self):
        current = self.head
        while current is not None:
            print(current.number, end=" ")
            print("")
            current = current.next

    def buscar(self, number):
        current = self.head
        while current is not None:
            if current.number == number:
                return 1
            current = current.next
        return 0

    # Buscar en todos los tweets una lista de palabras (PENDIENTE)
    def buscarTweets(self, lista_palabras):
        lista_tweets_encontrados = []
        current = self.head
        # Recorrer tweets
        while current is not None:
            # Borramos las stopwords del tweet actual
            current_tweet_description = borrarStopwords(current.description)
            # Recorremos cada palabra del tweet
            for palabra in tweet.split():
                # En caso de encontrar en el tweet la palabra buscada, agregamos su numero a la lista de tweets encontrados
                if lista_palabras in current_tweet_description:
                    # Verificar que el numero no se encuentre repetido en nuestra lista_tweets_encontrados
                    lista_tweets_encontrados = lista_tweets_encontrados.append(current.number)
            current = current.next
        return lista_tweets_encontrados

    # Agregar usuario al final de la lista
    def insert(self, tweet):
        # Si la lista está vacia
        if self.head is None:
            self.head = tweet
        else:
            #Si no existe en la lista
            existe = self.buscar(tweet.number)
            if existe == 0:
                # Si no existe en la lista, agregar al final
                current = self.head
                while current.next is not None:
                    current = current.next
                current.next = tweet

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
#Por cada 5 tweets en el data_list crear un usuario
for data in data_list:
    friend_list = UserList()
    tweet_list = TweetList()
    tweet = data.get("tweet")
    sentiment = data.get("sentiment")
    user = User(user_number, friend_list, tweet_list, sentiment)
    user_list.insert(user)
    contador = contador + 1
    if contador >= 5:
        # Siguiente usuario
        user_number = user_number + 1
        contador = 0

# Recorrer lista de usuarios
print("Lista de usuarios: ")
print("")
user_list.print()

# Borrar stopwords de un tweet
tweet = "found a raccoon in my house"
tweet = borrarStopwords(tweet)
print(tweet)
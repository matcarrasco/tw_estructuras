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

# Clase usuario para nuestra lista enlazada simple
class User:
    def __init__(self, number, tweet, sentiment):
        self.number = number
        self.tweet = tweet
        self.sentiment = sentiment
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
    tweet = data.get("tweet")
    sentiment = data.get("sentiment")
    user = User(user_number, tweet, sentiment)
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





















"""
class User:
    def __init__(self, number, friends, tweets, sentiment):
        self.number = number
        self.friends = friends
        self.tweet = tweet
        self.sentiment = sentiment
        self.next = None


class Tweet:
    def __init__(self, description, posted_by, likes, liked_by):
        self.description = description
        self.posted_by = posted_by
        self.likes = likes
        self.liked_by = liked_by
        self.next = None

# recorrer texto del tweet

"""

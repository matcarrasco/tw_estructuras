# Importar la libreria para leer los archivos csv
import csv

# Creamos la clase usuario para nuestra lista enlazada simple
class User:
    def __init__(self, number, tweet, sentiment):
        self.number = number
        self.tweet = tweet
        self.sentiment = sentiment
        self.next = None

"""
class User:
    def __init__(self, number, friends, tweets, sentiment):
        self.number = number
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

# borrar stopwords
stopwords = [a, and, of, his, hers, my, when, there, is, are, so, or, it, for]

# recorrer texto del tweet
for palabra in tweet:
    # si la palabra no es parte de la lista de stopwords se agrega a la descripcion o cuerpo del tweet
    if stopwords not in palabra:
        tweet_sin_stopwords = tweet_sin_stopwords.append(palabra)

"""

# Leer archivo y guardar sus datos en una lista
with open('tweet_sentiment.csv', mode='r') as file:
    # Crear diccionario con la libreria csv
    csv_reader = csv.DictReader(file)
    # Inicializar lista de datos
    data_list = []
    # Cada fila se agregará a la lista de datos
    for row in csv_reader:
        data_list.append(row)

# Crear lista de usuarios con los datos de los nodos
# Cada 5 tweets cambia el usuario
user_list = []
contador = 0
user_number = 1
for data in data_list:
    tweet = data.get("tweet")
    sentiment = data.get("sentiment")
    user = User(user_number, tweet, sentiment)
    user_list.append(user)
    contador = contador+1
    if contador >= 5:
        # Siguiente usuario
        user_number = user_number + 1
        contador = 0

# Recorrer lista de usuarios
for user in user_list:
    print("user number: ", user.number)
    print("user tweet: ", user.tweet)
    print("user sentiment: ", user.sentiment)
    print("")


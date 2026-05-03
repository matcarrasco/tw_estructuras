import csv
with open('tweet_sentiment.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)  # Crear diccionario con la libreria csv

    data_list = []  # Lista para guardar los diccionarios
    for row in csv_reader:
        data_list.append(row)

for data in data_list:
    print(data)

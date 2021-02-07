#import json
import random

f = open('pythonDB.db', 'w')
d = {}

# имена всякие
name = ['Masha', 'Tanya', 'Vanya', 'Petya', 'Kolya', 'Sash', 'Dasha', 'Sveta', 'Ira', 'Anya', 'Igor', 'Natasha']
# количество записей
cnt = 50000

# для поиска, чтобы поле было уникальным, добиваем имена порядковыми номерами
for i in range(cnt):
    d[str(i)] = random.choice(name) + str(i)

# запишем данные в файлик
f.write(str(d))
f.close()

# всякие размышления насчет обратной конвертации из str в dict
'''
f = open('pythonDB.db', 'r')
dd = f.read()
print(dd)
f.close()
print(type(dd))

a = json.loads(dd.replace("'",'"'))
print(type(a))
'''
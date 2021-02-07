import random
import redis

r = redis.Redis()

# имена всякие
name = ['Masha', 'Tanya', 'Vanya', 'Petya', 'Kolya', 'Sash', 'Dasha', 'Sveta', 'Ira', 'Anya', 'Igor', 'Natasha']
# количество записей
cnt = 50000

# для поиска, чтобы поле было уникальным, добиваем имена порядковыми номерами
for i in range(cnt):
    r.mset({i: random.choice(name)+str(i)})

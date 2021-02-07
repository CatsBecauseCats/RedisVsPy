import sys
import redis
import time
from createTableRadis import cnt

r = redis.Redis()

# поиск по ключу, здесь ключ - номер по порядку от 0 до cnt
startTime = time.time()
weFind = r.get(str(3))
endTimeKey = time.time() - startTime

# поиск по значению, для простоты берем то значение, которое нашли по ключу и ищем его перебором
# прерываем поиск, если нашли поле (поля все уникальны)
startTime = time.time()
for i in range(cnt):
    if r.get(str(i)) == weFind:
        break
endTimeValueUnic = time.time() - startTime

# поиск по значению, для простоты берем то значение, которое нашли по ключу и ищем его перебором
# (полный перебор  всех значений, актуально, если существуют неуникальные поля)
startTime = time.time()
for i in range(cnt):
    if r.get(str(i)) == weFind:
        tmp = r.get(str(i))
endTimeValueRepeat = time.time() - startTime

cntRec = sys.getsizeof('dump.rdb')

print('Время поиска по ключу: ', end='')
print("{:.4f}".format(endTimeKey), end='')
print(' сек')
print('Время поиска по значению (поля уникальны): ', end='')
print("{:.4f}".format(endTimeValueUnic), end= '')
print(' сек')
print('Время поиска по значению (поля не уникальны): ', end='')
print("{:.4f}".format(endTimeValueRepeat), end='')
print(' сек')
print('Занимаемая память (при количестве записей = ', cnt, '): ', cntRec, ' байт', end='')
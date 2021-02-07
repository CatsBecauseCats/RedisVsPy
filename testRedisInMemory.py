import random
import sys
import redis
import time

r = redis.Redis()
file = open('outputTestRedisInMemory.txt', 'w')

# имена всякие
name = ['Masha', 'Tanya', 'Vanya', 'Petya', 'Kolya', 'Sash', 'Dasha', 'Sveta', 'Ira', 'Anya', 'Igor', 'Natasha']
# количество записей
cnt = 80

# для поиска, чтобы поле было уникальным, добиваем имена порядковыми номерами
for i in range(cnt):
    r.mset({i: random.choice(name)+str(i)})

print('Время поиска по ключу - K')
print('Время поиска по значению (поля уникальны) - DM')
print('Время поиска по значению (поля не уникальны) - M ')
print('№', 'K,сек', 'DM,сек', 'M,сек', sep="                 ")

file.write('Время поиска по ключу - K' + '\n')
file.write('Время поиска по значению (поля уникальны) - DM' + '\n')
file.write('Время поиска по значению (поля не уникальны) - M ' + '\n')
file.write('№' + "                 " + 'K,сек' + "                 " + 'DM,сек' + "                 " + 'M,сек' + '\n')

mTimeKey = 0
mTimeValueUnic = 0
mTimeValueRepeat = 0

for j in range(cnt):
    key = j
    # поиск по ключу, здесь ключ - номер по порядку от 0 до cnt
    startTime = time.time()
    weFind = r.get(str(key))
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

    #cntRec = sys.getsizeof('dump.rdb')

    print(j+1, end="                 ")
    print("{:.4f}".format(endTimeKey), end="                 ")
    print("{:.4f}".format(endTimeValueUnic), end="                 ")
    print("{:.4f}".format(endTimeValueRepeat))

    file.write(str(j+1) + "                 ")
    file.write(str("{:.4f}".format(endTimeKey)) + "                 ")
    file.write(str("{:.4f}".format(endTimeValueUnic)) + "                 ")
    file.write(str("{:.4f}".format(endTimeValueRepeat)) + '\n')

    mTimeKey = mTimeKey + endTimeKey
    mTimeValueUnic = mTimeValueUnic + endTimeValueUnic
    mTimeValueRepeat = mTimeValueRepeat + endTimeValueRepeat
    #print(sys.getsizeof(r))

mTimeKey = mTimeKey /cnt
mTimeValueUnic = mTimeValueUnic / cnt
mTimeValueRepeat = mTimeValueRepeat / cnt

print('Среднее время поиска по ключу, сек: ', end='')
print("{:.4f}".format(mTimeKey))
print('Среднее время поиска по значению (поля уникальны), сек: ', end='')
print("{:.4f}".format(mTimeValueUnic))
print('Среднее время поиска по значению (поля не уникальны), сек: ', end='')
print("{:.4f}".format(mTimeValueRepeat))
print('Занимаемая память (при количестве записей = ', cnt, '): ', sys.getsizeof(r), ' байт')


file.write(str('Среднее время поиска по ключу, сек: '))
file.write(str("{:.4f}".format(mTimeKey)) + '\n')
file.write('Среднее время поиска по значению (поля уникальны), сек: ')
file.write(str("{:.4f}".format(mTimeValueUnic)) + '\n')
file.write('Среднее время поиска по значению (поля не уникальны), сек: ')
file.write(str("{:.4f}".format(mTimeValueRepeat)) + '\n')
file.write('Занимаемая память (при количестве записей = ' + str(cnt) + '): ' + str(sys.getsizeof(r)) + ' байт' + '\n')
file.close()
'''
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
'''
#import json
import random
import sys
import time

#f = open('pythonDB.db', 'w')
file = open('outputTestPythonInMemory.txt', 'w')
d = {}
searchVal = ''

# имена всякие
name = ['Masha', 'Tanya', 'Vanya', 'Petya', 'Kolya', 'Sash', 'Dasha', 'Sveta', 'Ira', 'Anya', 'Igor', 'Natasha']
# количество записей
cnt = 80

# для поиска, чтобы поле было уникальным, добиваем имена порядковыми номерами
for i in range(cnt):
    d[str(i)] = random.choice(name) + str(i)
findKey = ''

print('Время поиска по ключу - K')
print('Время поиска по значению (поля уникальны) - DM')
print('Время поиска по значению (поля не уникальны) - M ')
print('№', 'K,сек', 'DM,сек', 'M,сек', sep="                 ")
file.writelines('Время поиска по ключу - K' + '\n')
file.write('Время поиска по значению (поля уникальны) - DM' + '\n')
file.write('Время поиска по значению (поля не уникальны) - M ' + '\n')
file.write('№' + "                 " + 'K,сек' + "                 " + 'DM,сек' + "                 "+ 'M,сек' + '\n')
mTimeKey = 0
mTimeValueUnic = 0
mTimeValueRepeat = 0
for i in range(cnt):
    findKey = str(i)
    # ищем по ключу
    startTime = time.time()

    for key, value in d.items():
        if findKey == key:
            searchVal = value

    endTimeKey = time.time() - startTime

    # ищем по значению (не уникальные)
    startTime = time.time()
    for key, value in d.items():
        if searchVal == value:
            tmp = value
    endTimeValueRepeat = time.time() - startTime

    # ищем по значению (уникальные)
    startTime = time.time()
    for key, value in d.items():
        if searchVal == value:
            break
    endTimeValueUnic = time.time() - startTime

    print(i+1, end="                 ")
    print("{:.4f}".format(endTimeKey), end="                 ")
    print("{:.4f}".format(endTimeValueUnic), end="                 ")
    print("{:.4f}".format(endTimeValueRepeat))
    file.write(str(i+1) + "                 ")
    file.write(str("{:.4f}".format(endTimeKey)) + "                 ")
    file.write(str("{:.4f}".format(endTimeValueUnic)) + "                 ")
    file.write(str("{:.4f}".format(endTimeValueRepeat)) + '\n')
    mTimeKey = mTimeKey + endTimeKey
    mTimeValueUnic = mTimeValueUnic + endTimeValueUnic
    mTimeValueRepeat = mTimeValueRepeat + endTimeValueRepeat

mTimeKey = mTimeKey /cnt
mTimeValueUnic = mTimeValueUnic / cnt
mTimeValueRepeat = mTimeValueRepeat / cnt

print('Среднее время поиска по ключу, сек: ', end='')
print("{:.4f}".format(mTimeKey))
print('Среднее время поиска по значению (поля уникальны), сек: ', end='')
print("{:.4f}".format(mTimeValueUnic))
print('Среднее время поиска по значению (поля не уникальны), сек: ', end='')
print("{:.4f}".format(mTimeValueRepeat))
print('Занимаемая память (при количестве записей = ', cnt, '): ', sys.getsizeof(d), ' байт', end='')


file.write('Среднее время поиска по ключу, сек: ')
file.write(str("{:.4f}".format(mTimeKey)) + '\n')
file.write('Среднее время поиска по значению (поля уникальны), сек: ')
file.write(str("{:.4f}".format(mTimeValueUnic)) + '\n')
file.write('Среднее время поиска по значению (поля не уникальны), сек: ')
file.write(str("{:.4f}".format(mTimeValueRepeat)) + '\n')
file.write('Занимаемая память (при количестве записей = ' + str(cnt) + '): ' + str(sys.getsizeof(d)) + ' байт' + '\n')
file.close()

# запишем данные в файлик
# f.write(str(d))
# f.close()

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
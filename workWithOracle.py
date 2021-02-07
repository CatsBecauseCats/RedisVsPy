import sys
import time

import cx_Oracle
import config
import random
# test_sql - таблица
cx_Oracle.init_oracle_client(lib_dir="/usr/local/Cellar/instantclient-basic/19.3.0.0.0dbru/lib/")
connection = None
file = open('outputTestWorkWithOracle.txt', 'w')
print('Время поиска по ключу - K')
print('Время поиска по значению - DM')
#print('Время поиска по значению (поля не уникальны) - M ')
#print('№', 'K,сек', 'DM,сек', 'M,сек', sep="                 ")
print('№', 'K,сек', 'DM,сек', sep="                 ")
file.writelines('Время поиска по ключу - K' + '\n')
file.write('Время поиска по значению - DM' + '\n')
#file.write('Время поиска по значению (поля не уникальны) - M ' + '\n')
#file.write('№' + "                 " + 'K,сек' + "                 " + 'DM,сек' + "                 "+ 'M,сек' + '\n')
file.write('№' + "                 " + 'K,сек' + "                 " + 'DM,сек' + '\n')
mTimeKey = 0
mTimeValueUnic = 0
mTimeValueRepeat = 0

searchVal = ''

# имена всякие
name = ['Masha', 'Tanya', 'Vanya', 'Petya', 'Kolya', 'Sash', 'Dasha', 'Sveta', 'Ira', 'Anya', 'Igor', 'Natasha']
# количество записей
cnt = 80
d = [''] * cnt

# для поиска, чтобы поле было уникальным, добиваем имена порядковыми номерами
for i in range(cnt):
    #d.append((str(i), random.choice(name) + str(i)))
    d[i] = (str(i), random.choice(name) + str(i))

findKey = ''

# DROP TABLE test_sql;

# create table test_sql (
# id VARCHAR2(100),
# name VARCHAR2(100)
# );

# SELECT COUNT(*) FROM test_sql;


try:
    connection = cx_Oracle.connect(
        config.username,
        config.password,
        config.dsn,
        encoding=config.encoding)
    cur = connection.cursor()
    cur.execute("DROP TABLE test_sql")
    cur.execute("CREATE TABLE test_sql (id VARCHAR2(100), name VARCHAR2(100))")
    cur.bindarraysize = cnt
    cur.setinputsizes(100, 100)
    cur.executemany("insert into test_sql(id, name) values (:1, :2)", d)
    connection.commit()
    cur.execute("select * from test_sql")
    rows = cur.fetchall()
    #for row in rows:
    #    print(row[0], row[1])
    #cur.execute("SELECT COUNT(*) FROM test_sql")
    #cnt_rows = cur.fetchall()[0][0]
    #print(cnt_rows)
    #searchVal = d[0][1]
    #print(searchVal)
    #cur.execute("select * from test_sql where name = :mybv", mybv=searchVal)
    #tmp = cur.fetchall()
    #print(tmp)


    for k in range(cnt):
        startTime = time.time()
        findKey = k
        for i in range(cnt):
            # поиск по ключу
            #findKey = i
            cur.execute("select * from test_sql where id = :mybv", mybv=findKey)
            tmp = cur.fetchall()[0][0]
            #print(tmp)
        endTimeKey = time.time() - startTime

        # ищем по значению (не уникальные)
        searchVal = d[k][1]
        startTime = time.time()
        for i in range(cnt):
            cur.execute("select * from test_sql where name = :mybv", mybv=searchVal)
            tmp = cur.fetchall()[0][1]
            #print(tmp)
        endTimeValueRepeat = time.time() - startTime

        # ищем по значению (уникальные)
        '''
        startTime = time.time()
        for j in range(cnt):
            for i in range(cnt):
                #searchVal = d[j][1]
                cur.execute("select * from test_sql where name = :mybv", mybv=searchVal)
                tmp = cur.fetchall()[0][1]
                print(tmp)
                break
        endTimeValueUnic = time.time() - startTime
        '''
        mTimeKey = mTimeKey + endTimeKey
        #mTimeValueUnic = mTimeValueUnic + endTimeValueUnic
        mTimeValueRepeat = mTimeValueRepeat + endTimeValueRepeat

        print(k + 1, end="                 ")
        print("{:.4f}".format(endTimeKey), end="                 ")
        #print("{:.4f}".format(endTimeValueUnic), end="                 ")
        print("{:.4f}".format(endTimeValueRepeat))
        file.write(str(i + 1) + "                 ")
        file.write(str("{:.4f}".format(endTimeKey)) + "                 ")
        #file.write(str("{:.4f}".format(endTimeValueUnic)) + "                 ")
        file.write(str("{:.4f}".format(endTimeValueRepeat)) + '\n')
        mTimeKey = mTimeKey + endTimeKey
        #mTimeValueUnic = mTimeValueUnic + endTimeValueUnic
        mTimeValueRepeat = mTimeValueRepeat + endTimeValueRepeat

    mTimeKey = mTimeKey / cnt
    mTimeValueUnic = mTimeValueUnic / cnt
    mTimeValueRepeat = mTimeValueRepeat / cnt

    print('Среднее время поиска по ключу, сек: ', end='')
    print("{:.4f}".format(mTimeKey))
    print('Среднее время поиска по значению, сек: ', end='')
    print("{:.4f}".format(mTimeValueUnic))
    #print('Среднее время поиска по значению (поля не уникальны), сек: ', end='')
    #print("{:.4f}".format(mTimeValueRepeat))
    print('Занимаемая память (при количестве записей = ', cnt, '): ', sys.getsizeof(d), ' байт', end='')

    file.write('Среднее время поиска по ключу, сек: ')
    file.write(str("{:.4f}".format(mTimeKey)) + '\n')
    file.write('Среднее время поиска по значению, сек: ')
    file.write(str("{:.4f}".format(mTimeValueUnic)) + '\n')
    #file.write('Среднее время поиска по значению (поля не уникальны), сек: ')
    #file.write(str("{:.4f}".format(mTimeValueRepeat)) + '\n')
    file.write(
        'Занимаемая память (при количестве записей = ' + str(cnt) + '): ' + str(sys.getsizeof(d)) + ' байт' + '\n')
    file.close()
except cx_Oracle.Error as error:
    print(error)
finally:
    # release the connection
    if connection:
        connection.close()

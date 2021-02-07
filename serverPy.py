import json
import socketserver
import sys
import time
from createDict import cnt
host = '0.0.0.0'
port = 8800
addr = (host, port)

#
class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(512)
        inStr = self.data.decode('utf-8')
        inList = inStr.split()
        request = inList[0]
        endTimeKey = endTimeValueRepeat = endTimeValueUnic = time.time()
        if request == 'GET':
            findKey = inList[1]
            f = open('pythonDB.db', 'r')
            strDB = f.read()
            f.close()
            dictDB = json.loads(strDB.replace("'", '"'))
            searchVal = ''

            # ищем по ключу
            startTime = time.time()
            for key, value in dictDB.items():
                if findKey == key:
                    searchVal = value

            endTimeKey = time.time() - startTime

            # ищем по значению (не уникальные)
            startTime = time.time()
            for key, value in dictDB.items():
                if searchVal == value:
                    tmp = value
            endTimeValueRepeat = time.time() - startTime

            # ищем по значению (уникальные)
            startTime = time.time()
            for key, value in dictDB.items():
                if searchVal == value:
                    break
            endTimeValueUnic = time.time() - startTime

        cntRec = sys.getsizeof('pythonDB.rdb')

        print('Время поиска по ключу: ', end='')
        print("{:.4f}".format(endTimeKey), end='')
        print(' сек')
        print('Время поиска по значению (поля уникальны): ', end='')
        print("{:.4f}".format(endTimeValueUnic), end='')
        print(' сек')
        print('Время поиска по значению (поля не уникальны): ', end='')
        print("{:.4f}".format(endTimeValueRepeat), end='')
        print(' сек')
        print('Занимаемая память (при количестве записей = ', cnt, '): ', cntRec, ' байт')



if __name__ == "__main__":
    server = socketserver.TCPServer(addr, MyTCPHandler)

    print('Сервер работает...')
    server.serve_forever()

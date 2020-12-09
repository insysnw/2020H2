import socket
import datetime
import threading

address = ("0.0.0.0", 8686)

inputs = list()
outs = list()
clients = dict()

header_length = 5

def create_packet(sock,size_msg,msg,time):
    ans = bytearray()
    # 0 - отправка сообщения, 1 - сообщение о новом пользователе
    ans.append(0)
    # 2 байта времени (часы,минуты)
    ans.append(int(time[:2]))
    ans.append(int(time[3:]))
    # 5 байт длина nickname, далее сам nickname
    ans += (len(clients[sock])).to_bytes(header_length,"big")
    ans += clients[sock].encode()
    # 5 байт длина сообщения, далее само сообщение
    ans += (size_msg).to_bytes(header_length,"big")
    ans += msg.encode()
    return ans

def get_socket():

    # Создаем сокет
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(1)

    # Биндим сервер на нужный адрес и порт
    server.bind(address)

    server.listen()

    return server


def handle_connections(resource):
    
    while True:
        data = ""
        try:
            data = resource.recv(1)
        except:
            clear_resource(resource)
            del clients[resource]
            break
               
        if data:

            if resource not in outs:
                outs.append(resource)

            # Первый пакет от клиента с nickом
            if data[0] == 1:
                data += resource.recv(header_length)
                size_nick = int.from_bytes(data[1:],"big")
                data += resource.recv(size_nick)
                nick = data[6:].decode()
                print("New user " + nick)
                clients[resource] = nick
            # Пакет с сообщением
            else:
                time = datetime.datetime.now().strftime("%H:%M")
                size_msg = int.from_bytes(resource.recv(header_length),"big")
                msg = resource.recv(size_msg).decode()
                data = create_packet(resource,size_msg,msg,time)
                print('<{0}> [{1}] {2}'.format(time,clients[resource],msg))

            # Отправка данных всем клиентам
            for i in outs:
                i.sendall(data)                   

        else:
            # Очистка данных о ресурсе
            clear_resource(resource)
            del clients[resource]
            break


def clear_resource(resource):

    if resource in outs:
        outs.remove(resource)
    if resource in inputs:
        inputs.remove(resource)
    resource.close()

    print('Closing connection ' + str(resource))



if __name__ == '__main__':

    server_socket = get_socket()
    inputs.append(server_socket)

    print("Server is running, please, press ctrl+c to stop")
    try:
        while True:
            sock, addr = server_socket.accept()
            sock.setblocking(1)
            inputs.append(sock)
            print("New connection from {address}".format(address=addr))
            threading.Thread(target=handle_connections,args=(sock,),daemon=True).start()

    except KeyboardInterrupt:
        clear_resource(server_socket)
        print("Server stopped!")

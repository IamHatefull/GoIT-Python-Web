import socket
import threading

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.bind(('127.0.0.1', 1235))
soc.listen(2)

users = []


def response_all(user, data):
    for some_user in users:
        #print(user)
        if some_user is user:
            continue
        some_user.send(data)


def listen_user(user):
    while True:
        try:
            data = user.recv(2048)
        
            print(f'User sent {data}')
            user.send(str.encode('OK'))

            response_all(user, data)
        except ConnectionResetError:
            print("The remote host forcibly dropped the existing connection")
            break
        except KeyboardInterrupt:
            print("Stopped server")
            break



def start_server():
    print('Server started...')
    while True:
        try:
            user_socket, address = soc.accept()
            print(f'user {address} connected')

            users.append(user_socket)
            listen_concurrently = threading.Thread(
                target=listen_user,
                args=(user_socket,))
            listen_concurrently.start()
        except ConnectionResetError:
            print("The remote host forcibly dropped the existing connection")
        except KeyboardInterrupt:
            print("Stopped server")



if __name__ == '__main__':
    start_server()
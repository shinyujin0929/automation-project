import socket
import time
import keyboard
import threading
from cobot_control import CobotController  # 로봇팔 제어 클래스 임포트

# 서버 정보 설정
HOST = "172.30.1.56"
PORT = 9007

class Server:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.cobot = CobotController()  # 로봇팔 컨트롤러 초기화

    def start_server(self):
        client_socket = None
        server_socket = None
        
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print(f"Server listening on {self.host}:{self.port}")

            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            while True:
                command = client_socket.recv(1024).decode('utf-8')
                if not command:
                    print("Client disconnected.")
                    break
                print(f"Received command from client: {command}")

                response = self.cobot.handle_command(command)
                client_socket.sendall(response.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if client_socket:
                client_socket.close()
            if server_socket:
                server_socket.close()
            print("Server closed.")

    def keyboard_control(self):
        """ 로봇팔 제어 """
        print("\n키보드 명령어:")
        print("1: 하역 1번, 2: 하역 2번, 3: 하역 3번")
        print("a: 적재 1번, b: 적재 2번, c: 적재 3번")
        print("0: 기본 위치")

        while True:
            if keyboard.is_pressed('0'):
                self.cobot.default()
            if keyboard.is_pressed('1'):
                self.cobot.unload_1()
            if keyboard.is_pressed('2'):
                self.cobot.unload_2()
            if keyboard.is_pressed('3'):
                self.cobot.unload_3()
            if keyboard.is_pressed('a'):
                self.cobot.load_1()
            if keyboard.is_pressed('b'):
                self.cobot.load_2()
            if keyboard.is_pressed('c'):
                self.cobot.load_3()

if __name__ == "__main__":
    server = Server()
    
    # 서버와 키보드 제어를 동시에 실행
    server_thread = threading.Thread(target=server.start_server)
    keyboard_thread = threading.Thread(target=server.keyboard_control)

    server_thread.start()
    keyboard_thread.start()

    server_thread.join()
    keyboard_thread.join()

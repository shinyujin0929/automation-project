import time
from pymycobot.mycobot import MyCobot

class CobotController:
    def __init__(self, port='COM5', baudrate=115200):
        """로봇팔 초기화"""
        self.mc = MyCobot(port, baudrate)
        time.sleep(2)
        self.mc.set_gripper_mode(0)
        self.mc.init_eletric_gripper()
        print("로봇팔 연결 성공")

    def default(self):
        """기본 위치로 이동"""
        self.mc.send_angles([-90, 0, 0, 0, 0, 0], 20)
        print("기본 위치로 이동")
        time.sleep(2)

    def unload_1(self):
        """하역 1번 위치"""
        print("1번 물건 적재")
        self.mc.send_angles([-95.8, -4.48, 0.17, 4.3, -77.16, -5.88], 50)
        time.sleep(2)
        self.mc.send_angles([-97.03, -28.21, 27.94, 38.84, -86.22, 70], 50)
        time.sleep(1.5)
        self.mc.set_gripper_state(0, 80)  # 그리퍼 오픈
        time.sleep(1)
        self.mc.send_angles([-107.05, -11.51, 56.25, 39.46, -89.29, 72.5], 30)
        time.sleep(1.5)
        self.mc.set_gripper_state(1, 80)  # 그리퍼 닫기
        time.sleep(2)

    def unload_2(self):
        """하역 2번 위치"""
        print("2번 물건 적재")
        self.mc.send_angles([-95.8, -4.48, 0.17, 4.3, -77.16, -5.88], 40)
        time.sleep(3)
        self.mc.send_angles([-97.03, -28.21, 27.94, 38.84, -86.22, 70], 40)
        time.sleep(2)
        self.mc.set_gripper_state(0, 80)
        time.sleep(1)
        self.mc.send_angles([-141.15, -13.87, 65.79, 33.57, -84.37, 32.51], 40)
        time.sleep(2)
        self.mc.set_gripper_state(1, 80)
        time.sleep(2)

    def unload_3(self):
        """하역 3번 위치"""
        print("3번 물건 적재")
        self.mc.send_angles([-95.8, -4.48, 0.17, 4.3, -77.16, -5.88], 40)
        time.sleep(2)
        self.mc.send_angles([-97.03, -28.21, 27.94, 38.84, -86.22, 70], 40)
        time.sleep(2)
        self.mc.set_gripper_state(0, 80)
        time.sleep(2)

    def load_1(self):
        """적재 1번 위치"""
        print("3번 위치 물건 적재")
        self.mc.send_angles([-8.52, -18.54, 64.68, 14.23, -90.17, -9.31], 40)
        time.sleep(2)
        self.mc.set_gripper_state(0, 100)
        time.sleep(2)

    def load_2(self):
        """적재 2번 위치"""
        print("2번 위치 물건 적재")
        self.mc.send_angles([-8.52, -18.54, 64.68, 14.23, -90.17, -9.31], 40)
        time.sleep(2)
        self.mc.set_gripper_state(0, 100)
        time.sleep(2)

    def load_3(self):
        """적재 3번 위치"""
        print("1번 위치 물건 적재")
        self.mc.send_angles([-8.52, -18.54, 64.68, 14.23, -90.17, -9.31], 40)
        time.sleep(2)
        self.mc.set_gripper_state(0, 100)
        time.sleep(2)

    def handle_command(self, command):
        """서버에서 받은 명령 처리"""
        if command == "Arrived":
            print("Arrived: 이동 명령 받음")
            time.sleep(5)
            self.unload_1()  # 기본적으로 unload_1 실행
            return "START"
        return "INVALID COMMAND"

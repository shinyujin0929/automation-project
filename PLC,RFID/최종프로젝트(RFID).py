from mfrc522 import SimpleMFRC522  # MFRC522 NFC 리더 라이브러리 임포트
import RPi.GPIO as GPIO  # Raspberry Pi GPIO 제어 라이브러리 임포트
import signal  # 시스템 신호 처리 라이브러리 임포트
import spidev  # SPI 장치와 통신하기 위한 라이브러리 임포트
import sys  # 시스템 관련 함수 사용을 위한 라이브러리 임포트
import time  # 시간 관련 함수 사용을 위한 라이브러리 임포트
import serial  # 직렬 통신을 위한 라이브러리 임포트

# 직렬 통신 설정
port = '/dev/ttyUSB0'  # PLC와 연결된 직렬 포트
baudrate = 9600  # 직렬 통신 속도 설정
ser = serial.Serial(port, baudrate, timeout=1)  # 직렬 포트 열기

# NFC 클래스를 정의
class NFC():
    def __init__(self, bus=0, device=0, spd=1000000):
        self.reader = SimpleMFRC522()  # MFRC522 리더 초기화
        self.close()  # 리더 종료
        self.boards = {}  # 리더 목록을 저장할 딕셔너리

        self.bus = bus  # SPI 버스 번호
        self.device = device  # SPI 장치 번호
        self.spd = spd  # SPI 속도 설정

    def reinit(self):
        # 리더 재초기화: SPI 연결 설정
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    def close(self):
        # SPI 연결 종료
        self.reader.READER.spi.close()

    def addBoard(self, rid, pin):
        # 리더를 보드에 추가하고, 해당 리더에 대한 GPIO 핀을 설정
        self.boards[rid] = pin
        GPIO.setup(pin, GPIO.OUT)  # 핀을 출력 모드로 설정
        print(pin)

    def selectBoard(self, rid):
        # 지정된 리더가 존재하는지 확인 후 해당 리더의 핀을 활성화
        if not rid in self.boards:
            print("readerid" + rid + "not found")
            return False
        
        # 모든 리더 핀 중에서 지정된 리더의 핀만 HIGH로 설정
        for loop_id in self.boards:
            GPIO.output(self.boards[loop_id], loop_id == rid)
        return True
        
    def read(self, rid):
        # 지정된 리더에서 NFC 태그 데이터 읽기
        if not self.selectBoard(rid):
            return None
        
        self.reinit()  # 리더 초기화
        cid, val = self.reader.read_no_block()  # 비차단 방식으로 태그 읽기
        self.close()  # 리더 종료

        return val
    
    def write(self, rid, value):
        # 지정된 리더에 NFC 태그에 데이터 쓰기
        if not self.selectBoard(rid):
            return False
        
        self.reinit()  # 리더 초기화
        self.reader.write_no_block(value)  # 비차단 방식으로 데이터 쓰기
        self.close()  # 리더 종료
        return True
    
# PLC로 데이터를 전송하는 함수
def send_to_plc(value):
    data_to_send = bytes([value])  # 값을 바이트로 변환
    ser.write(data_to_send)  # 직렬 통신으로 데이터 전송
    print(f"sent{value}to plc")  # 전송한 값 출력

# Ctrl+C 신호를 처리하여 GPIO를 정리하고 종료하는 함수
def signal_handler(sig, frame):
    GPIO.cleanup()  # GPIO 핀 초기화
    print()
    sys.exit(0)  # 프로그램 종료

# 메인 함수
def main():
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C 시 종료 처리
    GPIO.setmode(GPIO.BCM)  # GPIO 번호를 BCM 모드로 설정

    nfc = NFC()  # NFC 객체 생성

    readers = [
        ("reader1", 5),  # reader1은 GPIO 5에 연결
        ("reader2", 6)   # reader2는 GPIO 6에 연결
    ]

    # 각 NFC 리더를 추가
    for r in readers:
        nfc.addBoard(r[0], r[1])

    # 무한 루프: NFC 태그 읽기 및 PLC로 전송
    while True:
        for r in readers:
            try:
                r_name = r[0]  # 리더 이름
                data = nfc.read(r_name)  # NFC 태그 데이터 읽기
                if data:
                    print(f"{r_name}: {data}")  # 읽은 데이터 출력

                    # reader1에서 "GATE OPEN"이 포함된 데이터가 있을 경우 PLC로 1을 전송
                    if r_name == "reader1" and "GATE OPEN" in data:
                        send_to_plc(1)  # PLC로 1 전송
                        time.sleep(2)  # 2초 대기

                    # reader2에서 "GATE OPEN"이 포함된 데이터가 있을 경우 PLC로 2를 전송
                    elif r_name == "reader2" and "GATE OPEN" in data:
                        send_to_plc(2)  # PLC로 2 전송
                        time.sleep(2)  # 2초 대기

            except Exception as e:
                print("e", e)  # 예외 발생 시 출력

    GPIO.cleanup()  # GPIO 정리

# 프로그램 실행
if __name__ == "__main__":
    main()  # main() 함수 실행

import Jetson.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (BCM 모드 사용)
servo_pin = 18  # 서보모터 제어 핀, 연결한 GPIO 핀으로 변경하세요

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# PWM 객체 생성 (50Hz 주파수)
pwm = GPIO.PWM(servo_pin, 50) 
pwm.start(0)  # PWM 시작

# 각도 설정 함수
def set_angle(angle):
    duty = (angle / 18) + 2  # 0도에서 180도까지 범위 설정
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

# 입출차기 동작 시뮬레이션
try:
    while True:
        # 입차: 서보 모터가 90도 회전하여 장애물 열림
        print("입차 - 장애물 열림")
        set_angle(90)
        time.sleep(5)  # 입차 시간 대기
        
        # 출차: 서보 모터가 원래 상태로 돌아옴 (0도)
        print("출차 - 장애물 닫힘")
        set_angle(0)
        time.sleep(5)  # 출차 시간 대기

except KeyboardInterrupt:
    print("종료됨")
    pwm.stop()
    GPIO.cleanup()

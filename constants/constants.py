
from ev3dev2.port import LegoPort
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.motor import *
from smbus import SMBus


class constants:

    def __init__(self):
       # self.DRIVING_MOTOR_LEFT = LargeMotor(OUTPUT_B)  # motor 1
       # self.DRIVING_MOTOR_RIGHT = LargeMotor(OUTPUT_C)  # motor 2
       # self.SECURING_MOTOR = MediumMotor(OUTPUT_A)
       # self.SHOOTING_MOTOR = MediumMotor(OUTPUT_D)

       # self.PRESSURE_SENSOR = TouchSensor(INPUT_4)
       # self.GYRO_SENSOR = GyroSensor(INPUT_3)
       # self.GYRO_SENSOR.calibrate()
       # self.COLOR_SENSOR = ColorSensor(INPUT_2)

        self.CAMERA_ADDRESS = 0x54
        input1 = LegoPort(INPUT_1)
        input1.mode = 'other-i2c'
        self.BUS = SMBus(3)
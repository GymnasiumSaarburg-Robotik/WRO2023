from decryption.api import capture

from constants.constants import constants
from ev3dev2.motor import *
from ev3dev2.sound import Sound

def only_contains_one_element(data):
    return len(set(data)) == 1


def readBlocks(current_direction):
    data = [174, 193, 32, 2, 255, 255]
    c.BUS.write_i2c_block_data(c.CAMERA_ADDRESS, 0, data)
    # Read first block
    data = ""
    block = c.BUS.read_i2c_block_data(c.CAMERA_ADDRESS, 0, 6 + 14)
    if not only_contains_one_element(block[7:]):
        data += str(block)
    while True:
        block2 = c.BUS.read_i2c_block_data(c.CAMERA_ADDRESS, 0, 14)
        if only_contains_one_element(block2):
            break
        data += "|\n" + str(block2)
    return capture(data, current_direction)

def shoot():
    a = MediumMotor(OUTPUT_A)
    d = MediumMotor(OUTPUT_D)

    d.on_for_rotations(speed=20, rotations=0.25, brake=True, block=True)
    a.on_for_rotations(speed=-60, rotations=1.25, brake=True, block=True)
    d.on_for_rotations(speed=-20, rotations=0.25, brake=True, block=True)

c = constants()

sound = Sound()
sound.speak('Ari ist voll der Hurensohn', volume=100)

#d = direction_data(c, 0)
for i in range(50):
    print(str(i))
    shoot()



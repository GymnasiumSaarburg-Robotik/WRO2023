from decryption.api import *

from constants.constants import constants#
from ev3dev2.motor import *


def only_contains_one_element(data):
    return len(set(data)) == 1


def read_blocks(current_direction):
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
    return Capture(data, current_direction)


c = constants()
d = direction_data(c, 0)


count = 1

c0 = d.captures[0]
image = c0.generate_bit_map()

for i in range(1, 9):
    print(str(i))
    c1 = d.captures[1]
    image = combine_bit_maps(image, c1.generate_bit_map(), 1)
    count += 1

cF = d.captures[9]
image = combine_bit_maps(image, cF.generate_bit_map(), 10)
print_two_d_array(image)
image = filter_and_convert_to_bitmap(image, 0.3)
image = get_square_bitmap(image)





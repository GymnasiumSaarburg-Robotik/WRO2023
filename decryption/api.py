import re
import json
from json import JSONEncoder
from json import JSONDecoder

from decryption.block import CCblock


class Capture:
    def __init__(self, raw_data: str = None, current_direction: int = None, blocks=None,
                 generate_missing_params: bool = True):
        if blocks is None:
            blocks = []
        if current_direction is None:
            current_direction = []

        self.CONST_CAMERA_DIRECTION_WIDTH = 65  # Einstellen bezüglich Drehung
        self.CONST_CAMERA_PIXEL_WIDTH = 319

        # Camera image is 319px
        # https://forum.pixycam.com/t/resolution-tracking-pixy2/5646
        # -> Claiming 316 x 208

        self.blocks = blocks
        self.current_direction = current_direction
        self.rawData = raw_data

        self.blockDirectionDiffs = []

        if raw_data is not None and generate_missing_params:
            self.decrypt_data(current_direction)

    def decrypt_data(self, current_direction):
        try:
            data = self.rawData
            data = re.findall('\[(.*?)\]', data)
            first = True
            for index, block in enumerate(data):
                block = block.replace("1, 0, ", "", 1)
                block_as_string_list = block.split(",")
                if first:
                    block_as_string_list = block_as_string_list[6:]
                    first = False
                block_as_string_list = block_as_string_list[:-4]
                data = [int(x) for x in block_as_string_list]
                summed_data = []
                num_hash = 0

                for i in range(len(data)):
                    if i % 2 != 0:
                        if data[i] == 1:
                            num_hash += 255
                        else:
                            num_hash += data[i]
                        summed_data.append(num_hash)
                        num_hash = 0
                    else:
                        num_hash += data[i]

                for i in range(1, int(len(summed_data) / 4) + 1):
                    base_index = i * 4 - 1

                    x_center = summed_data[base_index - 3]
                    y_center = summed_data[base_index - 2]
                    width = summed_data[base_index - 1]
                    height = summed_data[base_index]
                    x_pos = x_center - width / 2
                    y_pos = y_center - height / 2

                    # Relative Position im Bild [<0.5; 0.5; >0.5]
                    relative_direction = x_center / self.CONST_CAMERA_PIXEL_WIDTH
                    direction_offset = 0
                    if relative_direction > 0.5:
                        relative_direction -= 0.5
                        direction_offset = relative_direction * self.CONST_CAMERA_DIRECTION_WIDTH
                    elif relative_direction < 0.5:
                        relative_direction = 0.5 - relative_direction
                        direction_offset = -1 * relative_direction * self.CONST_CAMERA_DIRECTION_WIDTH

                    block_object = CCblock(int(x_pos), int(y_pos), int(x_center), int(y_center), int(width),
                                           int(height), int(width * height), direction_offset)
                    self.blocks.append(block_object)
                    self.blockDirectionDiffs.append(direction_offset)
        except True:  # Catch any exception
            print("Data could not be resolved.")
            return

    def __str__(self) -> str:
        return "CAPTURE: \n     rawData: {} \n      blocks {} \n      current_direction {}" \
            .format(self.rawData, self.blocks, self.current_direction)

    def generate_bit_map(self):
        image = [[0 for _ in range(325)] for _ in range(225)]
        for block in self.blocks:
            b = block
            print(str(block))
            for y in range(b.y_pos, b.y_pos + int(b.height)):
                for x in range(b.x_pos, b.x_pos + b.width):
                    image[y][x] = 1
        return image


class CaptureEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class CaptureDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if 'rawData' in dct:
            return Capture(raw_data=dct['rawData'], blocks=dct['blocks'], current_direction=dct['current_direction'],
                           generate_missing_params=False)
        if 'x_pos' in dct:
            return CCblock(dct['x_pos'], dct['y_pos'], dct['size'], dct['direction'])

def print_two_d_array(arr):
    for r in arr:
        print(str(r))

def only_contains_one_element(data):
    return len(set(data)) == 1

def combine_bit_maps(bitmap1, bitmap2, limit):
    average_bitmap = [[((bitmap1[a][b] + bitmap2[a][b]) / limit) for b in range(len(bitmap1[0]))] for a in
                      range(len(bitmap1))]
    return average_bitmap

def filter_and_convert_to_bitmap(arr, min_val):
    bitmap = []
    for subarr in arr:
        sub_bitmap = []
        for val in subarr:
            if val >= min_val:
                sub_bitmap.append(1)
            else:
                sub_bitmap.append(0)
        bitmap.append(sub_bitmap)
    return bitmap

def get_square_bitmap(bitmap):
    # Initialize variables
    height = len(bitmap)
    width = len(bitmap[0])
    square_bitmap = [[0] * width for _ in range(height)]
    rectangles = []

    # Define helper function to draw a filled square in the square_bitmap
    def draw_square(x, y, size):
        for i in range(x, x + size):
            for j in range(y, y + size):
                square_bitmap[j][i] = 1

    # Define helper function to find the boundaries of a rectangle
    def find_boundary(x, y):
        left, right, up, down = x, x, y, y
        stack = [(x, y)]
        while stack:
            i, j = stack.pop()
            if i < 0 or j < 0 or i >= width or j >= height or bitmap[j][i] == 0:
                continue
            bitmap[j][i] = 0  # mark pixel as visited
            left = min(left, i)
            right = max(right, i)
            up = min(up, j)
            down = max(down, j)
            stack.append((i - 1, j))
            stack.append((i + 1, j))
            stack.append((i, j - 1))
            stack.append((i, j + 1))
        return left, right, up, down

    # Iterate through each pixel in the bitmap and find the boundaries of each rectangle
    for i in range(width):
        for j in range(height):
            if bitmap[j][i] == 1:
                left, right, up, down = find_boundary(i, j)
                size = max(right - left + 1, down - up + 1)
                draw_square(left, up, size)

    return square_bitmap


class direction_data:
    def __init__(self, constants, direction):
        self.c = constants
        self.captures = []
        self.initialize(10, direction)

    def initialize(self, frame_count, direction):
        for i in range(frame_count):
            self.read_blocks(direction)

    def read_blocks(self, current_direction):
        data = [174, 193, 32, 2, 255, 255]
        self.c.BUS.write_i2c_block_data(self.c.CAMERA_ADDRESS, 0, data)
        # Read first block
        data = ""
        block = self.c.BUS.read_i2c_block_data(self.c.CAMERA_ADDRESS, 0, 6 + 14)
        if not only_contains_one_element(block[7:]):
            data += str(block)
        while True:
            block2 = self.c.BUS.read_i2c_block_data(self.c.CAMERA_ADDRESS, 0, 14)
            if only_contains_one_element(block2):
                break
            data += "|\n" + str(block2)
        capture = Capture(data, current_direction)
        print(len(capture.blocks))
        self.captures.append(capture)

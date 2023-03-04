import re
import json
from json import JSONEncoder
from json import JSONDecoder

from decryption.block import CCblock


class capture:
    def __init__(self, raw_data, current_direction):
        self.CONST_CAMERA_DIRECTION_WIDTH = 65  # Einstellen bezüglich Drehung
        self.CONST_CAMERA_PIXEL_WIDTH = 315  # Camera image is 319px

        self.rawData = raw_data
        self.blocks = []
        self.blockDirectionDiffs = []
        self.relativeDirections = []
        self.current_direction = current_direction
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

                    # Relative Position im Bild [<0.5; 0.5; >0.5]
                    relative_direction = x_center / self.CONST_CAMERA_PIXEL_WIDTH
                    self.relativeDirections.append(relative_direction)
                    direction_offset = 0
                    if relative_direction > 0.5:
                        relative_direction -= 0.5
                        direction_offset = relative_direction * self.CONST_CAMERA_DIRECTION_WIDTH
                    elif relative_direction < 0.5:
                        relative_direction = 0.5 - relative_direction
                        direction_offset = -1 * relative_direction * self.CONST_CAMERA_DIRECTION_WIDTH

                    block_object = CCblock(int(x_center), int(y_center), int(width * height), direction_offset)
                    self.blocks.append(block_object)
                    self.blockDirectionDiffs.append(direction_offset)
        except True:  # Catch any exception
            print("Data could not be resolved.")
            return


# subclass JSONEncoder
class CaptureEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class CaptureDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        return capture(dct['rawData'])


def only_contains_one_element(data):
    return len(set(data)) == 1


class direction_data:
    def __init__(self, constants, direction):
        self.c = constants
        self.captures = []
        self.initialize(10, direction)
        for s in self.captures:
            print(json.dumps(s, indent=4, cls=CaptureEncoder))

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
        self.captures.append(capture(data, current_direction))

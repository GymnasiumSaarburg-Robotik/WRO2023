import json
import numpy as np
import matplotlib.pyplot as plt

from decryption.api import CaptureDecoder, Capture


def combine_bit_maps(bitmap1, bitmap2, limit):
    average_bitmap = [[((bitmap1[a][b] + bitmap2[a][b]) / limit) for b in range(len(bitmap1[0]))] for a in
                      range(len(bitmap1))]
    return average_bitmap


def filter_and_convert_to_bitmap(arr, min_val):
    arr = np.array(arr)
    return np.where((arr >= min_val), 1, 0)


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


count = 1

c: Capture = json.load(open("json/data0.json"), cls=CaptureDecoder)
image = c.generate_bit_map()

for i in range(1, 9):
    print(str(i))
    c1: Capture = json.load(open("json/data" + str(i) + ".json"), cls=CaptureDecoder)
    image = combine_bit_maps(image, c1.generate_bit_map(), 1)
    count += 1

c1: Capture = json.load(open("json/data9.json"), cls=CaptureDecoder)
image = combine_bit_maps(image, c1.generate_bit_map(), 10)
image = filter_and_convert_to_bitmap(image, 0.3)
image = get_square_bitmap(image)

plt.imshow(image, cmap='gray')
plt.show()

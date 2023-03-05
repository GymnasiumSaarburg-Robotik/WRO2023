import json
from decryption.api import CaptureDecoder, Capture
import matplotlib.pyplot as plt

def combine_bit_maps(bitmap1, bitmap2, c):
    average_bitmap = [[(bitmap1[a][b] + bitmap2[a][b]) / c for b in range(len(bitmap1[0]))] for a in
                      range(len(bitmap1))]
    return average_bitmap


count = 1

c: Capture = json.load(open("json/data0.json"), cls=CaptureDecoder)
image = c.generate_bit_map()

for i in range(1, 10):
    c1: Capture = json.load(open("json/data" + str(i) + ".json"), cls=CaptureDecoder)
    image = combine_bit_maps(image, c1.generate_bit_map(), count)
    count += 1



# display the bitmap
plt.imshow(image, cmap='gray')
plt.show()

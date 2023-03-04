from decryption.api import capture

data = [1, 1, 0, 24, 1, 88, 0, 28, 0, 23]
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

print(summed_data)

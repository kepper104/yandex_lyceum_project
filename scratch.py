cells = [['69', '6d', '70', '6f', '72', '74', '20', '73', '79', '73', '0d', '0a', '0d', '0a', '69', '6d', ''], ['70', '6f', '72', '74', '20', '74', '61', '62', '0d', '0a', '66', '72', '6f', '6d', '20', '50', ''], ['79', '51', '74', '35', '20', '69', '6d', '70', '6f', '72', '74', '20', '75', '69', '63', '2c', '']]
print(cells)
all_cells = []
print(cells)
print(bytes(cells[0][0], "utf-8"))
print(bin(int(cells[0][0], 16)))
for i in cells:
    for el in i:
        if el == '':
            continue
        # print(el)
        all_cells.append((int(el, 16)))
    # all_cells.extend(i[:-1])
print(all_cells)
with open("test.txt", 'wb') as f:
    f.write(bytes(all_cells))
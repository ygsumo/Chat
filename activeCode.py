import random
import string


def gene_activation_code(number, length):
    result = {}

    source = list(string.ascii_uppercase)
    for index in range(10):
        source.append(str(index))

    while len(result) < number:
        keys = ''
        for index in range(1,length):
            keys += random.choice(source)
            if index > 4 and index != length-1 and index % 5 == 0:
                keys += "-"

        if keys not in result:
            result[keys] = 1
    for key in result:
        print key
    return result

if __name__ == "__main__":
    gene_activation_code(200, 21)

import numpy as np


def readline_after_spaces(file):
    line = file.readline()
    while line == "\n":
        line = file.readline()
    return line


def input_tensor(filename):
    file = open(filename, 'r')
    size = int(readline_after_spaces(file))
    tensor = np.zeros((size, size, size))

    for i in range(size):
        for j in range(size):
            line = readline_after_spaces(file)
            elements = line.split()
            if len(elements) != size:
                raise Exception
            for k in range(size):
                tensor[i, j, k] = elements[k]
    return tensor


def print_tensor(tensor):
    for i in range(tensor.shape[0]):
        for j in range(tensor.shape[1]):
            for k in range(tensor.shape[2]):
                if i == j or i == k or k == j:
                    print("X ", end=" ")
                else:
                    print(str(int(tensor[i, j, k])) + " ", end=" ")
            print()
        print()


def tensor_completeness_check(tensor):
    for i in range(tensor.shape[0]):
        for j in range(tensor.shape[1]):
            for k in range(tensor.shape[2]):
                if i != j and i != k and k != j and tensor[i, j, k] != 1:
                    return False
    return True


def process_tensor_complement(tensor):
    tensor_complement = np.zeros((tensor.shape[0], tensor.shape[1], tensor.shape[2]))
    for i in range(tensor.shape[0]):
        for j in range(tensor.shape[1]):
            for k in range(tensor.shape[2]):
                if i == j or i == k or k == j:
                    pass
                elif tensor[i, j, k] == 1:
                    tensor_complement[i, j, k] = 0
                else:
                    tensor_complement[i, j, k] = 1
    return tensor_complement


def two_complex_complement(filename):
    try:
        tensor = input_tensor(filename)
        print("Original graph:")
        print_tensor(tensor)
        # print(tensor)
        if tensor_completeness_check(tensor):
            print("Graph is complete")
        else:
            print("Complement graph:")
            print_tensor(process_tensor_complement(tensor))
            # print(process_tensor_complement(tensor))
    except:
        print("Wrong input")
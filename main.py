from itertools import permutations
from copy import deepcopy


def is_diagonally_dominant(matrix, n):
    was = False
    for i in range(n):
        sum = 0
        for j in range(n):
            if j == i:
                continue
            sum -= abs(matrix[i][j])
        if sum > matrix[i][i]:
            return False
        if sum < matrix[i][i]:
            was = True
    return was


def permute_fast(matrix, n, start):
    if n - 1 == start:
        if is_diagonally_dominant(matrix, n):
            return True
        return False
    for j in range(start, n):
        sumr = 2 * abs(matrix[j][start])
        for k in range(n):
            sumr -= abs(matrix[j][k])
        if sumr >= 0:
            matrix[start], matrix[j] = matrix[j], matrix[start]
            ok = permute_fast(matrix, n, start + 1)
            if ok:
                return True
            matrix[j], matrix[start] = matrix[start], matrix[j]
    return False


def permute(matrix, n):
    id = [i for i in range(n)]
    for p in permutations(id):
        a = matrix.copy()
        for i in range(n):
            for j in range(int((n + 1) / 2)):
                a[i][p[j]], a[i][j] = a[i][j], a[i][p[j]]
        if is_diagonally_dominant(a, n):
            return True, a
    return False, None


def gauss_seidel(matrix, n, max_iterations, eps):
    x = [matrix[i][n] / matrix[i][i] for i in range(n)]
    d = []
    iterations = 0
    while iterations != max_iterations:
        iterations += 1
        new_x = x.copy()
        for i in range(n):
            s1 = sum(matrix[i][j] * new_x[j] for j in range(i))
            s2 = sum(matrix[i][j] * x[j] for j in range(i + 1, n))
            new_x[i] = (matrix[i][n] - s1 - s2) / matrix[i][i]
        d = [abs(x[i] - new_x[i]) for i in range(n)]
        if max(d) < eps:
            return iterations, new_x, d
        x = new_x
    return max_iterations + 1, x, d


def get_stdin_input():
    exp = 1
    while True:
        _exp = input("Enter accuracy(10**-n): ")
        try:
            _exp = int(_exp)
        except ValueError:
            print("Input isn't an integer number: ", _exp)
            continue
        if _exp <= 0:
            print("Expected int >= 0, got %d, please try again" % _exp)
            continue
        exp = _exp
        break

    n = 0
    while True:
        _n = input("Enter matrix dimension: ")
        try:
            _n = int(_n)
        except ValueError:
            print("Input isn't an integer number: ", _n)
            continue
        if _n <= 0:
            print("Expected int >= 0, got %d, please try again" % _n)
            continue
        n = _n
        break

    max_iter = 0
    while True:
        _max_iter = input("Enter max iterations: ")
        try:
            _max_iter = int(_max_iter)
        except ValueError:
            print("Input isn't an integer number: ", _max_iter)
            continue
        if _max_iter <= 0:
            print("Expected int >= 0, got %d, please try again" % _n)
            continue
        max_iter = _max_iter
        break

    matrix = []
    print("Please enter extended matrix(1 row in line):")
    for i in range(n):
        while True:
            row = (list(map(lambda x: x.lstrip().rstrip(), input().replace(",", ".").split(" "))))
            if len(row) != n + 1:
                print("Expected %d elements in row, got %d, please try again" % (n + 1, len(row)))
                continue
            float_row = []
            for j in range(len(row)):
                try:
                    float_row.append(float(row[j]))
                except ValueError:
                    print("%s isn't float number" % row[j])
                    continue
            matrix.append(float_row)
            break
    return exp, n, max_iter, matrix



def get_file_input(filename):
    file = None
    try:
        file = open(filename, "r")
    except OSError:
        print("Cannot open file")
        exit(1)

    exp = 1
    try:
        exp = int(file.readline())
    except ValueError:
        print("Accuracy input isn't an integer number: ", exp)
        exit(1)

    n = 1
    try:
        n = int(file.readline())
    except ValueError:
        print("Matrix dimension input isn't an integer number: ", n)
        exit(1)


    max_iter = 1
    try:
        max_iter = int(file.readline())
    except ValueError:
        print("Max iterations input isn't an integer number: ", max_iter)
        exit(1)

    matrix = []
    for i in range(n):
        row = (list(map(lambda x: x.lstrip().rstrip(), file.readline().replace(",", ".").split(" "))))
        if len(row) != n + 1:
            print("Expected %d elements in row, got %d, in line %d" % (n + 1, len(row), i))
            exit(1)
        float_row = []
        for j in range(len(row)):
            try:
                float_row.append(float(row[j]))
            except ValueError:
                print("%s isn't float number in row %d" % (row[j], i))
                exit(1)
        matrix.append(float_row)
    return exp, n, max_iter, matrix


exp, n, max_iter, matrix = 1, 1, 1, []
fileIn = input("Do you want to use file input? (y means yes): ")
if fileIn == "y":
    fileName = input("Please enter filename: ")
    exp, n, max_iter, matrix = get_file_input(fileName)
else:
    exp, n, max_iter, matrix = get_stdin_input()
matrix_copy = matrix.copy()
ok = permute_fast(matrix, n, 0)
if not ok:
    print("cannot make diagonally dominant matrix with fast algorithm, try with all rows permutations?(y for yes)")
    y = input()
    if y == "y":
        ok, ans = permute(matrix_copy, n)
    if not ok:
        print("Matrix cannot be diagonally dominant")
        exit(1)

print("Diagonally dominant matrix:")
for i in range(n):
    print(matrix[i])
iterations, ans, d = gauss_seidel(matrix, n, max_iter, 10**-exp)
if iterations > 20:
    print("Cannot find answer with this accuracy and max iterations")
    print("Error vector:")
    print(d)
    print("Current answer:")
    print(ans)
    exit(1)
print("iterations:", iterations)
print("Error vector:")
print(d)
print("answer:")
print(ans)


import argparse


def matrx_from_lines(lines: [str]) -> [[int]]: # type: ignore
    return [[int(num) for num in line.split(' ')] for line in lines]


def mult_matrices(matrix1: [[int]], matrix2: [[int]]) -> [[int]]: # type: ignore
    m = len(matrix1)
    n = len(matrix1[0])
    if len(matrix2) != n:
        raise Exception("Bad input: Unable to mult matrices with such sizes")
    k = len(matrix2[0])

    mult = []

    for i in range(m):
        mult.append([])
        for j in range(k):
            s = 0
            for t in range(n):
                s += matrix1[i][t] * matrix2[t][j]
            mult[i].append(s)

    return mult


def matrix_to_text(matrix):
    lines = [' '.join([str(digit) for digit in line]) for line in matrix]
    text = '\n'.join(lines)
    return text


def main():
    parser = argparse.ArgumentParser(description='Mult matrices')
    parser.add_argument('sourcePath', type=str, help='Matrices to mult')
    parser.add_argument('resultPath', type=str, help='Multiplication')

    args = parser.parse_args()
    source_path = args.sourcePath
    result_path = args.resultPath

    try:
        fin = open(source_path, 'r')
        input_lines = fin.readlines()
        fin.close()
    except Exception as ex:
        print(f'Reading failed: {ex}')
        return

    try:
        matrix1_lines = []
        matrix2_lines = []
        is_divider_met = False
        for line in input_lines:
            if line == "\n":
                is_divider_met = True
                continue

            if is_divider_met:
                matrix2_lines.append(line)
            else:
                matrix1_lines.append(line)

        matrix1 = matrx_from_lines(matrix1_lines)
        matrix2 = matrx_from_lines(matrix2_lines)
    except Exception as ex:
        print(f'Parsing failed: {ex}')
        return

    try:
        mult = mult_matrices(matrix1, matrix2)
    except Exception as ex:
        print(f'Multiplication failed: {ex}')
        return

    text = matrix_to_text(mult)

    try:
        fout = open(result_path, 'w')
        fout.write(text)
        fout.close()
    except Exception as ex:
        print(f'Writing output failed: {ex}')


main()
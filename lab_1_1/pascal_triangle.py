import argparse

def makeRow (row):
    row = [1] + row 
    for i in range (1, len(row)-1):
        row[i] += row[i+1]
    return row

parser = argparse.ArgumentParser(description='Draws pascal triangle of size N.')
parser.add_argument('integer1', metavar='N', type=int, nargs=1, help='An integer for the triangle size')

args = parser.parse_args()
n = args.integer1[0]

row = []
spaces = n
j=0
for i in range (0,n):
    row = makeRow(row)
    strRow = " ".join(str (element) for element in row)
    strRow = " " * spaces + strRow
    spaces -= 1
    print(strRow)
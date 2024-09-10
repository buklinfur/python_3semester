import argparse
import random

def bubbleSort (arr):
    arrSize = len(arr)
    for i in range (0, arrSize-1):
        alSorted = True
        for j in range (0, arrSize-1):
            if arr[j] > arr [j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                alSorted = False
        arrSize -= 1
        if alSorted:
            break
    return arr

parser = argparse.ArgumentParser(description='Sort a random integers list of size N.')
parser.add_argument('integer1', metavar='N', type=int, nargs=1, help='An integer for the list size')

args = parser.parse_args()
n = args.integer1[0]

arr = random.sample(range(2), counts = [n, n], k=n)
print ("Original array:", arr)

sortedArr = bubbleSort (arr)
print ("Result array:", sortedArr)
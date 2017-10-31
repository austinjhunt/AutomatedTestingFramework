#!/bin/python
import sys


def addTwoBinaries(binary1, binary2, result_length):
    value1_int = int(binary1[2:], 2)
    value2_int = int(binary2[2:], 2)
    ans = value1_int + value2_int
    ans_binary = bin(ans)
    if ans > 31:
        ans_binary = ans_binary[:2] + ans_binary[3:]

    while len(ans_binary) != (result_length + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]

    return ans_binary

if __name__ == "__main__":
    addTwoBinaries(0011, 0001, 4)

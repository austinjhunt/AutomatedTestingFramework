#!/bin/python
import sys



def checkIfOverflow(value1,value2):
    
    ans = int(value1, 2) + int(value2, 2)
    if ans > 31:
        return ("Yes (an overflow will occur)")
    else:
        return ("No overflow")



def main(argv): 
	values=sys.argv[1].split(",")
	oracle=sys.argv[2]
	assert checkIfOverflow(values[0],values[1])==oracle,"Error: 01111 + 01000 returned overflow"
	print("Test Case 3 Passed")

if __name__ == '__main__':
	import sys
	i = 0
	main(sys.argv[1:])


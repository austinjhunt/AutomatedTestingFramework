def cofc_decimal_to_ones_complement(_decimal_value, _length_of_binary):
    # First we get the binary of the "positive" version of the number
    #
    ans_binary = bin(int(abs(_decimal_value)))
    # Then we make it x number of bits where x is the 4th parameters in our list
    #
    while len(ans_binary) != (_length_of_binary + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]
        # If the number is negative, we flip all bits
        #
    if _decimal_value < 0:
        ans_binary = ans_binary.replace('0', 'x')
        ans_binary = ans_binary.replace('1', '0')
        ans_binary = ans_binary.replace('x', '1')
        ans_binary = '0' + ans_binary[1:]

    return ans_binary
    
def main(argv): 
	values=sys.argv[1].split(",")
	oracle = sys.argv[2]
	decToOnesComp = cofc_decimal_to_ones_complement(values[0],values[1])
	print(decToOnesComp) 
	#assert decToOnesComp==oracle,"Error: " + values[0] + ", " + values[1] + " did not return '" + oracle + "'"
	
	
if __name__ == '__main__':
	import sys
	main(sys.argv[1:])
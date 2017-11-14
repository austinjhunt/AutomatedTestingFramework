def cofc_ones_complement_to_decimal(_ones_complement_binary):
    # First we check if it's positive; if it is, we simply convert to decimal
    #
    _ones_complement_binary = int(_ones_complement_binary)
    if _ones_complement_binary[2] == '0':
        ans_decimal = int(_ones_complement_binary[2:], 2)
    else:
        # First we swap the 0s with 1s and vice versa
        #
        _ones_complement_binary = _ones_complement_binary.replace('0', 'x')
        _ones_complement_binary = _ones_complement_binary.replace('1', '0')
        _ones_complement_binary = _ones_complement_binary.replace('x', '1')

        # Now we convert to decimal
        #
        ans_decimal = int(_ones_complement_binary[2:], 2) * -1

    return ans_decimal
    
    
    #this one may give a problem, only one param
def main(argv): 
	#values=sys.argv[1].split(",")
	oracle = sys.argv[2]
	onesCompToDec = cofc_ones_complement_to_decimal(argv[1])
	print(onesCompToDec) 
	#assert onesComptToDec==oracle,"Error: " + argv[1] + " did not return '" + oracle + "'"
	
	
if __name__ == '__main__':
	import sys
	main(sys.argv[1:])
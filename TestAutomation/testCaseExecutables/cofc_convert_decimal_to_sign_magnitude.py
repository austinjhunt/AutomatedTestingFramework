#TESTMETHOD
def cofc_convert_decimal_to_sign_magnitude(_decimal_value, _length_of_binary):
    decimal_value = int(_decimal_value)
    intLength = int(_length_of_binary)
    ans_binary = bin(int(abs(decimal_value)))
    # Then we make it x number of bits where x is the 4th parameters in our list
    #
    while len(ans_binary) != (intLength + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]
        # Finally, we make the MSB 1 if the number is negative, otherwise do nothing
        #
    if decimal_value <= 0: #was < 
        ans_binary = ans_binary[0:2] + '1' + ans_binary[3:]

    return ans_binary

#MAIN
def main(argv): 
	values=sys.argv[1].split(",")
	oracle = sys.argv[2]
	decToSign = cofc_convert_decimal_to_sign_magnitude(values[0],values[1])
	print(decToSign)
    #assert decToSign==oracle,"Error: " + values[0] + "," + values[1] + " did not return '" + oracle + "'"
	
	
	
if __name__ == '__main__':
	import sys
	main(sys.argv[1:])

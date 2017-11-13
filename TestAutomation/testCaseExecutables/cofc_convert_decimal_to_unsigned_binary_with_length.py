
#!/bin/python

def cofc_convert_decimal_to_unsigned_binary_with_length(_decimal_value, _length_of_binary):
    ans_binary = bin(_decimal_value)
    while len(ans_binary) < (_length_of_binary + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]

    # Remove MSB
    if len(ans_binary) > (_length_of_binary + 2):
        ans_binary = ans_binary[0:2] + ans_binary[3:]

    return ans_binary

    
def main(argv): 
	values=sys.argv[1].split(",")
	oracle = sys.argv[2]
	assert cofc_convert_decimal_to_unsigned_binary_with_length(values[0],values[1])==oracle,"Error: " + values[0] + ", " + values[1] + " did not return '" + oracle + "'"
	print(oracle)	
	
if __name__ == '__main__':
	import sys
	main(sys.argv[1:])


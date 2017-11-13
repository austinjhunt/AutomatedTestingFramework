def convert_simple_line_c_to_mips(_one_line):
    # First we separate by spaces
    #
    my_comps = _one_line.split(' ')

    # We use [:-1] to get rid of the semi-colon
    #
    if my_comps[0] == 'int':
        return 'addi $' + my_comps[1] + ', $zero, ' + my_comps[3][:-1]
    elif my_comps[3] == '+' and my_comps[4][:-1].isdigit():
        return 'addi $' + my_comps[0].replace('\t', '') + ", $" + my_comps[2] + ", " + my_comps[4][:-1]
    elif my_comps[3] == '-' and my_comps[4][:-1].isdigit():
        return 'addi $' + my_comps[0].replace('\t', '') + ", $" + my_comps[2] + ", -" + my_comps[4][:-1]
    elif my_comps[3] == '+' and not my_comps[4][:-1].isdigit():
        return 'add $' + my_comps[0].replace('\t', '') + ", $" + my_comps[2] + ", $" + my_comps[4][:-1]
    elif my_comps[3] == '-' and not my_comps[4][:-1].isdigit():
        return 'sub $' + my_comps[0].replace('\t', '') + ", $" + my_comps[2] + ", $" + my_comps[4][:-1]


def main(argv): 
	#values=sys.argv[1].split(",")
	oracle = sys.argv[2]
	assert convert_simple_line_c_to_mips(argv[1])==oracle,"Error: " + argv[1] + "did not return '" + oracle + "'"
	print(oracle)	
	
if __name__ == '__main__':
	import sys
	main(sys.argv[1:])
def binaryTwosComplementFromDecimal(_decimal_value, _bitstring_length):
    # Here's how we convert from decimal to two's complement (from web)
    #
    ans_binary = bin(int(_decimal_value) & int('0b' + '1' * int(_bitstring_length), 2))

    # Then we make it x number of bits where x is the 4th parameters in our list if it's negative, it will
    # not be less than x number of bits, therefore, we can add 0's (positive number)
    #
    while len(ans_binary) != (_bitstring_length + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]

    return ans_binary
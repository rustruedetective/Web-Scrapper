import re

def has_numbers(inputString):
    """ Checks if a string has numbers in it or not. """
    
    return any(char.isdigit() for char in inputString)



def split_alpha_numbers(str):
    """ Splits any text that contains a number or text.
        Returns them as a tuple of (text, numbers). """

    match = re.search(r'([\D]+)([\d]+)|([\d]+)([\D]+)', str)
    tup = (match.group(1), match.group(2))
    tup2 = (match.group(4), match.group(3))
    if tup[0] == None:
        return tup2
    return tup



def split_numbers_alpha(str):
    """ Splits any text that contains a number or text.
        Returns them as a tuple of (numbers, text). """

    match = re.search(r'([\D]+)([\d]+)|([\d]+)([\D]+)', str)
    tup = (match.group(2), match.group(1))
    tup2 = (match.group(3), match.group(4))
    if tup[0] == None:
        return tup2
    return tup
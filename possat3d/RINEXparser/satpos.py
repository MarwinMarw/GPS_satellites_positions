import math
from os import read

GM = 3.986005*pow(10.0,14)
c = 2.99792458*pow(10.0,8)
omegae_dot = 7.2921151467*pow(10.0,-5)


def split_neg_num(number, start_index=0):
    index_minus = number.find('-', start_index)
    fixed = []

    if index_minus > 0 and not number[index_minus-1].isalpha():
        num1 = number[:index_minus]
        num2 = number[index_minus:]

        fixn1 = split_neg_num(num1)
        fixn2 = split_neg_num(num2)
        
        if fixn1 is None:
            fixed.append(num1)
        else:
            for i in fixn1:
                fixed.append(i)

        if fixn2 is None:
            fixed.append(num2)
        else:
            for i in fixn2:
                fixed.append(i)

        return fixed

    else:    
        if index_minus != -1:
            return split_neg_num(number, index_minus+1)
        else:
            return None


def read_rinex(filename):
    rinex_file = open(filename, 'r')
    sattelites = {}

    #skip header
    while True:
        if 'END' in rinex_file.readline().split(' '):
            break
    #end header
    
    for line in rinex_file:
        split_line = line.split(' ')
        


    rinex_file.close()

def process_RINEX_file(filename):
    read_rinex(filename)
import numpy as np
import sys
import time
import csv

# project done in group of three,
# Griffin Storback - V00849885
# Jeffrey Olmstead - V00852585
# Dallas Brooks - V00

t0 = time.time()

if (len(sys.argv) != 2):
    print("Wrong number of parameters.")
    print("File should be run with one parameter; the name of the file")
    exit()

f = open(sys.argv[1])

for line in f:
    line_values = line.rsplit(",")
    event = line_values[5]
    secondary_type = line_values[6]
    x = line_values[7]
    y = line_values[8]
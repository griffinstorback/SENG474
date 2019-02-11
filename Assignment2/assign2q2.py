import numpy as np
import sys
import time

# Assignment done with homework partner,
# Griffin Storback - V00849885
# Jeffrey Olmstead - V00852585

t0 = time.time()

if (len(sys.argv) != 2):
    print("Wrong number of parameters.")
    print("File should be run with one parameter; the name of the file")
    exit()

f = open(sys.argv[1])

# Number of data points
N = int(f.readline())

# Number of features
D = int(f.readline())

# Number of epochs
T = 200

# Learning rate
n = 0.000001

# Read the line with label and headers
f.readline()

lines = [line.rstrip("\n") for line in f]

X = np.empty((N, D), dtype=float)
Y = np.empty(N, dtype=float)

#X = np.c_[np.ones((len(X), 1)), X]

for i in range(1, N):
    columns = lines[i].split("\t")
    Y[i] = columns[0]
    for j in range(0, D):
        X[i][j] = columns[j+1]

W = np.random.random_sample(D)

for i in range(0,T):
    
    T1 = time.time()

    Y_prediction = X.dot(W)
    adj = (Y - Y_prediction).dot(X)
    W = W + n/N * adj

    #for j in range(0, D):   
        #adj = 0
        #for k in range(0, N):
        #    adj = adj + ((Y[k] - X[k].dot(W)) * X[k][j])
        #W[j] = W[j] + n/N * adj

    T2 = time.time()
    print("done epoch in " + str(T2 - T1) + " seconds")


print(W)

t1 = time.time()

print("Total time: " + str(t1 - t0) + " seconds.")

P = X.dot(W).reshape(-1)
E = Y - P
q = 0
for e in E:
    q = q + e ** 2

print("Loss: " + str(q / (2*N)))

exit(0)
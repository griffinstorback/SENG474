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

# Read the line with label and headers
f.readline()

lines = [line.rstrip("\n") for line in f]

X = np.empty((N, D), dtype=float)
Y = np.empty(N, dtype=float)

for i in range(1, N):
    columns = lines[i].split("\t")
    Y[i] = columns[0]
    for j in range(0, D):
        X[i][j] = columns[j+1]

W = np.linalg.solve(X.T.dot(X), X.T.dot(Y))

t1 = time.time()

print("Total time: " + str(t1 - t0) + " seconds.")

P = X.dot(W).reshape(-1)
print(P)
E = Y - P
print(E)

q = 0
for e in E:
    q = q + e ** 2


print("Loss: " + str(q / (2*N)))

print(W)

exit(0)
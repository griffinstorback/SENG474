import numpy as np
import sys
import time
import csv

# Assignment done with homework partner,
# Griffin Storback - V00849885
# Jeffrey Olmstead - V00852585

t0 = time.time()

if (len(sys.argv) != 2):
    print("Wrong number of parameters.")
    print("File should be run with one parameter; the name of the file")
    exit()


# Set n and m values, for width and height of utility matrix
n = 943
m = 1682

# Open the file
f = open(sys.argv[1])

def rmse(matrix1, matrix2):
    rmse = np.sqrt(((matrix1 - matrix2) ** 2).mean())
    return rmse

def kth_column_U(M, U, V, i, k):
    s = 0
    divisor = 0

    for j in range(0, m):
        # if customer i rated item j
        if M[i][j]:

            s += (U[i].dot(V.T[j]) - (U[i][k] * V[k][j]) - M[i][j]) * V[k][j]
            divisor += V[k][j] * V[k][j]
    
    return -(s / divisor)

def kth_row_V(M, U, V, j, k):
    s = 0
    divisor = 0

    for i in range(0, n):
        # if customer i rated item j
        if M[i][j]:
            s += (U[i].dot(V.T[j]) - (U[i][k] * V[k][j]) - M[i][j]) * U[i][k]
            divisor += U[i][k] * U[i][k]
    
    return -(s / divisor)





# Construct utility matrix
M = np.empty((n, m))
for line in f:
    user_id, movie_id, rating, timestamp = map(int, line.rsplit('\t'))

    # need to take the id - 1 to fit the matrix, will add back after
    M[user_id-1][movie_id-1] = rating

# Initialize U and V
d = 20
U = np.random.rand(n, d)
V = np.random.rand(d, m)

# Perform T times
T = 20
for _ in range(0, 1):#T):
    
    for k in range(0, d):

        for i in range(0, n):
            U[i, k] = kth_column_U(M, U, V, i, k)

    for k in range(0, d):

        for i in range(0, m):
            V[k, i] = kth_row_V(M, U, V, i, k)
    
    print(rmse(U.dot(V), M))

t1 = time.time()
print("Took " + str(t1-t0) + " seconds.")

exit(0)

# Open file to write to
with open("blank.blank", 'wt') as output_file:
    tsv_writer = csv.writer(output_file, delimiter='\t')

    # Write headers
    tsv_writer.writerow("replace")

    # Write values
    tsv_writer.writerow("with real values")

exit(0)
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

# Construct utility matrix
M = np.empty((n, m))

# Contains all movies rated by given user
user_rated = dict()

# Contains all users who rated a given movie
movie_rated = dict()

for line in f:
    user_id, movie_id, rating, timestamp = map(int, line.rsplit('\t'))
    
    M[user_id-1][movie_id-1] = rating

    if user_id-1 not in user_rated:
        user_rated[user_id-1] = []
    user_rated[user_id-1].append(movie_id-1)

    if movie_id-1 not in movie_rated:
        movie_rated[movie_id-1] = []
    movie_rated[movie_id-1].append(user_id-1)


def rmse():
    known_cells = 0
    s = 0

    for i in range(0, n):
        for j in range(0, m):
            if j in user_rated[i]:
                known_cells += 1
                s += (U[i].dot(V.T[j]) - M[i][j]) ** 2

    return np.sqrt(s/known_cells)

def kth_column_U(M, U, V, i, k):
    s = 0
    divisor = 0

    # for each movie j rated by user i
    for j in user_rated[i]:
        
        s += (U[i].dot(V.T[j]) - (U[i][k] * V[k][j]) - M[i][j]) * V[k][j]
        divisor += V[k][j] * V[k][j]
    
    return -(s / divisor)

def kth_row_V(M, U, V, j, k):
    s = 0
    divisor = 0

    # for each user i who rated movie j
    for i in movie_rated[j]:
        
        s += (U[i].dot(V.T[j]) - (U[i][k] * V[k][j]) - M[i][j]) * U[i][k]
        divisor += U[i][k] * U[i][k]
    
    return -(s / divisor)


# Initialize U and V
d = 20
U = np.random.rand(n, d)
V = np.random.rand(d, m)

# Perform T times
T = 20
for _ in range(0, T):
    
    for k in range(0, d):

        for i in range(0, n):
            U[i][k] = kth_column_U(M, U, V, i, k)

    for k in range(0, d):

        for j in range(0, m):
            V[k][j] = kth_row_V(M, U, V, j, k)
    
    print(rmse())

t1 = time.time()
print("Took " + str(t1-t0) + " seconds.")

# Output file headers
output_columns = []
output_columns.append("UserId")
for i in range(0, d):
    output_columns.append(i+1)

# Open file to write to
with open("UT.tsv", 'wt') as output_file:
    tsv_writer = csv.writer(output_file, delimiter='\t')

    # Write headers
    tsv_writer.writerow(output_columns)

    # Write values
    for i in range(0, n):
        row = []
        row.append(i+1)
        row.extend(U[i])
        tsv_writer.writerow(row)

# Open second file to write to
output_columns[0] = "MovieId"
with open("VT.tsv", 'wt') as output_file:
    tsv_writer = csv.writer(output_file, delimiter='\t')

    # Write headers
    tsv_writer.writerow(output_columns)

    # Write values
    for i in range(0, m):
        row = []
        row.append(i+1)
        row.extend(V.T[i])
        tsv_writer.writerow(row)

exit(0)
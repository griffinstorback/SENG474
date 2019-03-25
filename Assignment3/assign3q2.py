import numpy as np
import sys
import time
import csv
import operator
import Queue

# Assignment done with homework partner,
# Griffin Storback - V00849885
# Jeffrey Olmstead - V00852585

t0 = time.time()

if (len(sys.argv) != 2):
    print("Wrong number of parameters.")
    print("File should be run with one parameter; the name of the file")
    exit()

f = open(sys.argv[1])

# Taxation parameter
B = 0.85

# Number of iterations
T = 10

# Read past the first 4 lines of the file, as they are comments.
for i in range(0,4):
    f.readline()

lines = [line.rstrip("\n") for line in f]

in_nodes = dict()
out_nodes = dict()
for line in lines:
    from_node, to_node = map(int, line.split('\t'))

    if from_node not in out_nodes:
        out_nodes[from_node] = []
    out_nodes[from_node].append(to_node)

    if to_node not in in_nodes:
        in_nodes[to_node] = []
    in_nodes[to_node].append(from_node)

# Add all nodes to D, their value being the degree of their outgoing nodes.
D = dict()
# At the same time, add deadend nodes to the queue q.
q = Queue.Queue()
for node in out_nodes:
    D[node] = len(out_nodes[node])
for node in in_nodes:
    if node not in D:
        D[node] = 0
        q.put(node)

# Number of nodes, to determine name of the file.
number_of_rows = len(D)
output_filename = "PR_" + str(number_of_rows/1000) + "k.tsv"

# List containing deadends.
L = list()

# Boolean dictionary telling whether item at index is in L.
M = dict()
for node in D:
    M[node] = False

# For each deadend, check if any of its incoming nodes are deadends as well.
while not q.empty():
    i = q.get()
    if not M[i]:
        L.append(i)
        M[i] = True

        # if there are no nodes pointing to the current node
        if i not in in_nodes:
            continue
        
        for j in in_nodes[i]:
            D[j] = D[j] - 1

            if D[j] == 0:
                q.put(j)

# Remove dead end nodes from D, and set n to be length of D (number of non-dead-end pages)
for i in L:
    D.pop(i, None)
n = len(D)

# Initialize dictionary to contain rank of each page, each initialized to 1/n
V = dict()
for i in D:
    V[i] = 1/float(n)
for i in L:
    V[i] = 1/float(n)

# Calculate page rank
for k in range(0, T):

    # Make a copy of V to refer to the previous rounds' values.
    V_prev = V.copy()

    for i in D:
        rank = 0
        if i in in_nodes:
            for j in in_nodes[i]:
                rank = rank + (V_prev[j] / len(out_nodes[j])) + ((1 - B) / n)
        
        V[i] = B * rank

    # Calculate page rank of dead ends
    for i in L:
        rank = 0
        if i in in_nodes:
            for j in in_nodes[i]:
                rank = rank + (V_prev[j] / len(out_nodes[j]))
        
        V[i] = rank

# Sort the pages by the smallest pagerank value
sorted_V = sorted(V.items(), key=operator.itemgetter(1))

# We want pages ordered by largest pagerank value, so reverse it
sorted_V.reverse()

# Open file to write to
with open(output_filename, 'wt') as output_file:
    tsv_writer = csv.writer(output_file, delimiter='\t')

    # Write headers for the 2 columns
    tsv_writer.writerow(['PageRank', 'Ids'])

    # Write each row
    for i in sorted_V:
        tsv_writer.writerow([i[1], i[0]])

t2 = time.time()

print("Wrote to: " + output_filename)
print("Took " + str(t2-t0) + " seconds.")
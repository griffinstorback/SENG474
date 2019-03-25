import numpy as np
import sys
import time
import csv
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
output_filename = "deadends_" + str(number_of_rows/1000) + "k.tsv"

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

# Open file to write to
with open(output_filename, 'wt') as output_file:
    tsv_writer = csv.writer(output_file, delimiter='\t')

    # Write each row
    for i in L:
        tsv_writer.writerow([i])

t1 = time.time()

print("Wrote to: " + output_filename)
print("Took " + str(t1-t0) + " seconds.")
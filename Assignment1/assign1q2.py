import sys
import csv
import uuid
import fnv
import numpy as np
import time

# Assignment done with homework partner,
# Griffin Storback - V00849885
# Jeffrey Olmstead - V00852585


t0 = time.time()
if (len(sys.argv) != 2):
    print("Wrong number of parameters.")
    print("File should be run with one parameter; the name of the file")
    exit()

# Threshold
x = 0.6

# Number of hash tables
b = 14

# Size of minhash signature
r = 6

# Large prime number
p = 15373875993579943603

# Initialize a and b values for hash functions.
a_values = []
b_values = []
for i in range(0, b*r):
    a_values.append(uuid.uuid4().int & (1<<64)-1)
    b_values.append(uuid.uuid4().int & (1<<64)-1)


def jaccard_similarity(a, b):
    result = float(len(a.intersection(b)) / len(a.union(b)))
    return result

f = open(sys.argv[1], encoding="utf8")

# Read the first line (consists of headers) so it is not a part of the questions list
f.readline()

lines = [line.rstrip("\n") for line in f]

# Initialize dictionary containing the qid + question and array of words
qid_questions = dict()
words = []
for line in lines:
    if len(line.split('\t')) == 2:
        qid, question = line.split('\t')
        qid_questions[qid] = question
        for word in question.split(' '):
            words.append(word)

# Intialize dictionary which will contain qid + qids of similar questions
qid_similarities = dict()
temp_similarities = dict()
signatures = dict()
for qid in qid_questions:
    qid_similarities[qid] = list()
    temp_similarities[qid] = list()
    signatures[qid] = list()


t1 = time.time()
print("Initialization done: " + str(t1-t0))


### Create min hash signatures
# For each question
for qid in qid_questions:
    signature = []
    words = qid_questions[qid].split(' ')
    
    # First, initialize the list of words converted to int.
    word_nums = [None] * len(words)
    for k in range(0, len(words)):
        word_nums[k] = fnv.hash(words[k].encode('utf-8'), bits=64)

    # For each hash function
    for i in range(0, b*r):
        min_hash = p + 1

        # For each word in the question
        for word in word_nums:
            hash_value = (a_values[i] * word + b_values[i]) % p

            # min_hash represents the word with smallest hash value for this hash function.
            if hash_value < min_hash:
                min_hash = hash_value
        signature.append(min_hash)
    signatures[qid] = signature


t2 = time.time()
print("Minhash signatures created: " + str(t2-t0))


### Create candidate pairs
candidate_pairs = []
# For each band
for i in range(0,b):
    q_hashes_for_band = dict()

    # For each signature
    for qid in signatures:
        hash_value = hash(tuple(signatures[qid][i*r: i*r + r]))

        # Add each hash value to a dictionary with hash as key and list of colliding qids as value.
        if hash_value not in q_hashes_for_band:
            q_hashes_for_band[hash_value] = []
        q_hashes_for_band[hash_value].append(qid)

    # Check created hash values for collisions, which will form the candidate pairs.
    for hash_value in q_hashes_for_band:
        if len(q_hashes_for_band[hash_value]) > 1:

            # Nested for-loops look bad, but only run on hash indexes that more than one question hashed to
            for qid in q_hashes_for_band[hash_value]:
                for qid2 in q_hashes_for_band[hash_value]:
                    if qid != qid2:
                        candidate_pairs.append((qid,qid2))


t3 = time.time()
print("Candidate pairs created: " + str(t3-t0))


# Calculate jaccard similarity of the signatures of the candidate pairs found.
for qid, qid2 in candidate_pairs:
    if jaccard_similarity(set(signatures[qid]), set(signatures[qid2])) > x:
        if qid2 not in temp_similarities[qid]:
            temp_similarities[qid].append(qid2)

# Eliminate false positives.
for qid in temp_similarities:
    if len(temp_similarities[qid]) >= 1:
        for qid2 in temp_similarities[qid]:
            if jaccard_similarity(set(qid_questions[qid].split(' ')), set(qid_questions[qid2].split(' '))):
                qid_similarities[qid].append(qid2)



t4 = time.time()
print("Comparisons done: " + str(t4-t0))

if (sys.argv[1] == "question_4k.tsv"):
    output_filename = "question_sim_4k.tsv"
elif (sys.argv[1] == "question_50k.tsv"):
    output_filename = "question_sim_50k.tsv"
elif (sys.argv[1] == "question_150k.tsv"):
    output_filename = "question_sim_150k.tsv"
elif (sys.argv[1] == "question_290k.tsv"):
    output_filename = "question_sim_290k.tsv"
else:
    output_filename = "question_sim_unknown_input_file.tsv"

# Open file to write to
with open(output_filename, 'wt') as output_file:
    tsv_writer = csv.writer(output_file, delimiter='\t')

    # Write headers for the 2 columns
    tsv_writer.writerow(['qid', 'similar-qids'])

    # Write each row
    for qid in qid_similarities:
        if len(qid_similarities) != 0:
            tsv_writer.writerow([qid, ', '.join(qid_similarities[qid])])
        else:
            tsv_writer.writerow([qid, ' '])

t5 = time.time()
print("Wrote to file " + output_filename + " in " + str(t5-t0) + " seconds.")

exit()
import sys
import csv
import time

# Assignment done with homework partner,
# Griffin Storback - V00849885
# Jeffrey Olmstead - V00852585

if (len(sys.argv) != 2):
    print("Wrong number of parameters.")
    print("File should be run with one parameter; the name of the file")
    exit()

threshold = 0.6

t0 = time.time()

def jaccard_similarity(str1, str2):
    str1 = set(str1.split(' '))
    str2 = set(str2.split(' '))
    result = float(len(str1.intersection(str2)) / len(str1.union(str2)))
    return result


f = open(sys.argv[1], encoding="utf8")

# Read the first line (consists of headers) so it is not a part of the questions list
f.readline()

lines = [line.rstrip("\n") for line in f]

# Initialize dictionary containing the qid + question
qid_questions = dict()
for line in lines:
    if len(line.split('\t')) == 2:
        qid, question = line.split('\t')
        qid_questions[qid] = question

# Intialize dictionary which will contain qid + qids of similar questions
qid_similarities = dict()
for qid in qid_questions:
    qid_similarities[qid] = list()

# Compare each question against all other questions
for qid in qid_questions:
    for qid2 in qid_questions:
        if (qid != qid2 and jaccard_similarity(qid_questions[qid], qid_questions[qid2]) > threshold):
            qid_similarities[qid].append(qid2)


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

t1 = time.time()
print("Wrote to file " + output_filename + " in " + str(t1 - t0) + " seconds.")

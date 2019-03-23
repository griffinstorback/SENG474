import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import csv

# project done in group of three,
# Griffin Storback - V00849885
# Jeffrey Olmstead - V00852585
# Dallas Brooks - V00868024

t0 = time.time()

if (len(sys.argv) != 2):
    print("Wrong number of parameters.")
    print("File should be run with one parameter; the name of the file")
    exit()

f = open(sys.argv[1])

shot_counts = dict()
goal_counts = dict()
goal_positions_x = dict()
goal_positions_y = dict()

shot_counts["Snap Shot"] = 0
goal_counts["Snap Shot"] = 0
shot_counts["Slap Shot"] = 0
goal_counts["Slap Shot"] = 0
shot_counts["Wrist Shot"] = 0
goal_counts["Wrist Shot"] = 0
shot_counts["Wrap-around"] = 0
goal_counts["Wrap-around"] = 0
shot_counts["Tip-In"] = 0
goal_counts["Tip-In"] = 0
shot_counts["Backhand"] = 0
goal_counts["Backhand"] = 0
shot_counts["Deflected"] = 0
goal_counts["Deflected"] = 0

goal_positions_x["Snap Shot"] = list()
goal_positions_x["Slap Shot"] = list()
goal_positions_x["Wrist Shot"] = list()
goal_positions_x["Wrap-around"] = list()
goal_positions_x["Tip-In"] = list()
goal_positions_x["Backhand"] = list()
goal_positions_x["Deflected"] = list()

goal_positions_y["Snap Shot"] = list()
goal_positions_y["Slap Shot"] = list()
goal_positions_y["Wrist Shot"] = list()
goal_positions_y["Wrap-around"] = list()
goal_positions_y["Tip-In"] = list()
goal_positions_y["Backhand"] = list()
goal_positions_y["Deflected"] = list()

for line in f:
    line_values = line.rsplit(",")
    event = line_values[5].strip('\"')
    secondary_type = line_values[6].strip('\"')
    x = line_values[7].strip('\"')
    y = line_values[8].strip('\"')

    if event == "Goal" and secondary_type != "NA":
        goal_counts[secondary_type] += 1
        goal_positions_x[secondary_type].append(x)
        goal_positions_y[secondary_type].append(y)
    elif event == "Shot" and secondary_type != "NA":
        shot_counts[secondary_type] += 1


slap_average = 1.0 * goal_counts["Slap Shot"] / (goal_counts["Slap Shot"] + shot_counts["Slap Shot"])
snap_average = 1.0 * goal_counts["Snap Shot"] / (goal_counts["Snap Shot"] + shot_counts["Snap Shot"])
wrist_average = 1.0 * goal_counts["Wrist Shot"] / (goal_counts["Wrist Shot"] + shot_counts["Wrist Shot"])
wrap_average = 1.0 * goal_counts["Wrap-around"] / (goal_counts["Wrap-around"] + shot_counts["Wrap-around"])
tip_average = 1.0 * goal_counts["Tip-In"] / (goal_counts["Tip-In"] + shot_counts["Tip-In"])
backhand_average = 1.0 * goal_counts["Backhand"] / (goal_counts["Backhand"] + shot_counts["Backhand"])
deflected_average = 1.0 * goal_counts["Deflected"] / (goal_counts["Deflected"] + shot_counts["Deflected"])

print("Slap average: " + str(100 * slap_average))
print("Snap average: " + str(100 * snap_average))
print("Wrist average: " + str(100 * wrist_average))
print("Wrap average: " + str(100 * wrap_average))
print("Tip average: " + str(100 * tip_average))
print("Backhand average: " + str(100 * backhand_average))
print("Deflected average: " + str(100 * deflected_average))

fig, ax = plt.subplots()
plt.xlim(-100, 100)
plt.ylim(-60, 60)

ax.scatter(goal_positions_x["Snap Shot"], goal_positions_y["Snap Shot"])

plt.show()
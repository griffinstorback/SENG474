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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def print_goal_averages():
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

    return

def scatter_goal_locations():
    xx, yy = zip(*goal_positions["Slap Shot"])
    plt.scatter(xx, yy, color="blue")
    xx, yy = zip(*goal_positions["Snap Shot"])
    plt.scatter(xx, yy, color="red")
    xx, yy = zip(*goal_positions["Deflected"])
    plt.scatter(xx, yy, color="orange")
    xx, yy = zip(*goal_positions["Wrist Shot"])
    plt.scatter(xx, yy, color="green")
    xx, yy = zip(*goal_positions["Backhand"])
    plt.scatter(xx, yy, color="yellow")
    xx, yy = zip(*goal_positions["Tip-In"])
    plt.scatter(xx, yy, color="cyan")
    xx, yy = zip(*goal_positions["Wrap-around"])
    plt.scatter(xx, yy, color="magenta")

    plt.show()

    return

#
# Load data
#

if (len(sys.argv) != 2):
    print("Wrong number of parameters.")
    print("File should be run with one parameter; the name of the file")
    exit()

f = open(sys.argv[1])

shot_counts, goal_counts, goal_positions = dict(), dict(), dict()

shot_counts["Snap Shot"], shot_counts["Slap Shot"], shot_counts["Wrist Shot"], shot_counts["Wrap-around"], shot_counts["Tip-In"], \
    shot_counts["Backhand"], shot_counts["Deflected"] = 0, 0, 0, 0, 0, 0, 0
goal_counts["Snap Shot"], goal_counts["Slap Shot"], goal_counts["Wrist Shot"], goal_counts["Wrap-around"], goal_counts["Tip-In"], \
    goal_counts["Backhand"], goal_counts["Deflected"] = 0, 0, 0, 0, 0, 0, 0

goal_positions["Snap Shot"], goal_positions["Slap Shot"], goal_positions["Wrist Shot"], goal_positions["Wrap-around"], \
    goal_positions["Tip-In"], goal_positions["Backhand"], goal_positions["Deflected"] = list(), list(), list(), list(), list(), list(), list()

for line in f:
    line_values = line.rsplit(",")
    event = line_values[5].strip('\"')
    secondary_type = line_values[6].strip('\"')
    x = line_values[7].strip('\"')
    y = line_values[8].strip('\"')
    
    if event == "Goal" and secondary_type != "NA":
        goal_counts[secondary_type] += 1
        if is_number(x) and is_number(y):
            x = float(x)
            y = float(y)
            goal_positions[secondary_type].append((x,y))
    elif event == "Shot" and secondary_type != "NA":
        shot_counts[secondary_type] += 1

#
# Do something to data
#

# Print goal averages for each type of shot
print_goal_averages()

# Scatter goal locations, colored by their type
scatter_goal_locations()


# Cluster goals wrt each quadrant of ice
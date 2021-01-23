import datetime
import os

# -------- Transfer today's data to "smile_data.csv" -------- #

data = ""
date = ""
with open(os.path.dirname(os.path.abspath(__file__)) + "/today.csv", "r") as f:
    total = 0
    date = ""
    i = 0
    for line in f.readlines():
        d, v = line.split(",")
        total += float(v)
        date = d
        i += 1

    date = datetime.datetime.strptime(date, "%Y/%m/%d %H:%M:%S")
    average_smile = total / i


with open(os.path.dirname(os.path.abspath(__file__)) + "/smile_data.csv", "a") as f:
    f.write(f"{date},{average_smile}\n")

# Delete today's file to update everyday.
os.remove(os.path.dirname(os.path.abspath(__file__) + "/today.csv"))

import csv
import re
import os, sys

def regex(s, index):

    # starting from one
    index = str(index + 1)

    # separating two different line types
    if s.find("GR3D_FREQ") == -1:

        # creating a regex expression
        reg = r"RAM\s(\d{4})/(\d{4})MB .{11} CPU \[(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|)\] BCPU@(\d+\.?\d*C) MCPU@(\d+\.?\d*C) GPU@(\d+\.?\d*C) .*"

        # calculating ram usage percentage
        ram_percentage = str(int(100 * (int(re.sub(reg, r"\1", s)) / int(re.sub(reg, r"\2", s)))))

        return re.sub(
            reg,
            index
            + r",\1,\2,"
            + ram_percentage
            + r",\3,\5,\7,\9,\11,\13,\4,\6,\8,\10,\12,\14,,,\15,\16,\17",
            s
        )

    # creating a regex expression
    reg = r"RAM\s(\d{4})/(\d{4})MB .{11} CPU \[(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|),(\d{1,3}%|off)@?(\d+,?|)\] EMC_FREQ \d+%@\d+ GR3D_FREQ (\d+%)@?(\d+) APE \d+ MTS fg \d+% bg \d+% BCPU@(\d+\.?\d*C) MCPU@(\d+\.?\d*C) GPU@(\d+\.?\d*C) .*"

    # calculating ram usage percentage
    ram_percentage = str(int(100 * (int(re.sub(reg, r"\1", s)) / int(re.sub(reg, r"\2", s)))))

    return re.sub(
        reg,
        index
        + r",\1,\2,"
        + ram_percentage
        + r",\3,\5,\7,\9,\11,\13,\4,\6,\8,\10,\12,\14,\15,\16,\17,\18,\19",
        s
    )


def main():

    # making a list to insert to csv file
    row_list = list()
    first_row = [
        "index",
        "RAM usage",
        "RAM amount",
        "RAM usage percentage",
        "CPU 1 usage",
        "CPU 2 usage",
        "CPU 3 usage",
        "CPU 4 usage",
        "CPU 5 usage",
        "CPU 6 usage",
        "CPU 1 frequency",
        "CPU 2 frequency",
        "CPU 3 frequency",
        "CPU 4 frequency",
        "CPU 5 frequency",
        "CPU 6 frequency",
        "GPU usage",
        "GPU frequency",
        "BCPU temperature",
        "MCPU temperature",
        "GPU temperature"
    ]

    # opening log file
    if os.path.exists("tegrastats.log"):
        file = open("tegrastats.log", "r")
        lines = file.readlines()
    else:
        print("log file not found")
        sys.exit()

    # adding info from txt file to list
    for i in range(len(lines)):
        s = regex(lines[i], i).split(",")
        row_list.append(s)

    # inserting list into csv file
    with open("test.csv", "w", newline="") as file:
        writer = csv.writer(file)

        # writing first row
        writer.writerow(first_row)

        # writing the rest of the info
        writer.writerows(row_list)


if __name__ == "__main__":
    main()

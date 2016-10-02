import datetime
import time
import random

def write(timestamp, file, target_temp,current_temp):
    formatted_time = datetime.datetime.fromtimestamp((timestamp / 1000)).strftime('%Y-%m-%d %H:%M:%S')
    tt = "0" if target_temp is None else str(target_temp)
    msg = formatted_time + "," + str(current_temp) + "," + tt + "\n"
    filename = "log/" + file + ".templog"
    with open(filename, "a") as myfile:
        myfile.write(msg)


timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000

print timestamp



for x in range(0, 1000):
    timestamp = timestamp + 5 *1000
    write(timestamp, "F_1", random.randrange(0, 101, 2), random.randrange(0, 101, 2))
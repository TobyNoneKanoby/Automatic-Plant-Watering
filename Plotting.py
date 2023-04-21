import csv
import matplotlib.pyplot as plt
from time import sleep
from os import system
import sys
import time

start_time=time.time()


# Open the CSV file and read the data into lists
with open('fuktighet.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    timestamps = []
    temps = []
    humids1 = []
    humids2 = []
    for row in reader:
        timestamps.append(row['time'])
        #temps.append(float(row['temperature sensor 1']))
        humids1.append(float(row['humidity sensor 1']))
        humids2.append(float(row['humidity sensor 2']))

# Create the plot
fig, ax = plt.subplots(num='plot')



manager = plt.get_current_fig_manager() #fullskjerm
manager.full_screen_toggle()

#ax.plot(timestamps, temps, label='Temperature')
ax.plot(timestamps, humids1, label='Plante 1')
ax.plot(timestamps, humids2, label='Plante 2')
ax.set_xlabel('Tid')
ax.set_ylabel('Prosent fuktighet')
ax.set_title('Fuktighet')
plt.ylim(50, 80)
#plt.xticks(timestamps, [k for k in range(0,len(timestamps),5)])
#plt.grid(color='r', linestyle='-', linewidth=1)
ax.legend()

# Show the plot
plt.show(block=False)
plt.pause(20)#viser i 20 sek før den lukker
plt.close()



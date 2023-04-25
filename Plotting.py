import matplotlib.pyplot as plt
import csv
import matplotlib.dates as mdates
from datetime import datetime



# Define the file name
filename = '/home/tobias/fuktighet_V2.csv'

# Define the lists to store the data
timestamps = []
humidities1 = []
humidities2 = []
vanning_ack1 = []
vanning_ack2 = []

# Read the data from the CSV file
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader) # Skip the header row
    for row in csvreader:
        timestamps.append(row[0])
        humidities1.append(int(row[2]))
        humidities2.append(int(row[3]))
        vanning_ack1.append(int(row[4]) if row[4] else None) # Convert empty string to None
        vanning_ack2.append(int(row[5]) if row[5] else None) # Convert empty string to None

# Convert timestamps to datetime objects
timestamps = [datetime.strptime(ts, '%m-%d %H:%M') for ts in timestamps]

# Create the scatter plot
plt.scatter(timestamps, humidities1, label='Plante 1')
plt.scatter(timestamps, humidities2, label='Plante 2')

for i, vanning1 in enumerate(vanning_ack1):
    if vanning1 == 1:
        plt.scatter(timestamps[i], humidities1[i], marker='x', color='blue', s=200)

for i, vanning2 in enumerate(vanning_ack2):
    if vanning2 == 1:
        plt.scatter(timestamps[i], humidities2[i], marker='x', color='orange', s=200)


plt.plot(timestamps, humidities1, color='blue', alpha=0.5)
plt.plot(timestamps, humidities2, color='orange', alpha=0.5)

# Set the x-tick labels to show only one tick per day
days = mdates.DayLocator()
date_fmt = mdates.DateFormatter('%d-%m')
plt.gca().xaxis.set_major_locator(days)
plt.gca().xaxis.set_major_formatter(date_fmt)
#plt.xticks(rotation=45)

manager = plt.get_current_fig_manager() #fullskjerm
manager.full_screen_toggle()
plt.grid(True)
plt.ylim(50, 90)
plt.xlabel('Tid [ved midnatt]')
plt.ylabel('Fuktighet [%]')
plt.title('Fuktighetsavlesning')
plt.legend()
plt.show(block=False)
plt.pause(20)#viser i 20 sek før den lukker
plt.close()





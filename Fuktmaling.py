import time
import csv
import board
from adafruit_seesaw.seesaw import Seesaw
import matplotlib.pyplot as plt
from datetime import datetime
from adafruit_extended_bus import ExtendedI2C as I2C
from smbus import SMBus
from time import sleep
import pickle


# Import the bus
i2c_bus = I2C(22)
addr = 0x38 # bus address
bus = SMBus(22) # indicates /dev/ic2-2

# Initialize the Seesaw sensors
ss1 = Seesaw(i2c_bus, addr=0x36)
ss2 = Seesaw(i2c_bus, addr=0x37)

# Open the CSV file in append mode and write a header if the file is new
with open('fuktighet.csv', 'a', newline='') as csvfile:
    fieldnames = ['time', 'temperature sensor 1', 'humidity sensor 1', 'humidity sensor 2']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:
        writer.writeheader()

# Append data to the CSV file
with open('fuktighet.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp1_list = []
    #temp2_list = []
    humid1_list = []
    humid2_list = []
    for i in range(10):
        temp1_list.append(ss1.get_temp())
        humid1_list.append(ss1.moisture_read())
        humid2_list.append(ss2.moisture_read())
        time.sleep(0.5) # Wait 0.5 seconds between each measurement
    temp1 = int(sum(temp1_list) / len(temp1_list)) # Calculate average temperature
    #temp2 = sum(temp2_list) / len(temp2_list)
    humid1_var = sum(humid1_list) / len(humid1_list) # Calculate average humidity
    humid2_var = sum(humid2_list) / len(humid2_list)
    humid1 = int(((humid1_var - 317) / (1015 - 317)) * 100) #prosentomgjøring
    humid2 = int(((humid2_var - 317) / (1015 - 317)) * 100)
    writer.writerow([timestamp, temp1, humid1, humid2])
    print("Fukt1: ", humid1)
    print("Fukt2: ", humid2)
    
file1 = open('data1', 'rb') #leser terskelverdi plante1
terskel1 = pickle.load(file1)
file1.close()

file2 = open('bryter1', 'rb') #leser status om plante 1 er på plass
status1 = pickle.load(file2)
file2.close()

print("terskel 1:",terskel1)
print("status1:", status1)
    
if (humid1 < terskel1) and (status1 ==1):
    bus.write_byte(addr, 0x1)
    sleep(0.5)
    bus.write_byte(addr, 0x0)
    
sleep(5)
file3 = open('data2', 'rb') #leser terskelverdi plante2
terskel2 = pickle.load(file3)
file3.close()

file4 = open('bryter2', 'rb') #leser status om plante 2 er på plass
status2 = pickle.load(file4)
file4.close()
print("terskel 2:",terskel2)
print("status2:", status2)
    
if (humid2 < terskel2) and (status2 ==1):
    bus.write_byte(addr, 0x2)
    sleep(0.5)
    bus.write_byte(addr, 0x0)
    

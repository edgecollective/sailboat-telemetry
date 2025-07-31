#with open("my_file.txt", "w") as f:
#    f.write("This is the original content.\n")
import time
import random

lat=41.77658028957489
lon=-71.38852260058152
compass=0
tilt=0

lat_lon_stepsize=.0001
tilt_stepsize=1

firstline="latitude,longitude,compass_heading,tilt\n"
with open("sailboat_data.csv", "w") as f:
        f.write(firstline)

while True:

    
    d_lat=random.uniform(0,1)*lat_lon_stepsize
    d_lon=random.uniform(0,1)*lat_lon_stepsize
    d_tilt=random.uniform(0,1)*tilt_stepsize
    
    lat=lat+d_lat
    lon=lon+d_lon
    tilt=tilt+d_tilt
    dataline=str(lat)+","+str(lon)+","+str(compass)+","+str(tilt)+"\n"
    # Append new content to the file
    print(dataline)
    with open("sailboat_data.csv", "a") as f:
        f.write(dataline)

    time.sleep(5)
    # Verify the content of the file
    #with open("my_file.txt", "r") as f:
    #    content = f.read()
    #    print(content)

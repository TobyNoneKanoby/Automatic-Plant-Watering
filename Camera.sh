#!/bin/bash
DATE=$(date +"%Y-%m-%d_%H%M")
libcamera-still -o /home/tobias/timelapse/$DATE.jpg

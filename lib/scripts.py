#!/usr/bin/python
# -*- coding: utf-8 -*-

# deviceWatcher - lib/scripts.py
# ------------------------------
# This is the classes/functions to
# Maintain/Manipulate the Devices

import csv

def _parseDeviceCSV(fileName):
    with open(fileName, 'r') as csvFile:
        csvDevices = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in csvDevices:
            yield row
    
def createDeviceList(csvFile):
    deviceList = []
    for device in _parseDeviceCSV(csvFile):
        deviceList.append(device)
    return deviceList
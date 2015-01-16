#!/usr/bin/python
# -*- coding: utf-8 -*-

# deviceWatcher - main.py
# -----------------------
# This is the main program logic

import lib.devices as devices
import lib.scripts as scripts
import lib.db as db

csvFile = 'c:/temp/testDevices.csv'
deviceList = []

def main():
    _setDevices(deviceList)
    printStats(deviceList)
    
def printStats(deviceList):
    for device in deviceList:
        print(device.getCurrentStatus())

    
def _setDevices(deviceList):
    tempList = scripts.createDeviceList(csvFile)
    for device in tempList:
        deviceList.append(devices.device(*device))    
    

if __name__ == '__main__':
    main()
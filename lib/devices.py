#!/usr/bin/python
# -*- coding: utf-8 -*-

# deviceWatcher - lib/devices.py
# ------------------------------
# This is the classes for the devices

import ipaddr
import socket
import time
import platform
import os

class device():
    '''device(base): This is the base class for the Devices.
    
    currentIP = The current ip address of the device (eg. 10.0.0.1)
    Name = The name of the device (eg. "Ramingining Zebra")
    Site = The Name of the Site/Location
    Subnet = The CIDR annotated version of the devices residing subnet
    machineName = The Machine NAme of the device (netbios name) '''
    
    currentIP = ipaddr.IPAddress
    Name = ''
    Site = ''
    SiteCode = ''
    Subnet = ipaddr.IPNetwork
    machineName = ''
    timeout = 3
    currentStatus = {'Status': '', 'Delay': 0, 'Time': 0}
    
    def __init__(self, currentIP, Name, Site, Subnet, machineName):
        self.currentIP = ipaddr.IPAddress(currentIP, 4)
        self.Name = Name
        self.Site = Site
        self.Subnet = Subnet
    
    def _ping(self):
        if platform.system() == 'Windows':
            response = os.system("ping -n 1 " + self.currentIP.__str__())
        elif platform.system() == 'Linux':
            response = os.system("ping -c 1 " + self.currentIP.__str__())
        else:
            print('Error: Invalid System type (' + platform.system() + ')')
            return(2)
        
        if response == 0:
            return(0)
        else:
            return(1)    

    def _updateIP(self):
        for addressIter in self.Subnet:
            curIPIter, aliasList, addressList = socket.gethostbyaddr(addressIter)
            if self.machineName == curIPIter:
                self.currentIP = ipaddr.IPAddress(addressIter)
                
    def _updateStatus(self):
        status = self._ping()
        if status == None:
            self.currentStatus['Status'] = "Down"
            self.currentStatus['Delay'] = None
        else:
            self.currentStatus['Status'] = "Up"
            self.currentStatus['Delay'] = status
            self.currentStatus['Time'] = time.time()
            
    def getCurrentStatus(self):
        self._updateStatus()
        print(self.Name + " is " + self.currentStatus['Status'] + "!")
        
if __name__ == '__main__':
    test = device('192.168.1.21', 'lounge server', 'narrows', '192.168.1.0/24', 'Lounge-Server')
    test.getCurrentStatus()
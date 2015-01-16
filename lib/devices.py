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
import subprocess

import pingparser

class device(object):
    '''device(base): This is the base class for the Devices.
    
    currentIP = The current ip address of the device (eg. 10.0.0.1)
    Name = The name of the device (eg. "server 1")
    Site = The Name of the Site/Location
    Subnet = The CIDR annotated version of the devices residing subnet
    machineName = The Machine Name of the device (netbios name) '''
    
    currentIP = ipaddr.IPAddress
    Name = ''
    Site = ''
    SiteCode = ''
    Subnet = ipaddr.IPNetwork
    machineName = ''
    timeout = 3
    currentStatus = 0
    currentStats = {}
    
    def __init__(self, currentIP, Name, Site, Subnet, machineName):
        self.currentIP = ipaddr.IPAddress(currentIP, 4)
        self.Name = Name
        self.Site = Site
        self.Subnet = Subnet
        self._updateStatus()
    
    def _ping(self):
        #if platform.system() == 'Windows':
            #response = subprocess.Popen(["ping", "-n 1", self.currentIP.__str__()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #response = os.system("ping -n 1 " + self.currentIP.__str__() + ' > NUL 2>&1')
        #elif platform.system() == 'Linux':
            #response = subprocess.Popen(["ping", "-c 1", self.currentIP.__str__()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #response = os.system("ping -c 1 " + self.currentIP.__str__() + ' >/dev/null 2>&1')
        if platform.system() == 'Windows':
            ping = subprocess.Popen("ping -n 1 " + self.currentIP.__str__(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            response, error = ping.communicate()            
            #response = os.system("ping -n 1 " + self.currentIP.__str__())
        elif platform.system() == 'Linux':
            ping = subprocess.Popen("ping -c 1 " + self.currentIP.__str__(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            response, error = ping.communicate()
            #response = os.system("ping -c 1 " + self.currentIP.__str__())
        else:
            print('Error: Invalid System type (' + platform.system() + ')')
            return(2)

        ret = pingparser.parse(response, platform.system())
        
        if ret['sent'] == ret['received']:
            return(0)
        else:
            return(1)
        
        #if response == 0:
            #return(0)
        #else:
            #return(1)
        
    def _pingStats(self, count=5):
        if platform.system() == 'Windows':
            ping = subprocess.Popen(["ping", "-n", str(count), self.currentIP.__str__()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            response, error = ping.communicate()            
            #response = os.system("ping -n 1 " + self.currentIP.__str__())
        elif platform.system() == 'Linux':
            ping = subprocess.Popen(["ping", "-c", str(count), self.currentIP.__str__()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            response, error = ping.communicate()
            #response = os.system("ping -c 1 " + self.currentIP.__str__())
        else:
            print('Error: Invalid System type (' + platform.system() + ')')
            return(2)
        
        ret = pingparser.parse(response, platform.system()) 
        self.currentStats = ret
        return ret
    
    def _updateIP(self):
        for addressIter in self.Subnet:
            curIPIter, aliasList, addressList = socket.gethostbyaddr(addressIter)
            if self.machineName == curIPIter:
                self.currentIP = ipaddr.IPAddress(addressIter)
                
    def _updateStatus(self):
        status = self._ping()
        if status == None:
            self.currentStatus = 1
        elif status == 0:
            self.currentStatus = 0
            
    def getCurrentStatus(self):
        self._updateStatus()
        if self.currentStatus == 0:
            print(self.Name + " is up!")
        elif self.currentStatus == 1:
            print(self.Name + " is Down!")            
        
if __name__ == '__main__':
    up = device('127.0.0.1', 'up', 'test', '192.168.1.0/24', 'test')
    up.getCurrentStatus()
    down = device('127.0.0.11', 'down', 'test', '192.168.1.0/24', 'test')
    down.getCurrentStatus()
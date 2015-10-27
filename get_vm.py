#!/usr/bin/python

import libvirt
import sys
from optparse import OptionParser

#VirtUser = 'vmindru'
#VirtHost = '127.0.0.1' 
#KeyFile="/home/vmindru/.ssh/localhost"
VirtUri = "qemu+ssh://"+VirtUser+"@"+VirtHost+"/system"+"?keyfile="+KeyFile

def get_opt():
    parser = OptionParser()
    parser.add_option(  "-u",
                        "--user", 
                        dest="VirtUser",
                        help="QEMU User to connect", 
                        metavar="USER")
    parser.add_option(  "-H",
                        "--host", 
                        dest="VirtHost",
                        help="QEMU HOST to connect", 
                        metavar="HOST")
    parser.add_option(  "-k",
                        "--key", 
                        dest="SshKey",
                        help="PATH to key for SSH, if not specified default will be used", 
                        metavar="KEY")
    (options, args) = parser.parse_args() 
    return options,args

def getcount(VirtUri):
    conn = libvirt.open(VirtUri)
    Count = conn.numOfDomains() 
    return Count

if __name__ == "__main__":
    (opts, args) = get_opt()

print getcount(VirtUri)

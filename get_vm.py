#!/usr/bin/python

import libvirt
import sys
from optparse import OptionParser


def get_opt():
    parser = OptionParser("usage: %prog -u USER -H HOST -K path_key_file")
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
    if not options.VirtUser:
        parser.error("you have to specify -u USER" )
    if not options.VirtHost:
        parser.error("you have to specify -H host" )
    if not options.SshKey:
        parser.error("you have to specify -k key" )
    return options,args,parser

def getcount(VirtUri):
    conn = libvirt.open(VirtUri)
    Count = conn.numOfDomains() 
    return Count

if __name__ == "__main__":
    (opts, args, parser) = get_opt()
    VirtUser=opts.VirtUser
    VirtHost=opts.VirtHost
    SshKey=opts.SshKey
    VirtUri = "qemu+ssh://"+VirtUser+"@"+VirtHost+"/system"+"?keyfile="+SshKey
    print getcount(VirtUri)

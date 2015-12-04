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
    parser.add_option(  "-l",
                        "--local", 
                        dest="Local",
                        action="store_true",
                        help="query local qemu:///system", 
                        )
    parser.add_option(  "-m",
                        "--booked-mem",
                        dest="BookedMem",
                        action="store_true",
                        help="query for total memmory booked",
                    )
    parser.add_option(  "-C",
                        "--cpu-count",
                        dest="CpuCount",
                        action="store_true",
                        help="query for number of virtual cores allocated",
                    )
    parser.add_option(  "-c",
                        "--count-vm",
                        dest="VmCount",
                        action="store_true",
                        help="query for total running VM",
                    )

    (options, args) = parser.parse_args() 
    if not options.Local:
        if not options.VirtUser:
            parser.error("you have to specify -u USER" )
        if not options.VirtHost:
            parser.error("you have to specify -H host" )
        if not options.SshKey:
            parser.error("you have to specify -k key" )
    return options,args,parser

def VmCount(VirtUri):
    conn = libvirt.open(VirtUri)
    Count = conn.numOfDomains() 
    return Count

def CpuCount(VirtUri):
    Core = 0 
    conn = libvirt.open(VirtUri)
    for dom in conn.listAllDomains():
        if dom.info()[0] == 1:
            Core = Core + dom.info()[3]
    return Core

def BookedMem(VirtUri):
    Mem = 0 
    conn = libvirt.open(VirtUri)
    for dom in conn.listAllDomains():
        if dom.info()[0] == 1:
            Mem = Mem + dom.info()[1]
    return Mem 


if __name__ == "__main__":
    (opts, args, parser) = get_opt()
    
    

    if not opts.Local:
        VirtUser=opts.VirtUser
        VirtHost=opts.VirtHost
        SshKey=opts.SshKey
        VirtUri = "qemu+ssh://"+VirtUser+"@"+VirtHost+"/system"+"?keyfile="+SshKey
    else:
        VirtUri = "qemu:///system"

    if  opts.VmCount:
        print VmCount(VirtUri)
    elif opts.CpuCount:
        print CpuCount(VirtUri)
    elif opts.BookedMem:
        print BookedMem(VirtUri)
    else:
        print VmCount(VirtUri)































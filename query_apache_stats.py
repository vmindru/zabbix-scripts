#!/usr/bin/python

from __future__ import print_function
from sys import stderr
from sys import stdout
from sys import exit
from optparse import OptionParser
from urllib import urlopen


class __getopts__():
    def __init__(self):
        version = 2.2
        usage = "usage: %prog [options] source_path, container:dest_path"
        parser = OptionParser(usage=usage, version=version)
        parser.add_option("-v", "--verbose",
                          help="enable verbose mode, [default: %default]",
                          default=False,
                          action="store_true")
        parser.add_option("-t", "--socket-timeout",
                          help="set socket timeout, "
                          "[default: %default]",
                          default=3,
                          dest="socket_timeout")
        parser.add_option("-p", "--port",
                          help="port to connect to server, "
                          "[default: %default]",
                          default=80,
                          dest="port")
        parser.add_option("-a", "--address",
                          help="address to communicate to server this can be"
                          "hostname or fqdn"
                          "[default: %default]",
                          dest="address",
                          default="127.0.0.1")
        parser.add_option("-m", "--metric",
                          help="Will return value of the requested metric"
                          "this option is mutual exclusive with -s option",
                          dest="metric",
                          choices=["TotalkBytes",
                                   "CPULoad",
                                   "ReqPerSec",
                                   "BytesPerSec",
                                   "BytesPerReq",
                                   "BusyWorkers",
                                   "IdleWorkers"],
                          default=None)
        parser.add_option("-s", "--scoreboard",
                          help="get number of workers in specified status"
                          "valid statuses are _,S,R,W,K,D,C,L,G,I,."
                          "this option is mutual exclusive with -m|--metrics",
                          choices=["_", "S", "R", "W", "K",
                                   "D", "C", "L", "G", "I", "."],
                          nargs=1,
                          dest="scoreboard",
                          default=False
                          )

        (self.options, self.args) = parser.parse_args()
        if self.options.metric and self.options.scoreboard:
            parser.error("options -m and -s are mutually exclusive")
        """ due to the fact that -s and -m are mutual exclusive, when setting
        -s we still need an valid options.metric  value """
        if self.options.scoreboard:
            self.options.metric = "scoreboard"
        self.options.uri = "/server-status?auto"


def __debug_msg__(message, debug=False, dest="stderr"):
    """ Debug print function

        will print passed message when debug is True
        the output can be sent to stderr or stdout

        Attributes
        ----------
        message: string, the string to print
        debug: Boolean, print the message when True
        dest: string: print the message to stderr or stdout

        Returns
        -------
        nothing is returned

        """
    if debug is True:
        if dest == "stderr":
            print(message, file=stderr)
        elif dest == "stdout":
            print(message, file=stdout)
        else:
            print("invalid dest value {}, valid stdout|stderr".format(dest))


def http_request(address, uri, port=80, debug=False):
    """ Creates HTTP request

    Function to fire off an HTTP request to the web server, throw an
    exception gracefully and print FAIL if a connection can't be made
    The URL is build from "http://"+address+":"+port+"/"+uri

    Attributes
    ----------
               address: web server address, fqdn or ip
               port: tcp port
               uri: uri to amend to the end of formed uri
    """
    try:
        url = "http://{}:{}/{}".format(address, port, uri)
        http_response = urlopen(url)
        return http_response

    except:
        __debug_msg__("Error requesting URL: {}".format(url), debug)
        exit(1)


def get_metric(metric, http_response, debug=False):
    """get metric value

     return requested metric value from a http_request.
     http_request is the http data from apache server_status?auto request.

     Attributes
     ----------
       requested_metric: string, the desired http metric
       http_request: http_request must be an object with read() method

     Valid metrics:
     --------------
     TotalAccesses: Total amount of requests served since server started
     TotalkBytes: Total amount of kBytes served since server started
     uptime: HTTP server uptime
     CPULoad: to be documented
     ReqPerSec: Requests per second
     BytesPerSec: Bytes per second
     BytesPerReq: Bytes per request
     BusyWorkers: Number of Workers in busy status
     IdleWorkers: Number of Workers in Idle status
     Scoreboard: Scoreboard info

     Returns
     --------

     Returns value of the metric, or False in case no metric has been found
     in server_status

    """
    valid_metric = dict(TotalAccesses="Total Accesses",
                        TotalkBytes="Total kBytes",
                        uptime="Uptime",
                        CPULoad="CPULoad",
                        ReqPerSec="ReqPerSec",
                        BytesPerSec="BytesPerSec",
                        BytesPerReq="BytesPerReq",
                        IdleWorkers="IdleWorkers",
                        BusyWorkers="BusyWorkers",
                        scoreboard="Scoreboard")
    if metric in valid_metric:
        buf = 'none'
        while len(buf) != 0:
            __debug_msg__(dir(http_response))
            buf = http_response.readline()
            if valid_metric[metric] in buf:
                return str(buf.split(":")[1])
        return False
    else:
        __debug_msg__("{} metric is not valid".format(metric), debug)
        return False


def count_scoreboard_metric(scoreboard_key, scoreboard, debug=False):
    """get apache workers stats

    check if requested scoreboard_key is valid, and return
    number of workers in scoreboard_key status

    Attributes
    -----------

      scoreboard_key: the key we want to count
      scoreboard: string object value take from apache server_status?auto

    Valid Variants
    --------------
    Scoreboard Key are worker statuses, with following valid variants

     idle workers:
     "_" Waiting for Connection,

     busy workers:
     "S" Starting up,
     "R" Reading Request,
     "W" Sending Reply,
     "K" Keepalive (read),
     "D" DNS Lookup,
     "C" Closing connection,
     "L" Logging,
     "G" Gracefully finishing,
     "I" Idle cleanup of worker,

     no worker running, but there are free slots as per config:
     "." Open slot with no current process

     Returns
     ---------

     Returns number of scoreboard_keys occurrences in scoreboard

    """
    scoreboard_keys = ["_", "S", "R", "W", "K", "D", "C", "L", "G", "I", "."]
    if scoreboard_key in scoreboard_keys:
        return scoreboard.count(scoreboard_key)
    else:
        __debug_msg__("{} key is not valid, must be one of {}".
                      format(scoreboard_key, scoreboard_keys))


if __name__ == "__main__":

    opts = __getopts__()
    debug = opts.options.verbose
    address = opts.options.address
    port = opts.options.port
    uri = opts.options.uri
    requested_metric = opts.options.metric
    __debug_msg__("getting data for {}".format(requested_metric, debug))
    http_response = http_request(address, uri, port, debug)
    metric_value = get_metric(requested_metric,
                              http_response,
                              debug)
    if metric_value is False:
            __debug_msg__("Could not get {} metric value".
                          format(requested_metric),
                          debug)
            exit(1)
    else:
        try:
            metric_value = metric_value.strip()
        except:
            __debug_msg__("something went really wrong,unexpected "
                          "metric_value", debug)

    if requested_metric == "scoreboard" and metric_value is not False:
        scoreboard_key = opts.options.scoreboard
        print(count_scoreboard_metric(scoreboard_key, metric_value, debug))
        exit(0)
    else:
        print(metric_value)
        exit(0)

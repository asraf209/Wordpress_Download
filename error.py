#!/usr/bin/python

import time
import classes


def log_debug(string, level, config):
    
    if level == 1:
        levelmsg = "Critical"
    elif level == 2:
        levelmsg = "Message"
    
    timestr = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    error_msg = "[Thread%d] [%s] [%s] %s" % (config.thread_id, timestr, levelmsg, string)
    
    if config.debug:
        print error_msg
            
    try:
        filename = config.debug_file_name + "_" + str(config.thread_id)
        debugfile = open(filename, "a")
        debugfile.write(error_msg.__str__() + '\n')
        debugfile.close()

    except Exception as err:
        print err
        print "Error in log_debug()"


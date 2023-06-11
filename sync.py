#!/usr/bin/python3
from optparse import OptionParser
from filecmp import dircmp, cmp
from os import remove
from shutil import copytree, copy, rmtree
from datetime import datetime
import os
import time

def log(text, logfile):
    print(text)
    logfile.write(text + "\n")

def deep_sync(source, target, logfile):
    result = dircmp(source, target)
    result.compare = cmp

    for toCopy in result.diff_files:
        log("COPYING " + os.path.join(source, toCopy) + " to " + target, logfile)
        copy(os.path.join(source, toCopy), target)

    for toCopy in result.left_only:
        log("COPYING " + os.path.join(source, toCopy) + " to " + target, logfile)
        if os.path.isdir(os.path.join(source, toCopy)):
            copytree(os.path.join(source, toCopy), os.path.join(target, toCopy))
        else:
            copy(os.path.join(source, toCopy), target)
    
    for toRemove in result.right_only:
        log("REMOVING " + os.path.join(target, toRemove), logfile)
        if os.path.isdir(os.path.join(target, toRemove)):
            rmtree(os.path.join(target, toRemove))
        else:
            remove(os.path.join(target, toRemove))

    for subdir in result.subdirs:
        deep_sync(os.path.join(source, subdir), os.path.join(target, subdir), logfile)
        

def main():
    parser = OptionParser()
    parser.add_option("-i", "--interval", dest="interval",
                  help="synchronisation interval (in minutes)", default="1")
    parser.add_option("-s", "--source", dest="source", help="source folder - MANDATORY")
    parser.add_option("-t", "--target", dest="target", help="target folder - MANDATORY")
    parser.add_option("-l", "--logfile", dest="logfile", help="Path to log file", default="log.txt")
    (options, args) = parser.parse_args()
    if (options.source is None or options.target is None):
        parser.print_help()
        exit()

    logfile = open(options.logfile, "w")
    while(True):
        log("SYNC ATTEMPT AT " + str(datetime.now()), logfile)
        deep_sync(options.source, options.target, logfile)
        log("SYNC COMPLETE AT " + str(datetime.now()), logfile)
        time.sleep(int(options.interval) * 60)

if __name__=="__main__":
    main()
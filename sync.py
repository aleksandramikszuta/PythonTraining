#!/usr/bin/python3
from optparse import OptionParser
from filecmp import dircmp, cmp
from os import remove
from shutil import copytree, copy, rmtree
import os

def deep_sync(source, target):
    result = dircmp(source, target)
    result.compare = cmp

    for toCopy in result.diff_files:
        #print ("COPYING " + os.path.join(source, toCopy) + " " + target)
        copy(os.path.join(source, toCopy), target)

    for toCopy in result.left_only:
        #print ("COPYING " + os.path.join(source, toCopy) + " " + target)
        if os.path.isdir(os.path.join(source, toCopy)):
            copytree(os.path.join(source, toCopy), os.path.join(target, toCopy))
        else:
            copy(os.path.join(source, toCopy), target)
    
    for toRemove in result.right_only:
        if os.path.isdir(os.path.join(target, toRemove)):
            rmtree(os.path.join(target, toRemove))
        else:
            remove(os.path.join(target, toRemove))

    for subdir in result.subdirs:
        deep_sync(os.path.join(source, subdir), os.path.join(target, subdir))
        

def main():
    parser = OptionParser()
    parser.add_option("-i", "--interval", dest="interval",
                  help="synchronisation interval (in minutes)", default="1")
    parser.add_option("-s", "--source", dest="source", help="source folder - MANDATORY")
    parser.add_option("-t", "--target", dest="target", help="target folder - MANDATORY")
    (options, args) = parser.parse_args()
    if (options.source is None or options.target is None):
        parser.print_help()
        exit()

    deep_sync(options.source, options.target)

if __name__=="__main__":
    main()
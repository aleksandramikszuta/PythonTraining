#!/usr/bin/python3
from optparse import OptionParser
from filecmp import dircmp

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

    diff =  dircmp(options.source, options.target)
    print("Report")
    print(diff.report())

if __name__=="__main__":
    main()
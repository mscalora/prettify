#!/usr/bin/env python
"""prettify an html or xml file v1.0.1

Usage:
	prettify [options] [original-file [prettified-file]]

Options:
	-v --verbose   verbose output
	-h --help      print this help information
"""
import sys
import getopt
import os
try:
	from BeautifulSoup import BeautifulSoup as soup
except ImportError:
	sys.stderr.write("Beautiful Soup is required to use prettify, see: http://www.crummy.com/software/BeautifulSoup/\n")
	sys.exit(20) 

verbose = False

def main(argv):
	global verbose
	
	argc = len(argv)
	html = ''

	if argc and not os.path.exists(argv[0]):
		print __doc__
		return 20
	
	if argc>0:
		html = open(argv[0]).read()
	else:
		while 1:
			try:
				line = sys.stdin.readline()
			except KeyboardInterrupt:
				sys.stderr.write("Interrupted by user!\n")
				return 5
		
			if not line:
				break
			html += line

	lcount0 = html.count('\n') + (1 if html[-1:]!='\n' else 0)
	ccount0 = len(html)

	if argc>1 and os.path.exists(argv[1]):
		root, ext = os.path.splitext(argv[1])
		backup = "%s.bak" % root
		if verbose:
			print "Overwriting %s, original backedup to %s" % (argv[1], backup)
		oldhtml = open(argv[1]).read()
		open(backup,'w').write(oldhtml)

	formatted = soup(html).prettify()
	lcount1 = formatted.count('\n') + (1 if formatted[-1:]!='\n' else 0)
	ccount1 = len(formatted)
	
	if argc>1:
		open(argv[1],'w').write(formatted)
	else:
		sys.stdout.write(formatted)
		
	if verbose: 
		print "Original:   %d lines, %d characters" % (lcount0,ccount0)
		print "Prettified: %d lines, %d characters" % (lcount1,ccount1)
	return 0

def bufcount(filename):
    f = open(filename)                  
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines

def pre_main():
	global verbose
	# parse command line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], "vh", ["help","verbose"])
	except getopt.error, msg:
		print msg
		print "for help use --help"
		return 2
	# process options
	for o, a in opts:
		if o in ("-v", "--verbose"):
			verbose = True
		elif o in ("-h", "--help"):
			print __doc__
			return 0
	# process arguments
	return main(args) # process() is defined elsewhere

if __name__ == "__main__":
	sys.exit(pre_main())

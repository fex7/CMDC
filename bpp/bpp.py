#!/usr/bin/env python
"""Batch preprocessor.

This module preprocesses bat files.
It does operations such as:
* #include

It is a console utility.
Write this in a terminal to get help:
$ python bpp.py --help

This utility will work correctly on Windows operating systems.

Author: Fex
GitHub: https://github.com/Fexxyi
Date: 12 May 2021

"""

import random
import sys
import os
 
sys.path.insert(
	1, os.path.realpath(os.path.join(__file__, '..', 'Lib'))
)

from PyLib.preprocessor import (
	Preprocessor,
)
from PyLib.bppcli import (
	BppCLI,
)
from PyLib.utils import (
	chdir_to_filedir,
	get_temp_dir,
)
from PyLib.exceptions import (
	BPPError,
	CLIError,
)



def main(argc, argv):
	"""Main function to bpp utility."""

	bpp_cli = BppCLI()
	status = bpp_cli.parse(argv)
	if not status:
		return None
	bpp_cli.validate()
	parsered_args = bpp_cli.get_parsered_args()
	source = parsered_args['source']
	output = parsered_args['output']
	run = parsered_args['run']
	if run is not None and os.name != 'nt':
		raise CLIError("Argument '--run / -r' works on OS Windows")
	if source is None:
		raise CLIError("Argument '--source or -s' not specified")
	source = os.path.abspath(source)
	current_dir = os.getcwd()
	chdir_to_filedir(source)
	preprocessor = Preprocessor(source)
	preprocessor.preprocessize()
	os.chdir(current_dir)
	if output is not None:
		output = os.path.abspath(output)
		preprocessor.save(output)
	else:
		if run is not None:
			temp_file_name = '__output_%s__.bat' % random.randrange(100000, 999999)
			tmp_dir = get_temp_dir()
			output = os.path.abspath(
				os.path.join(tmp_dir, temp_file_name)
			)
			preprocessor.save(output)
		else:
			preprocessed_file = preprocessor.get_preprocessed_file()
			print(preprocessed_file)
			return None
	if run is not None:
		command = "call %s" % output
		try:
			os.system(command)
			
		finally:
			if parsered_args['output'] is None:
				os.remove(output)
	return None

def run():
	"""Runs the main function.
	
	Raises:
	    SystemExit -- calls sys.exit

	"""

	if os.name != 'nt':
		print("Warning: Bpp utility works correctly in OS Windows")
	argc = len(sys.argv)
	argv = sys.argv
	current_dir = os.getcwd()
	try:
		main(argc, argv)
	
	except Exception as ex:
		exceps = (BPPError, OSError,)
		if isinstance(ex, exceps):
			error_message = 'Error: %s' % (
				'\n'.join(map(str, ex.args)),
			)
			if isinstance(ex, OSError) and ex.filename is not None:
				error_message += ": '%s'" % ex.filename
			print(error_message)
		else:
			error_message = "Error: Some kind of error has occurred"
			print(error_message)
		sys.exit(1)
	
	else:
		sys.exit(0)
	
	finally:
		try:
			os.chdir(current_dir)
		
		except Exception:
			pass


__all__ = [
	'main',
	'run',
]


if __name__ == "__main__":
	try:
		run()
	
	except Exception:
		error_message = "Error: Something went wrong"
		print(error_message)
		sys.exit(1)

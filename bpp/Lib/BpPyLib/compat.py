"""Compatibility between Python 2 and 3."""

import sys

__all__ = [

]


# Python version information.
PYTHON_VERSION = sys.version_info
PYTHON_MAJOR_VERSION = sys.version_info[0]

# Functions and constants specific to the Python language version.
if PYTHON_MAJOR_VERSION == 2:
	...

else:
	...
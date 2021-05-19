"""Bpp library package."""

__all__ = [
	'init',
]


def init():
	"""Initializes modules and packages.
	
	Return:
	    value: int -- imports count
	
	"""

	from . import abcs
	from . import utils
	from . import bppcli
	from . import prompts
	from . import version
	from . import includer
	from . import exceptions
	from . import precommands
	from . import preprocessor

	globals().update(locals())
	return len(locals())
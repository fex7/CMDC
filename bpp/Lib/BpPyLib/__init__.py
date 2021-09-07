"""Bpp library package."""

__all__ = [
	'init',
]


def init():
	"""Initializes modules and packages of this package.
	
	Return:
	    value: int -- imports count
	
	"""

	from . import abcs
	from . import utils
	from . import cores
	from . import bppcli
	from . import prompts
	from . import version
	from . import includer
	from . import exceptions
	from . import structures
	from . import precommands
	from . import preprocessor

	globals().update(locals())
	return len(locals())
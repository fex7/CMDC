"""Bpp utility version."""

__version__ = "1.0.0"


def getversion():
	"""Return bpp version.

	If returns '' then version not found.

	Return:
	    value: str -- '' or other string

	"""

	if "__version__" in globals():
		return __version__
	else:
		return ''


__all__ = [
	'getversion',
]


if __name__ == "__main__":
	print("v%s" % __version__)

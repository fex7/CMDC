"""Bpp utility version."""

__all__ = ['getversion',]
__version__ = "0.1.2"
__author__ = "Artashes Nazinyan (fex1)"
__author_email__ = "theartman380@gmail.com"
__author_github__ = "https://github.com/fex7"


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


if __name__ == "__main__":
	print("v%s" % __version__)
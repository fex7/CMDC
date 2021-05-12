"""bpp utility exceptions."""


class PreprocessorError(Exception):
	"""Main exception class a preprocessor commands."""
	pass


class IncludeError(PreprocessorError):
	"""Main included errors class."""
	pass


class IncludedSourceError(IncludeError):
	"""Raises when the source file is included itself."""
	pass


__all__ = [
	n for n in globals() if not n.startswith('_')
]
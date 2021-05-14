"""Bpp utility exceptions."""


class BPPError(Exception):
	"""Main exception class for Bpp utility."""
	pass


class PreprocessorError(BPPError):
	"""Main exception class a preprocessor commands."""
	pass


class IncludeError(PreprocessorError):
	"""Main included errors class."""
	pass


class IncludedSourceError(IncludeError):
	"""Raises when the source file is included itself."""
	pass


class CLIError(BPPError):
	"""Command Line Interface exception."""
	pass


__all__ = [
	n for n in globals() if not n.startswith('_')
]
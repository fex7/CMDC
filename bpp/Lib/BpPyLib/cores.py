"""In this kernel module for preprocessor commands."""

import os

__all__ = [
	'IncluderCore'
]


class IncluderCore:
	"""The 'Include' command core.
	
	Constructor:
	    regexs: dict -- The 'Include' command regexs
	
	#### Example ####:
	>>> import precommands, os
	>>> path = input('Enter file path: ')
	>>> com_include = precommands.PreprocessorCommands().com_include
	>>> obj = IncluderCore(com_include)
	>>> res = obj.absolutize(os.path.dirname(path), open(path).read())

	"""

	def __init__(self, com_include):
		self._com_include = com_include
	
	def absolutize(self, path, source):
		"""Makes inclusions in 'source' absolutized.

		This method simply finds all inclusions in 'source',
		and replaces the paths with absolute ones.
		It just inserts the value of the -
		'path' parameter at the beginning.

		But inclusions that already have an -
		absolute path will not change.
		And also, inclusions with reference to -
		environment variables will not change either.
		
		Args:
		    path: str -- Insertable path (directory path)
		    source: str --
		        File value in which you need -
		        to do absolutization
		
		Return:
		    value: str -- Absolutized 'source'
		
		Raises:
		    TypeError -- If incorrect args types
		    ValueError -- If incorrect args
		
		"""

		com_include = self._com_include
		absolutized = source
		for m1 in com_include[1].finditer('\n' + source + '\n'):
			m1 = m1.group()
			if com_include[2].search('\n' + m1 + '\n') is not None:
				continue
			included_file = com_include[11].search(m1)
			if included_file is None:
				continue
			included_file = included_file.group()[1:-1].strip()
			if os.path.isabs(included_file):
				continue
			absolutized = absolutized.replace(
				m1, m1.replace(included_file, os.path.join(path, included_file))
			)
		return absolutized
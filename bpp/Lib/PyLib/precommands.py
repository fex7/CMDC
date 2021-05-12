"""Preprocessor commands."""

import re



class IncluderRegexs:
	"""Regular expressions of the 'include' command."""
	
	com_include = {
		# Good templates.
		1:     re.compile(r'(?<=\n)[ \t]*:#include[ \t]*".+"[ \t]*(?=\n)'), # :#include "fold\lib.bat"
		2:     re.compile(r'(?<=\n)[ \t]*:#include[ \t]*".*%.*"[ \t]*(?=\n)'), # :#include "%lib_dir%\lib.bat"
		11:    re.compile(r'"(.+)"'), # included file path - "fold\lib.bat"
		21:    re.compile(r'"(.+)"'), # included file path - "%lib_dir%\lib.bat"
		# Bad templates.
		-1:    re.compile(r'(?<=\n)[ \t]*:#include[ \t]*(?!.+)'), # :#include 
		-2:    re.compile(r'(?<=\n)[ \t]*:#include[ \t]*""'), # :#include ""
		-3:    re.compile(r'(?<=\n)[ \t]*:#include[ \t]*"(?!.+)'), # :#include "
		-4:    re.compile(r'(?<=\n)[ \t]*:#include[ \t]*".+[^"](?!.+)'), # :#include "lib.bat
		-5:    re.compile(r'(?<=\n)[ \t]*:#include [^"].+"'), # :#include lib.bat"
		-6:    re.compile(r'(?<=\n)[ \t]*:#include [^"].+[^"](?!.+)'), # :#include fold\lib.bat
	}


class PreprocessorCommands(IncluderRegexs,):
	"""Regular expressions of all preprocessor commands."""
	pass


__all__ = [
	n for n in globals() if not n.startswith('_')
]
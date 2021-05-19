"""Preprocessor commands."""

import re
import os
import copy

__all__ = [
	'IncluderRegexs',
	'PreprocessorCommands',
]


class IncluderRegexs:
	"""Regular expressions of the 'include' command.
	
	This class has a regular expression dictionary -
	for the 'include' command.

	The keys in the dictionary are of type integer.
	This dictionary contain the given keys:

	Keys names:
	    1, 11, 2, 21
	    -1, -2, -3, -4, -5, -6
	
	Correct:
	Key 1:
	    This is a standart include expression.
	    Match example - :#include "somes\some.bat"
		
	Key 11:
	    This one just fetches the contents of the 'include'.
	    Match example - "somes\some.bat"

	Key 2:
	    This is the 'include' expression -
	    with reference to environment variables.
	    Match example - :#include "%somes_path%\some.bat"

	Key 21:
	    This one also just fetches the contents of the 'include',
	    but which has a reference to environment variables.
	    Match example - "%somes_path%\some.bat"
	
	Incorrect:
	Key -1:
	    Match example - :#include

	Key -2:
	    Match example - :#include ""
	
	Key -3:
	    Match example - :#include "

	Key -4:
	    Match example - :#include "some.bat

	Key -5:
	    Match example - :#include some.bat"

	Key -6:
	    Match example - :#include some.bat

	Positive keys are valid 'include' expressions.
	Negative keys are incorrect 'include' expressions.

	For example, the regular expression 1 -
	is just looking for the 'include' expression:
	:#include "somes\some.bat".

	The regular expression 11, on the other hand,
	simply retrieves the value:
	"somes\some.bat".

	"""
	
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

	if os.name == 'posix':
		com_include[2] = re.compile(r'(?<=\n)[ \t]*:#include[ \t]*".*\$.*"[ \t]*(?=\n)')
	
	def get_com_include(self):
		"""Return 'include' command regexs.
		
		Return:
		    value: dict -- 'include' command regexs

		"""

		return copy.copy(self.com_include)


class PreprocessorCommands(IncluderRegexs,):
	"""Regular expressions of all preprocessor commands.
	
	This class has dictionaries with regular expressions -
	for various preprocessor commands.

	The keys in the dictionary are of type integer.
	In these dictionaries, the keys must be of the given format:

	Positive keys are correct regular expressions.
	They are used to find the correct command expressions.

	Negative keys are incorrect regular expressions.
	They are used to find invalid command expressions.
	They are used, for example, by a syntactic analyzer.

	But the keys are sometimes tied.
	For example, keys 1 and 11 for the 'include' command:

	1 - lookings for just the 'include' expression.
	For example - :#include "somes\some.bat".
	Key 11, on the other hand, simply fetches the value:
	For example - "somes\some.bat".

	You can create for example key 3 and keys 31, 32, etc.
	Just add a number to the key name, starting with one.

	This class inherits all regex classes using multiple inheritance.
	It currently only inherits the 'IncluderRegexs' class.
	But their number may increase in the future.

	"""
	
	def __repr__(self):
		repr_text = "PreprocessorCommands()"
		return repr_text
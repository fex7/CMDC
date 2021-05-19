"""Implements the 'include' command.

Write this For more information:
>>> # import sys
>>> # sys.path.insert(1, <includer module path>)
>>> import includer
>>> help(includer.Includer)

"""

import os
import textwrap

from .abcs import (
	BaseCommand,
)
from .exceptions import (
	IncludeError,
	IncludedSourceError,
)
from .prompts import (
	get_include_prompt,
)

__all__ = [
	'Includer',
	'get_special_includer',
]


class Includer(BaseCommand):
	"""Class for the 'include' command.

	Constructor:
	    regexs: dict -- include command regexs.
	    source_file_path: str -- source file path
	
	Raises:
	    TypeError -- If incorrect types.
	----------------------------------------

	This class is not tied to any programming language.
	It just provides functionality for the 'include' command.

	This class is not very flexible.
	There are a lot of things you have to implement -
	in order for everything to work as it should.
	For example, there is no recursive 'include'.

	Example:
	>>> help(Includer.start)
	There's just an example of how a -
	recursive 'include' can be implemented.

	The constructor takes a 'source_file_path' parameter.
	It's just the path to the source file.
	The class does not check this path in any way,
	and does not read the file from this path.
	This parameter is needed for other purposes.

	The constructor takes a parameter such as 'regexs'.
	It is a dictionary with regular expressions.
	These keys must be there:
	Keys names - <1,  11,  2,  21>
	
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

	Example:
	>>> # import sys
	>>> # sys.path.insert (1, <includer module path>)
	>>> import precommands
	>>> help(precommands.IncluderRegexs)
	It's just more about it there.
	
	"""

	def __new__(cls, regexs, source_file_path):
		error_message = "Param '%s' type is '%s', not '%s'"
		if not isinstance(regexs, dict):
			raise TypeError(
				error_message % (
					'regexs', 'dict',
					type(regexs).__name__),)
		if not isinstance(source_file_path, str):
			raise TypeError(
				error_message % (
					'source_file_path', 'str',
					type(source_file_path).__name__),)
		return super().__new__(cls)

	def __init__(self, regexs, source_file_path):
		self._regexs = regexs
		self._source_file_path = source_file_path
		self._comment_symbol = '::'
		self._file_extensions = ('.bat', '.cmd', '.hbat', '.hb')
	
	def __repr__(self):
		repr_text = "Includer(regexs=%s, source_file_path=%s)" % (
			self._regexs, self._source_file_path
		)
		return repr_text
	
	def setproperty(self, name, value):
		"""Set the property new value.
		
		The parameter 'name' for example -
		could be 'comment' OR 'extensions'.

		If name == 'extensions' then
		    set file extensions. ( ['.bat', '.cmd','.py'] )
		If name == 'comment' then
		    set comment symbol. ( '//', '#', '::', ...etc ) -
		    * the specify one option.
		
		Args:
		    name: str -- property name.
		    value: object -- new value
		
		Raises:
		    TypeError -- if incorrectly params types
		    ValueError -- if unsupported property
		    AttributeError -- if attribute not found
		
		"""
		 
		if not isinstance(name, str):
			raise TypeError("Param name is 'str'")
		if name == 'extensions' and not isinstance(value, (list, tuple)):
			errmsg = "If param name == 'extension' do the value is 'list' or 'tuple'"
			raise TypeError(errmsg)
		if name == 'comment' and not isinstance(value, str):
			errmsg = "If param name == 'comment' do the value is 'str'"
			raise TypeError(errmsg)
		if name in ('extensions', 'comment'):
			if name == 'extensions':
				self._file_extensions = value
			elif name == 'comment':
				self._comment_symbol = value
		else:
			errmsg = "This name '%s' - not supported" % name
			raise ValueError(errmsg)
	
	def getproperty(self, name):
		"""Return property value.
		
		The parameter 'name' for example -
		could be 'comment' OR 'extensions'.

		If name == 'extensions' then
		    return file extensions. ( ['.bat', '.cmd','.py'] )
		If name == 'comment' then
		    return comment symbol. ( '//', '#', '::', ...etc ) -
		    * the specify one option.
		
		Args:
		    name: str -- property name.
		
		Return:
		    value: object -- property value
		
		Raises:
		    TypeError -- if incorrectly params types
		    ValueError -- if unsupported property

		"""
		
		if not isinstance(name, str):
			raise TypeError("Param name is 'str'")
		if name in ('extensions', 'comment'):
			if name == 'extensions':
				return self._file_extensions
			elif name == 'comment':
				return self._comment_symbol
		else:
			errmsg = "This name '%s' - not supported" % name
			raise ValueError(errmsg)

	def read_included_file(self, file_path):
		"""Read included file.
		
		Args:
		    file_path: str -- file path
		
		Return:
		    value: str -- file value
			
		"""

		if not os.path.isfile(file_path):
			raise FileNotFoundError('Include file not found')
		file_ext = os.path.splitext(os.path.split(file_path)[-1])[-1]
		if file_ext not in self._file_extensions:
			raise OSError(
				"File extension must be in %s" % self._file_extensions)
		return self.read(file_path)
	
	def read_from_environ(self, environ_var):
		"""Read file from environment.

		Reads the file path of which is specified -
		in environment variables.
		
		Args:
		    environ_var: str -- environment variable name
		
		Return:
		    value: tuple -- :
		        0 is file value,
		        1 is unwrapped environment variable

		"""
		
		variable_value = os.popen('echo %s' % environ_var).read().strip()
		file_value = self.read_included_file(variable_value)
		return (file_value, variable_value)
	
	def syntax_analyze(self, source):
		"""The syntax analyzer for the inlcude command.

		Args:
		    source: str -- source file value
		
		Return:
		    value: bool -- True, is correctly
		
		Raises:
		   IncludeError -- raises if syntax incorrectly.
		   
		"""
		
		
		error_message = textwrap.dedent("""
			Syntax Error with 'include' command:\n
			* %s
			Line - %s
			SyntaxError - %s""")[1:]
		com_include = self._regexs
		bad_templates = (n for n in com_include if n < 0)
		for n in bad_templates:
			match = com_include[n].search(source)
			if match is not None:
				match = match.group().strip()
				if com_include[n].search('\n' + match) is None:
					continue
				try:
					line = source.splitlines().index(match)
					
				except ValueError:
					line = -1
				prompt = get_include_prompt(n)
				raise IncludeError(
					error_message % (prompt, line, match)
				)
		else:
			return True
	
	def not_include_source(self, source, include_expression):
		"""Raises exceptions due to the inclusion of itself.

		You do NOT need to call this method to check -
		if the file itself is included or not,
		this method just throws an exception.

		This method must be called if the file tries to include itself.
		For example, if the file "C:\myscript.bat" does the following:
		
		:#include "C:\myscript.bat"
		This is mistake!

		Args:
		    source: str -- source file value
		    include_expression: str -- for example ":#include source.bat"
		
		Raises:
		    IncludedSourceError -- just raises
		
		"""

		error_message = textwrap.dedent("""
			The file is trying to include itself.\n
			Line - %s
			IncludeError - %s""")[1:]
		try:
			line = source.splitlines().index(include_expression)

		except ValueError:
			line = -1
		raise IncludedSourceError(error_message % (line, include_expression))
	
	def start(self, source):
		"""Performs inclusion.

		This method makes the inclusion non-recursive.
		If you want to do it recursively,
		call it multiple times.

		An example of recursive inclusion:
		------------------------------
		>>> # source = <source file value>
		>>> # includer_object = <Includer object>
		>>> while True:
		...     includeds = includer_object.start(source)
		...     if includeds != source:
		...         source = includeds
		...     else:
		...         break
		------------------------------

		Args:
		    source: str -- source file value
		
		Return:
		    value: str -- source after include on
		
		Raises:
		    IncludeError -- raises if syntax incorrectly.
		    IncludedSourceError -- raises if includes itself.

		"""
		
		# analyze
		self.syntax_analyze(source)
		after_replacement = (
			'%s ' % self._comment_symbol + 'File - "%s"\n' +\
			'%s%s(\n\n' % (self._comment_symbol, '-'*30)
		)
		before_replacement = (
			'\n\n%s%s)\n' % (self._comment_symbol, '-'*30)
		)
		error_message = "Syntax Error from 'include' command"
		com_include = self._regexs
		source_includes = source
		for m2 in com_include[2].finditer(source):
			m2 = m2.group()
			included_file = com_include[21].search(m2)
			if included_file is not None:
				included_file = included_file.group()[1:-1].strip()
				included_file_value, variable_value = self.read_from_environ(included_file)
				if os.path.abspath(variable_value) == self._source_file_path:
					self.not_include_source(source, m2)
				included_value = '%s %s %s' % (
					after_replacement % os.path.split(variable_value)[-1],
					included_file_value,
					before_replacement,
				)
				source_includes = source_includes.replace(m2, included_value)
			else:
				raise IncludeError(error_message)
		for m1 in com_include[1].finditer(source_includes):
			m1 = m1.group()
			included_file = com_include[11].search(m1)
			if included_file is not None:
				included_file = included_file.group()[1:-1].strip()
				if os.path.abspath(included_file) == self._source_file_path:
					self.not_include_source(source, m1)
				included_file_value = self.read_included_file(included_file)
				included_value = '%s %s %s' % (
					after_replacement % os.path.split(included_file)[-1],
					included_file_value,
					before_replacement,
				)
				source_includes = source_includes.replace(m1, included_value)
			else:
				raise IncludeError(error_message)
		return source_includes


def get_special_includer(regexs, source_file_path, lang='batch'):
	"""Return special Includer object.
	
	In 'lang' parameter, you must specify the name of the language.
	For example - 'batch', python, 'cplusplus'
	
	It will just put the file extension and comment character,
	for that language.

	A 'lang' param value is not case sensitive.
	
	Args:
	    regexs: dict -- include command regexs.
	    source_file_path: str -- source file path
	    lang: str -- language name. For example 'batch' or 'python'
	
	Return:
	    value: Includer -- Includer object
	
	Raises:
	    TypeError -- If incorrectly params types
	    ValueError -- If incorrectly params

	"""
	
	error_message = "Param '%s' type is '%s', not '%s'"
	if not isinstance(lang, str):
		raise TypeError(
			error_message % (
				'lang', 'str',
				type(lang).__name__,)
		)
	lang = lang.lower()
	includer = Includer(regexs, source_file_path)
	if lang == 'batch':
		includer._comment_symbol = '::'
		includer._file_extensions = ('.bat', '.cmd', '.hbat', '.hb')
	elif lang == 'python':
		includer._comment_symbol = '#'
		includer._file_extensions = ('.py')
	elif lang == 'c':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.c', '.h')
	elif lang == 'cplusplus':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.cpp', '.cxx', '.cc', '.h', '.hpp')
	elif lang == 'java':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.java')
	elif lang == 'c#':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.cs')
	elif lang == 'go':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.go')
	elif lang == 'bash':
		includer._comment_symbol = '#'
		includer._file_extensions = ('.sh')
	elif lang == 'javascript':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.js')
	else:
		raise ValueError("This lang '%s' is unsupported" % lang)
	return includer


def include_all(source_file_path, lang='batch'):
	"""High-level and reliable function for the 'include' command.

	This function is based on the 'Includer' class,
	and the 'get_special_includer' function.

	It is recommended to use this function instead -
	of the 'Includer' class or the 'get_special_includer' function.

	This function:
	* Is at a higher level than the 'Includer' class.
	* More reliable than the 'Includer' class.
	* Simpler than the 'Includer' class.
	* More convenient than the 'Includer' class.
	* Supports recursive 'include'.
	* But less flexible than the 'Includer' class.
	----------------------------------------
	
	Args:
	    source_file_path: str -- Source file path
	
	    lang: str -- :
	        Program language name.
	        Example - 'batch', 'python', 'java', etc
	        This parameter affects language specific features.
	        For example, a comment character, or file extensions, etc.
	
	Return:
	    value: str -- Source file after includes.
	
	Raises:
	    TypeError -- If incorrect types.
	    FileNotFoundError -- If source file not found.
	    ValueError -- If problem in arguments.
	    ImportError -- If import module not found. Example:
	        module 'precommands.py' not found.
	    IncludeError -- If problem in include command.
	    IncludedSourceError -- If includes itself.
	    OSError -- If problem in operating system.
	----------------------------------------

	This function performs all the 'include' expressions -
	that are specified inside the file.

	The general syntax for the 'include' command is:
	:#include "Inclusion file path"

	Working with environment variables is also supported.
	On Windows, these are percent characters (%variable%),
	on Linux, these are dollar signs ($variable).

	You need to write 'include' statements inside files -
	before running this function.

	Example in Windows:
	:#include "somes\some.py"
	:#include "%somepy_path%"
	:#include "%somes_path%\some.py"

	Example in Linux:
	:#include "somes/some.py"
	:#include "$somepy_path"
	:#include "$somes_path/some.py"
	----------------------------------------
	
	############# -Examples- ###############
	----------------------------------------
	>>> # imports 'include_all' function.
	>>> from includer import include_all
	>>> 
	>>> # Opens source files.
	>>> source1 = open('src.bat')
	>>> source2 = open('src.py')
	>>> source3 = open('src.java')
	>>> # Reads source files and closes.
	>>> source_val1 = source1.read(); source1.close() 
	>>> source_val2 = source2.read(); source2.close()
	>>> source_val3 = source3.read(); source3.close()
	>>> # Calls 'include_all' function. Inclusions.
	>>> included1 = include_all(source_val1)
	>>> included2 = include_all(source_val2, 'python')
	>>> included3 = include_all(source_val3, 'java')
	>>> # Saves results.
	>>> target1 = open('nsrc.bat', 'w')
	>>> target1.write(included1); target1.close()
	>>> target2 = open('nsrc.py', 'w')
	>>> target2.write(included2); target2.close()
	>>> ...
	----------------------------------------

	"""
	
	if not isinstance(source_file_path, str):
		raise TypeError("Param 'source_file_path' must be 'str' type")
	if not os.path.isfile(source_file_path):
		raise FileNotFoundError("Source file not found")
	from .precommands import PreprocessorCommands
	preproc_commands = PreprocessorCommands()
	regexs = preproc_commands.get_com_include()
	includer_obj = get_special_includer(regexs, source_file_path, lang)
	source_file_value = '\n' + includer_obj.read(source_file_path) + '\n'
	start_include = includer_obj.start
	while True:
		included_source = start_include(source_file_value)
		if included_source != source_file_value:
			source_file_value = included_source
		else:
			break
	return included_source[1:-1]
"""Bpp utility prompts.

Hints for CLI or for syntax errors, etc.
Are here hints for different preprocessor commands.

"""

__all__ = [
	'get_include_prompt',
]


_includer_prompts = {
	-1: "The 'include' must be followed by a value",
	-2: "In quotes there must be a text",
	-3: "You cannot specify only one quotation mark",
	-4: "You have to close quotes on the sides",
	-5: "You have to close quotes on the sides",
	-6: "The path must be quoted in quotes",
}


def get_include_prompt(number):
	"""Returns some prompt for 'Include' command.

	Param 'number' is the regex number of -
	the 'include' command.
	
	Example:
	    -1, -2, 3, etc
	
	If number < 0 then error hint,
	If number > 0 then standart hint.

	This feature works best with error hints.

	If this function returns an empty string,
	it means he did not find such a hint.
	And if it returns some kind of string, then I found a hint.

	Args:
	    number: int -- Regular expression number
	
	Return:
	    value: str -- :
	        If result == '' then hint not found
	        If result is some string then is promt found
	
	Raises:
	    TypeError -- If incorrectly parameter types.
	
	"""
	
	if not isinstance(number, int):
		raise TypeError(
			"Param 'number' must be type 'int' not '%s'" % type(number).__name__
		)
	return _includer_prompts.get(number, "")
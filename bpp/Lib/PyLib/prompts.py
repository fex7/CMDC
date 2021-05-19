"""Bpp utility prompts.

Hints for CLI or for syntax errors, etc.
Are here hints for different preprocessor commands.

"""

__all__ = [
	'get_include_prompt',
]


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
	if number == -1:
		prompt = "The 'include' must be followed by a value"
	elif number == -2:
		prompt = "In quotes there must be a text"
	elif number == -3:
		prompt = "You cannot specify only one quotation mark"
	elif number == -4 or number == -5:
		prompt = "You have to close quotes on the sides"
	elif number == -6:
		prompt = "The path must be quoted in quotes"
	else:
		prompt = ""
	return prompt
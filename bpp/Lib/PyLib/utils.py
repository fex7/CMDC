"""Utilities"""

import os



def chdir_to_filedir(file_path):
	"""Changed directory to file directory.
	
	Args:
	    file_path: str -- file path
	
	Return:
	    value: str -- file dir name
	
	Raises:
	    FileNotFoundError -- if file not found.

	"""

	if not os.path.isfile(file_path):
		raise FileNotFoundError("File not found")
	file_dirname = os.path.dirname(file_path)
	os.chdir(file_dirname)
	return file_dirname


def get_temp_dir():
	"""Return Temp directory path."""
	
	if os.name == 'nt':
		tmp_dir = os.getenv('Temp', '.')
	elif os.name == 'posix':
		tmp_dir = os.getenv('TMPDIR', '.')
	else:
		tmp_dir = os.getenv('TMP', '.')
	return tmp_dir


__all__ = [
	'chdir_to_filedir',
	'get_temp_dir',
]
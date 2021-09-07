"""Data structures.

There are different data structures here.
It is recommended to simply create objects -
of these structures from this module.
But you can also define subclasses if needed.

"""

import copy

__all__ = [
	'frozendict',
]


def _immutable(instance, *args, **kwargs):
	"""Raises 'TypeError' because the object is immutables.
	
	This function must be called in methods of immutable classes -
	if this method changes an object.

	Args:
	    instance: Object -- some object
	    args: tuple -- some positional args
	    kwargs: dict -- some keyword args
	
	Raises:
	    TypeError -- Just raises

	"""

	errmsg = "'%s' object does not support this operation" % (
		type(instance).__name__
	)
	raise TypeError(errmsg)


class frozendict(dict):
	"""Immutable dict.

	frozendict() -> empty frozendict object
	frozendict(dict_object) -> frozendict object

	This class is an immutable dictionary.

	The 'frozendict' objects are hashed.
	Hence, you can use them as a key in a 'dict' object -
	or as an element in a 'set' object.

	It supports all dictionary methods that do not modify an object.
	But If you try to call for example the 'pop' method,
	a 'TypeError' will simply be raised.

	The constructor takes the same arguments as -
	the 'dict' constructor.

	Note. 'frozendict' is a subclass of 'dict'.

	| Unsupported 'dict' methods |
	* __setitem__     * setdefault
	* __delitem__     * popitem
	* update          * clear
	* pop
	------------------------------------

	#### Examples ####
	>>> # If calles 'hash(fd0, ..., fd4)' then returns hash
	>>> fd0 = frozendict()
	>>> fd1 = frozendict({1: 2, 2: 1})
	>>> fd2 = frozendict({'foo': 'bar', 1991: 'good year!'})
	>>> fd3 = frozendict(key1='val', key2='val')
	>>> fd4 = frozendict([('k1', 0), ('k2', 0)])
	>>>
	>>> # If called 'hash(fd5)' then raised TypeError
	>>> fd5 = frozendict({'k1': [1, 2, 3], 'k2': [3, 2, 1]}) 
	>>> fd6 = frozendict({[1, 2]: 12}) # is error
	>>>
	>>> # Common methods for Python 3 and 2:
	>>> fd7 = frozendict({1: 2, 'hi': 'bye'})
	>>> keys = fd7.keys()
	>>> values = fd7.values()
	>>> items = fd7.items()
	>>> hivalue = fd7.get('hi')
	>>> fd7copy = fd7.copy()

	"""

	__slots__ = ('_hash_cache',)

	def __init__(self, *args, **kwargs):
		"""Initialize self."""

		super(frozendict, self).__init__(*args, **kwargs)
		object.__setattr__(self, '_hash_cache', None)

	def __repr__(self):
		"""The '__repr__' for self."""

		repr_text = "frozendict(%s)" % (
			super(frozendict, self).__repr__()
		)
		return repr_text

	def __hash__(self):
		"""Returns a hash.

		If all values are hashable, then it returns a hash,
		otherwise raises a 'TypeError' exception.

		"""

		if self._hash_cache is not None:
			return self._hash_cache
		try:
			frozenset_obj = frozenset(self.items())

		except TypeError:
			hash_value = None
		else:
			hash_value = hash(frozenset_obj)
			object.__setattr__(self, '_hash_cache', hash_value)
		
		if hash_value is None:
			raise TypeError("Not all elements are hashable.")
		return hash_value
	
	def __copy__(self):
		"""Returns a copy of the object."""
		return self
		
	def __deepcopy__(self, memo=None):
		"""Performs a deep copying of an object."""

		try:
			# Checks hashable.
			hash(self)
			
		except TypeError:
			dict_object = copy.deepcopy(dict(self))
			return type(self)(dict_object)
		
		else:
			return type(self)(self)
	
	def __reduce__(self, *args):
		"""Implements support for 'pickle'."""

		pickle_value = (
			type(self),
			(dict(self),)
		)
		return pickle_value
	
	def copy(self):
		"""D.copy() -> a shallow copy of D."""
		return self.__copy__()
	
	@classmethod
	def fromkeys(cls, *args, **kwargs):
		"""Identical to the 'dict.fromkeys' method."""
		
		dict_object = dict.fromkeys(*args, **kwargs)
		return cls(dict_object)
	
	# Unsupported methods:
	def __setattr__(self, *args, **kwargs):
		"""Not supported."""
		errmsg = "'%s' object is read-only" % (
			type(self).__name__
		)
		raise AttributeError(errmsg)

	def __delattr__(self, *args, **kwargs):
		"""Not supported."""
		errmsg = "'%s' object is read-only" % (
			type(self).__name__
		)
		raise AttributeError(errmsg)

	def __setitem__(self, *args, **kwargs):
		"""Not supported."""
		errmsg = "'%s' object does not support item assignment" % (
			type(self).__name__
		)
		raise TypeError(errmsg)

	def __delitem__(self, *args, **kwargs):
		"""Not supported."""
		errmsg = "'%s' object doesn't support item deletion" % (
			type(self).__name__
		)
		raise TypeError(errmsg)

	def setdefault(self, *args, **kwargs):
		"""Not supported."""
		_immutable(self)

	def update(self, *args, **kwargs):
		"""Not supported."""
		_immutable(self)

	def pop(self, *args, **kwargs):
		"""Not supported."""
		_immutable(self)
		
	def clear(self, *args, **kwargs):
		"""Not supported."""
		_immutable(self)
	
	def popitem(self, *args, **kwargs):
		"""Not supported."""
		_immutable(self)
"""Data structures."""

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
	
	Rauses:
	    TypeError -- Just raises

	"""

	raise TypeError("'%s' object is immutable" % type(instance).__name__)


class frozendict(dict):
	"""Immutable dict.

	frozendict() -> empty frozendict object
	frozendict(dict_object) -> frozendict object

	This class is an immutable dictionary.

	It supports all dictionary methods that do not modify an object.
	But If you try to call for example the 'pop' method,
	a 'TypeError' will simply be raised.

	The constructor takes the same arguments as -
	the dictionary constructor.

	Unsupported 'dict' methods:
	* __setitem__
	* __delitem__
	* popitem
	* setdefault
	* update
	* pop
	* clear

	Examples:
	>>> # If calles 'hash(fd0, ..., fd4)' then returns hash
	>>> fd0 = frozendict()
	>>> fd1 = frozendict({1: 2, 2: 1})
	>>> fd2 = frozendict({'foo': 'bar', 1991: 'good year!'})
	>>> fd3 = frozendict(key1='val', key2='val')
	>>> fd4 = frozendict([('k1', 0), ('k2', 0)])
	>>> # If called 'hash(fd5)' then raised TypeError
	>>> fd5 = frozendict({'k1': [1, 2, 3], 'k2': [3, 2, 1]}) 
	>>> fd6 = frozendict({[1, 2]: 12}) # is error

	"""

	__slots__ = ('_hash_cache',)

	def __init__(self, *args, **kwargs):
		"""Initialize self."""

		super(type(self), self).__init__(*args, **kwargs)
		object.__setattr__(self, '_hash_cache', None)

	def __repr__(self):
		"""The '__repr__' for self."""

		repr_text = "frozendict(%s)" % (
			super(type(self), self).__repr__()
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
		
	def __deepcopy__(self, memo={}):
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
		"""FD.copy() -> a shallow copy of FD."""
		return self.__copy__()
	
	@classmethod
	def fromkeys(cls, *args, **kwargs):
		"""Identical to the 'dict.fromkeys' method."""
		
		dict_object = dict.fromkeys(*args, **kwargs)
		return cls(dict_object)
	
	# Unsupported methods.
	def __setattr__(self, *args, **kwargs):
		_immutable(self)
		
	def __delattr__(self, *args, **kwargs): _immutable(self)
	def __setitem__(self, *args, **kwargs): _immutable(self)
	def __delitem__(self, *args, **kwargs): _immutable(self)
	def setdefault(self, *args, **kwargs): _immutable(self)
	def popitem(self, *args, **kwargs): _immutable(self)
	def update(self, *args, **kwargs): _immutable(self)
	def clear(self, *args, **kwargs): _immutable(self)
	def pop(self, *args, **kwargs): _immutable(self)
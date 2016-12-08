# -*- coding: utf-8 -*-
"""RegExp

Make regular expression easy to use.
"""
import re
import os
import sys
import ctypes
import inspect
from functools import wraps
from collections import defaultdict
try:
    import __builtin__
except:
    import builtins as __builtin__

__version__ = '0.1.0'
__author__ = 'Frost Ming'
__license__ = 'MIT'

IS_PY3 = sys.version_info[0] > 2

# Monkey patch built in string types.
# Refer to https://github.com/clarete/forbiddenfruit
Py_ssize_t = \
    hasattr(ctypes.pythonapi, 'Py_InitModule4_64') \
    and ctypes.c_int64 or ctypes.c_int


class PyObject(ctypes.Structure):
    pass

PyObject._fields_ = [
    ('ob_refcnt', Py_ssize_t),
    ('ob_type', ctypes.POINTER(PyObject)),
]


class SlotsProxy(PyObject):
    _fields_ = [('dict', ctypes.POINTER(PyObject))]


def patchable_builtin(klass):
    # It's important to create variables here, we want those objects alive
    # within this whole scope.
    name = klass.__name__
    target = klass.__dict__

    # Hardcore introspection to find the `PyProxyDict` object that contains the
    # precious `dict` attribute.
    proxy_dict = SlotsProxy.from_address(id(target))
    namespace = {}

    # This is the way I found to `cast` this `proxy_dict.dict` into a python
    # object, cause the `from_address()` function returns the `py_object`
    # version
    ctypes.pythonapi.PyDict_SetItem(
        ctypes.py_object(namespace),
        ctypes.py_object(name),
        proxy_dict.dict,
    )
    return namespace[name]


@wraps(__builtin__.dir)
def __filtered_dir__(obj=None):
    name = hasattr(obj, '__name__') and obj.__name__ or obj.__class__.__name__
    if obj is None:
        # Return names from the local scope of the calling frame, taking into
        # account indirection added by __filtered_dir__
        calling_frame = inspect.currentframe().f_back
        return sorted(calling_frame.f_locals.keys())
    return sorted(set(__dir__(obj)).difference(__hidden_elements__[name]))

# Switching to the custom dir impl declared above
__hidden_elements__ = defaultdict(list)
__dir__ = dir
__builtin__.dir = __filtered_dir__


def curse(klass, attr, value, hide_from_dir=False):
    """Curse a built-in `klass` with `attr` set to `value`
    This function monkey-patches the built-in python object `attr` adding a new
    attribute to it. You can add any kind of argument to the `class`.
    It's possible to attach methods as class methods, just do the following:
      >>> def myclassmethod(cls):
      ...     return cls(1.5)
      >>> curse(float, "myclassmethod", classmethod(myclassmethod))
      >>> float.myclassmethod()
      1.5
    Methods will be automatically bound, so don't forget to add a self
    parameter to them, like this:
      >>> def hello(self):
      ...     return self * 2
      >>> curse(str, "hello", hello)
      >>> "yo".hello()
      "yoyo"
    """
    dikt = patchable_builtin(klass)

    old_value = dikt.get(attr, None)
    old_name = '_c_%s' % attr   # do not use .format here, it breaks py2.{5,6}

    if old_value:
        dikt[old_name] = old_value
        dikt[attr] = value

        try:
            dikt[attr].__name__ = old_value.__name__
        except (AttributeError, TypeError):  # py2.5 will raise `TypeError`
            pass
        try:
            dikt[attr].__qualname__ = old_value.__qualname__
        except AttributeError:
            pass
    else:
        dikt[attr] = value

    if hide_from_dir:
        __hidden_elements__[klass.__name__].append(attr)


def get_builtin_method(klass, name):
    dikt = patchable_builtin(klass)
    old_name = '_c_%s' % name
    return dikt.get(old_name, dikt[name])


class PatchClass(object):
    match = lambda self, pat, flags=0: re.match(pat, self, flags)
    match = staticmethod(match)
    search = lambda self, pat, flags=0: re.search(pat, self, flags)
    search = staticmethod(search)
    findall = lambda self, pat, flags=0: re.findall(pat, self, flags)
    findall = staticmethod(findall)
    finditer = lambda self, pat, flags=0: re.finditer(pat, self, flags)
    finditer = staticmethod(finditer)

    @staticmethod
    def replace(self, pat, new, count=None):
        if isinstance(pat, re._pattern_type):
            return pat.sub(new, self, count or 0)
        return get_builtin_method(self.__class__, 'replace')(
            self, pat, new, count or -1)

    @staticmethod
    def split(self, sep=None, maxsplit=None):
        if isinstance(sep, re._pattern_type):
            return sep.split(self, maxsplit or 0)
        return get_builtin_method(self.__class__, 'split')(
            self, sep, maxsplit or -1)

    @staticmethod
    def rsplit(self, sep=None, maxsplit=None):
        if isinstance(sep, re._pattern_type):
            maxsplit = maxsplit or 0
            if maxsplit > 0:
                pat, flags = sep.pattern, sep.flags
                pat = re.compile('(' + pat.strip('()') + ')', flags)
                rs = pat.split(self)
                if len(rs) > 2*maxsplit + 1:
                    rs[:-2*maxsplit] = [self[0:0].join(rs[:-2*maxsplit])]
                    rs[-2*maxsplit:] = rs[-2*maxsplit+1::2]
            else: rs = sep.split(self)
            return rs
        return get_builtin_method(self.__class__, 'rsplit')(
            self, sep, maxsplit or -1)

    @staticmethod
    def find(self, pat, start=0, end=None):
        if isinstance(pat, re._pattern_type):
            if end is None: end = len(self)
            res = pat.search(self, start, end)
            return res.start() if res else -1
        return get_builtin_method(self.__class__, 'find')(
            self, pat, start, end)

    @staticmethod
    def rfind(self, pat, start=0, end=None):
        if isinstance(pat, re._pattern_type):
            if end is None: end = len(self)
            try:
                return max(m.start() for m in pat.finditer(self, start, end))
            except ValueError:
                return -1
        return get_builtin_method(self.__class__, 'rfind')(
            self, pat, start, end)

    @staticmethod
    def count(self, pat, start=0, end=None):
        if end is None: end = len(self)
        if isinstance(pat, re._pattern_type):
            return len(pat.findall(self, start, end))
        return get_builtin_method(self.__class__, 'count')(
            self, pat, start, end)

    @staticmethod
    def partition(self, sep):
        if isinstance(sep, re._pattern_type):
            pat, flags = sep.pattern, sep.flags
            pat = re.compile('(' + pat.strip('()') + ')', flags)
            rs = pat.split(self, 1)
            rs.extend([self[0:0]] * (3-len(rs)))
            return tuple(rs)
        return get_builtin_method(self.__class__, 'partition')(self, sep)

    @staticmethod
    def rpartition(self, sep):
        if isinstance(sep, re._pattern_type):
            pat, flags = sep.pattern, sep.flags
            pat = re.compile('(' + pat.strip('()') + ')', flags)
            rs = pat.split(self)
            if len(rs) > 3:
                rs[:-2] = [self[0:0].join(rs[:-2])]
            rs = [self[0:0]] * (3-len(rs)) + rs
            return tuple(rs)
        return get_builtin_method(self.__class__, 'rpartition')(self, sep)

    @staticmethod
    def index(self, pat, start=0, end=None):
        if isinstance(pat, re._pattern_type):
            if end is None: end = len(self)
            try:
                return pat.search(self, start, end).start()
            except AttributeError:
                raise ValueError('substring not found')
        return get_builtin_method(self.__class__, 'index')(
            self, pat, start, end)

    @staticmethod
    def rindex(self, pat, start=0, end=None):
        if isinstance(pat, re._pattern_type):
            if end is None: end = len(self)
            try:
                return max(m.start() for m in pat.finditer(self, start, end))
            except ValueError:
                raise ValueError('substring not found')
        return get_builtin_method(self.__class__, 'rindex')(
            self, pat, start, end)

    @staticmethod
    def startswith(self, prefix, start=0, end=None):
        if end is None: end = len(self)
        if not isinstance(prefix, tuple):
            prefix = [prefix]
        for p in prefix:
            if isinstance(p, re._pattern_type):
                if p.match(self, start, end) is not None: return True
            elif get_builtin_method(self.__class__, 'startswith')(
                self, p, start, end):
                 return True
        return False

    @staticmethod
    def endswith(self, suffix, start=0, end=None):
        if end is None: end = len(self)
        if not isinstance(suffix, tuple):
            suffix = [suffix]
        for p in suffix:
            if isinstance(p, re._pattern_type):
                pat, flags = p.pattern, p.flags
                p = re.compile(pat.rstrip('$') + '$', flags)
                if p.search(self, start, end) is not None: return True
            elif get_builtin_method(self.__class__, 'endswith')(
                self, p, start, end):
                 return True
        return False

methods_to_patch = [
    'match', 'search', 'findall', 'finditer', 'replace', 'split', 'rsplit',
    'find', 'rfind', 'index', 'rindex', 'partition', 'rpartition', 'count',
    'startswith', 'endswith'
]


def patch_all():
    """Monkey patch regular expression methods to `str`."""
    to_patch = ['str'] if IS_PY3 else ['str', 'unicode']
    to_patch = [getattr(__builtin__, klass) for klass in to_patch]
    for klass in to_patch:
        for meth in methods_to_patch:
            curse(klass, meth, getattr(PatchClass, meth))

patch_all()
del patch_all, PatchClass

# coding=UTF-8

"""Provides utilities for simulating strongly-typed objects."""

from enum import Enum

__author__ = 'alen'


# TODO: completely shift from mapping to kwargs everywhere


class TypeCheck(object):

    """Performs type-checking as a descriptor decorator.

    Defeated its purpose 5 minutes later. Useful as a reminder if reverting
    back to decorator with no inputs.
    """

    def __init__(self, *types):
        self.types = types
        self.func = None

    def __call__(self, f):
        def _type_check(inst, *args, **kwargs):
            for k, t in enumerate(self.types):
                if isinstance(t, tuple):
                    k = t[0] - 1
                    t = t[1]
                if args[k] is None and inst._noneable:
                    continue
                elif not isinstance(args[k], getattr(inst, t)):
                    raise TypeError('Expected type {}, got type {}'.format(
                        getattr(inst, t).__name__, type(args[k]).__name__))
            return f(inst, *args, **kwargs)
        return _type_check

    def __get__(self, inst, type_=None):
        """Useful if params don't get passed to get right function context."""
        if inst is None or self.func is None:
            return self
        return self.__class__(self.func.__get__(inst, type_))


class _NoneType(object):

    """Special None-replacement object to avoid bad things."""

    def __nonzero__(self):
        return False

    def __bool__(self):
        self.__nonzero__()


_None = _NoneType()


class MetaTyped(type):
    """Get ready for this world of pain."""

    def __new__(mcs, name, bases, attribs):
        types = [a for a, p in attribs.items() if
                 isinstance(p, ImmutableType)]
        attribs['_types'] = types
        return type.__new__(mcs, name, bases, attribs)

    def __instancecheck__(self, other):
        self_template = self
        while self_template._generated:
            self_template = self_template.__base__

        other_template = type(other)
        try:
            while other_template._generated:
                other_template = other_template.__base__
        except:
            pass

        try:
            while self_template != other_template:
                other_template = other_template.__base__
            for t in other_template._types:
                if t in self._types:
                    try:
                        a = getattr(self, t)
                    except:
                        continue
                    if not issubclass(getattr(other, t), a):
                        # print ' ', t, 'failed as', getattr(other, t).__name__
                        raise Exception()
                    # print ' ', t, 'passed as', getattr(other, t).__name__
                else:
                    return False
        except:
            return False

        return True


class ImmutableType(object):

    def __init__(self, value=_None, silent=False):  # TODO: not use _None?
        if value is not _None:
            if not isinstance(value, type):
                raise TypeError('constructing error, type must be a type, got '
                                '{}'.format(value.__name__))
        self.value = value
        self.types = {}

    def __get__(self, instance, type=None):
        if self.value:
            return self.value
        try:
            return self.types[id(instance)]
        except KeyError:
            raise AttributeError('property not defined yet')

    def __set__(self, instance, value):
        if id(instance) in self.types or self.value:
            raise AttributeError('property already defined')
        else:
            if not isinstance(value, type):
                raise TypeError('value must be a type, got object of type {}'
                                .format(type(value).__name__))
            self.types[id(instance)] = value

    def __delete__(self, instance):
        if id(instance) not in self.types or self.value:
            raise AttributeError('property not defined yet')
        else:
            raise AttributeError('property cannot be removed')


class Typed(object):

    """A common ancestor to all typed objects."""

    __metaclass__ = MetaTyped
    _generated = False
    _data = None
    _type_dict = None
    _noneable = True

    @classmethod
    def types_keys(cls):
        return [t for t, v in cls.__dict__.items() if
                isinstance(v, ImmutableType)]

    @property
    def types(self):
        if self._type_dict:
            return self._type_dict
        else:
            self._type_dict = {k: getattr(self, k) for k in self.types_keys()}
            return self._type_dict

    @classmethod
    def is_acceptable(cls, inst):
        return False

    def __init__(self, *args, **kwargs):
        """Perform generic Typed object initialisation."""
        types = self.__class__.types_keys()
        if len(types) == 1 and len(args) == 1:
            # print 'args:', types[0], args[0]
            try:
                setattr(self, types[0], args[0])
            except:
                pass
        for a in types:
            # print 'kwargs:', types, kwargs
            try:
                getattr(self, a)
            except AttributeError:
                setattr(self, a, kwargs.get(a))

    def __str__(self):
        s = ''
        for t in self._types:
            try:
                n = getattr(self, t).__name__
            except AttributeError:
                n = '?'
            s += ',{}:{}'.format(t, n)

        s = s[1:] if len(s) else s

        if self._data is not None:
            return '({}){}'.format(s, repr(self._data))
        else:
            return s

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, type(self)) and isinstance(self, type(other))\
               and (self._data is None or self._data == other._data)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Typed):
            other = other._data
        return self._data < other

    def __le__(self, other):
        if isinstance(other, Typed):
            other = other._data
        return self._data <= other

    def __gt__(self, other):
        if isinstance(other, Typed):
            other = other._data
        return self._data > other

    def __ge__(self, other):
        if isinstance(other, Typed):
            other = other._data
        return self._data >= other

    def __len__(self):
        try:
            return len(self._data)
        except TypeError:
            raise TypeError('object has no len()')

    def __contains__(self, item):
        try:
            return item in self._data
        except TypeError:
            raise TypeError('object is not iterable')

    def __delitem__(self, key):
        try:
            self._data.__delitem__(key)
        except TypeError:
            raise TypeError('cannot delete items in this object')

    def __getitem__(self, key):
        try:
            return self._data[key]
        except TypeError:
            raise TypeError('cannot get items in this object')
        except KeyError as e:
            raise KeyError(str(e))

    def __iter__(self):
        try:
            for v in self._data:
                yield v
        except TypeError:
            raise TypeError('{} object is not iterable.'.format(
                self.__class__.__name__))

    # __hash__ = None

    def untype(self):
        if isinstance(self._data, list):
            untyped = list(self._data)
            for k, v in enumerate(untyped):
                try:
                    untyped[k] = v.untype()
                except AttributeError:
                    pass
            return untyped
        elif isinstance(self._data, dict):
            untyped = self._data.copy()
            for k, v in untyped.items():
                try:
                    untyped[k] = v.untype()
                except AttributeError:
                    pass
            return untyped
        return self._data


def factory(cls, mapping=None, name=None, **kwargs):
    types = cls.types_keys()

    if len(types) == 1 and isinstance(mapping, type):
        mapping = {types[0]: mapping}

    if mapping is None:
        mapping = kwargs

    if any([not isinstance(v, type) for _, v in mapping.items()]):
        raise TypeError('mapped types must be of type type')

    if not name:
        name = '{}{}'.format(cls.__name__,
            ''.join([v.__name__.capitalize() for _, v in mapping.items()]))

    attribs = cls.__dict__.copy()
    attribs['_generated'] = True
    for k in types:
        try:
            getattr(cls, k)
        except:
            try:
                v = mapping.pop(k)
                try:
                    check = getattr(cls, '_{}_check'.format(k)).__func__
                    if not check(v):
                        raise TypeError('suitability check failed for typed '
                                        'attrib {} with value {}'
                                        .format(k, v.__name__))
                except AttributeError:
                    pass
                attribs[k] = ImmutableType(v)
            except KeyError:
                raise TypeError('missing type mapping: {}'.format(k))
    if len(mapping):
        raise TypeError('type mapping too big: {}'.format(mapping))

    return type(name, (cls,), attribs)


class Map(Typed):  # TODO: setdefault, cmp/lt/gt/etc.

    """A not-deriving friendly typed dict implementation."""

    key_type = ImmutableType()
    item_type = ImmutableType()
    _key_type_check = lambda k: k.__hash__ is not None

    @classmethod
    def is_acceptable(cls, inst):
        try:
            for k, v in inst.items():
                if issubclass(cls.key_type, Typed):
                    if not isinstance(k, cls.key_type) and \
                            not cls.key_type.is_acceptable(k):
                        return False
                elif issubclass(cls.key_type, Enum):
                    if not isinstance(k, cls.key_type) and \
                            not hasattr(cls.key_type, k):
                        return False
                elif not isinstance(k, cls.key_type):
                    return False

                if v is None and cls._noneable:
                    continue
                elif issubclass(cls.item_type, Typed):
                    if not isinstance(v, cls.item_type) and \
                            not cls.item_type.is_acceptable(v):
                        return False
                elif issubclass(cls.item_type, Enum):
                    if not isinstance(v, cls.item_type) and \
                            not hasattr(cls.item_type, v):
                        return False
                elif not isinstance(v, cls.item_type):
                    return False
        except:
            return False
        return True

    def __init__(self, dict_=None, *args, **kwargs):
        super(Map, self).__init__(self, *args, **kwargs)

        if not self._generated and not self._key_type_check\
                .__func__(kwargs.get('key_type')):
            raise TypeError('key_type must be hashable')

        self._data = {}

        if dict_ is not None:
            self.update(dict_)

        # TODO: better way to do this, should probably move to MetaTyped soon
        self.__class__ = factory(Map, {'key_type': self.key_type,
                                       'item_type': self.item_type})

    def __setitem__(self, key, item):
        if isinstance(key, self.key_type):
            if isinstance(item, self.item_type) \
                    or (item is None and self._noneable):
                self._data[key] = item
        else:
            raise TypeError('Expected ({},{}), got ({},{})'.format(
                self.key_type.__name__, self.item_type.__name__,
                type(key).__name__, type(item).__name__))

    def clear(self):
        self._data.clear()

    def copy(self):
        return Map(self._data.copy(), self.key_type, self.item_type)

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def iteritems(self):
        return self._data.iteritems()

    def iterkeys(self):
        return self._data.iterkeys()

    def itervalues(self):
        return self._data.itervalues()

    def values(self):
        return self._data.values()

    def has_key(self, key):
        return key in self._data

    # TODO: prevent from partially failing
    def update(self, other=None):
        if other is None:
            return
        if not hasattr(other, 'items'):
            raise TypeError('cannot iterate over {}'.format(other))
        for k, v in other.items():
            self[k] = v

    def get(self, key, fail_obj=None):
        if key in self:
            return self[key]
        else:
            return fail_obj

    def pop(self, key, *args):
        return self._data.pop(key, *args)

    def popitem(self):
        return self._data.popitem()

    @classmethod
    def fromkeys(cls, iterable, value):
        d = cls()
        for key in iterable:
            d[key] = value
        return d


class Array(Typed):  # TODO: mul, add

    """A typed list implementation."""

    item_type = ImmutableType()
    _item_type_check = lambda i: hasattr(i, '__cmp__') or hasattr(i, '__lt__')\
        or hasattr(i, '__gt__')

    @classmethod
    def is_acceptable(cls, inst):
        try:
            for v in inst:
                # print '  ->', type(v), '<=', cls.item_type
                if v is None and cls._noneable:
                    continue
                elif issubclass(cls.item_type, Typed):
                    if not isinstance(v, cls.item_type) and \
                            not cls.item_type.is_acceptable(v):
                        return False
                elif issubclass(cls.item_type, Enum):
                    if not isinstance(v, cls.item_type) and \
                            not hasattr(cls.item_type, v):
                        return False
                elif not isinstance(v, cls.item_type):
                    return False
                # print '  -> pass'
        except:
            return False
        return True

    def __init__(self, list_=None, *args, **kwargs):
        super(Array, self).__init__(self, *args, **kwargs)

        if not self._generated and not self._item_type_check\
                .__func__(kwargs.get('item_type')):
            raise TypeError('item_type must be sortable')

        self._data = []

        if list_ is not None:
            self.extend(list_)

        # TODO: better way to do this, should probably move to MetaTyped soon
        self.__class__ = factory(Array, {'item_type': self.item_type})

    def extend(self, other):
        if hasattr(other, '__iter__'):
            other = list(other)
            error = TypeError('Expected all of type {}, got types {}'
                    ,format(set([type(item) for item in other])))

            for k, v in enumerate(other):
                if v is None and self.item_type._noneable:
                    continue
                elif issubclass(self.item_type, (Typed, Enum)):
                    if not isinstance(v, self.item_type):
                        if self.item_type.is_acceptable(v):
                            # print 'Instantiating', self.item_type, v
                            other[k] = self.item_type(v)
                        else:
                            raise error
                elif not isinstance(v, self.item_type):
                    raise error
        else:
            raise TypeError('type {} is not iterable'.format(
                type(other).__name__))

        for i in other:
            self.append(i)

    @TypeCheck((2, 'item_type'))
    def __setitem__(self, key, item):
        self._data[key] = item

    @TypeCheck('item_type')
    def append(self, item):
        self._data.append(item)

    def index(self, index):
        return self._data[index]

    @TypeCheck((2, 'item_type'))
    def insert(self, index, item):
        self._data.insert(index, item)

    def pop(self):
        self._data.pop()

    @TypeCheck('item_type')
    def remove(self, item):
        self._data.remove(item)

    @TypeCheck('item_type')
    def count(self, item):
        self._data.count(item)

    def reverse(self):
        self._data.reverse()

    def sort(self):
        self._data.sort()

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __imul__(self, other):
        self._data *= other
        return self


# SIMPLE TESTS

class Dummy(Typed):
    pass


class Map2(Typed):
    """Unfriendly :(."""

    key_type = ImmutableType()
    item_type = ImmutableType()

ta = Map({1: 3, 2: 2, 3: 1}, key_type=int, item_type=int)
t1 = factory(Map, {'key_type': int, 'item_type': int})
tb = t1({1: 3, 2: 2, 3: 1})
tc = t1({1: 3, 2: 2})
td = Map2(key_type=int, item_type=int)

tx = factory(Map, {'key_type': object, 'item_type': int})
ty = Map({1: 3, 2: 2, 3: 1}, key_type=object, item_type=int)
tz = tx({1: 3, 2: 2, 3: 1})

tn = factory(Map, {'key_type': int, 'item_type': t1})
tm = factory(Map, {'key_type': object, 'item_type': t1})
to = factory(Map, {'key_type': int, 'item_type': object})
ti = tn()
tj = Map({10: ta}, key_type=int, item_type=t1)
tk = tm(tj)
tl = to({10: ta})
tg = to({1: 3, 2: 2, 3: 1})
th = Map({1: 3, 2: 2, 3: 1}, key_type=object, item_type=int)
tr = Map({1: 3, 2: 2, 3: 1}, key_type=int, item_type=object)

try:
    tt = tn(to)
    assert False
except:
    pass

assert isinstance(ta, Map)
assert isinstance(tb, Map)
assert isinstance(tc, Map)
assert isinstance(ta, t1)
assert isinstance(tb, t1)
assert isinstance(tc, t1)
assert not isinstance(td, t1)
assert isinstance(Map(key_type=int, item_type=int), t1)
assert isinstance(td, Typed)
assert not isinstance(object(), Typed)
assert not isinstance(Typed(), t1)
assert not isinstance(Typed(), Dummy)
assert ta == tb
assert not ta != tb
assert not ta == tc
assert tc != tb
assert ta != tk
assert ta != tg
assert ta != th
assert tb != tg
assert tb != th
assert tg != th
assert tr == tg
assert type(tr) != type(tg)
assert isinstance(tr, type(tg))
assert isinstance(tg, type(tr))
assert isinstance(ta, type(tg))
assert not isinstance(tg, type(ta))  # TODO: further checking of post-init type

assert isinstance(ty, tx)
assert isinstance(ty, Map)
assert isinstance(ty, Typed)
assert isinstance(tz, tx)
assert isinstance(tz, Map)
assert isinstance(tz, Typed)
assert isinstance(ta, tx)
assert isinstance(tb, tx)
assert not isinstance(td, tx)
assert not isinstance(tz, t1)
assert not isinstance(ty, t1)

assert isinstance(ti, tn)
assert isinstance(ti, tm)
assert isinstance(ti, to)
assert isinstance(tk, tm)
assert not isinstance(tk, tn)
assert not isinstance(tk, to)
assert isinstance(tj, tn)
assert isinstance(tk, tm)
assert not isinstance(tk, to)

assert ta.is_acceptable({1:1, 2:2, 3:3})
assert not ta.is_acceptable({1:1, 2: "alen", 3:3})
assert t1.is_acceptable({1:1, 2:2, 3:3})
assert not t1.is_acceptable({1:1, 2: "alen", 3:3})
assert not tn.is_acceptable({1: object()})
assert tn.is_acceptable({1: ta})

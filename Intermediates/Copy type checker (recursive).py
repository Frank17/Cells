from collections.abc import MutableSequence, MutableSet, MutableMapping, Container
from copy import deepcopy


class NoMutableElementFoundError(Exception): pass


def is_mutable(obj):
    return isinstance(obj, (MutableSequence, MutableSet, MutableMapping))


def is_container(obj):
    return isinstance(obj, Container)


def get_type(i, j):
    return 'shallow copy' if i is j else 'deep copy'


class Checker:
    def __init__(self, iter1, iter2):
        assert iter1 == iter2, 'Two iterables should have the same value'
        self._iter1 = iter1
        self._iter2 = iter2
        self.iter = deepcopy(iter1)
        self.stop_at = None
        self.has_mutable = False

    def check_copy(self, recursive=False):
        if self.iter1 is self.iter2:
            return 'assignment'
        elif isinstance(self._iter1, dict):
            return self._recursive(self._iter1.values(),
                                   self._iter2.values(), recursive)
        return self._recursive(self._iter1, self._iter2, recursive)

    def _recursive(self, iter1, iter2, recursive):
        if recursive:
            for i, j in zip(iter1, iter2):
                if is_mutable(i):
                    self.has_mutable = True
                    self.stop_at = i
                    iter1, iter2 = i, j
                    break
                if is_container(i):
                    self._iter1, self._iter2 = i, j
                    return self.check_copy(True)
        return self._get_type(iter1, iter2)

    def _get_type(self, iter1, iter2):
        if self.has_mutable:
            return get_type(iter1, iter2)
        for i, j in zip(iter1, iter2):
            if is_mutable(i):
                self.stop_at = i
                return get_type(i, j)
        raise NoMutableElementFoundError

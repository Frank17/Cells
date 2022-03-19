from collections.abc import MutableSequence, MutableSet, MutableMapping, Container


class NoMutableElementFoundError(Exception): pass


def is_mutable(obj):
    return isinstance(obj, (MutableSequence, MutableSet, MutableMapping))


def is_container(obj):
    return isinstance(obj, Container)


class Checker:
    def __init__(self, iter1, iter2):
        assert iter1 == iter2, 'Two iterables should have the same value'
        self.iter1 = iter1
        self.iter2 = iter2
        self.is_nested = False

    def check_copy(self, recursive=False):
        if self.iter1 is self.iter2:
            return 'assignment'
        elif isinstance(self.iter1, dict):
            return self._recursive(self.iter1.values(),
                                   self.iter2.values(), recursive)
        return self._recursive(self.iter1, self.iter2, recursive)

    def _recursive(self, iter1, iter2, recursive):
        if recursive:
            for i, j in zip(iter1, iter2):
                if is_container(i):
                    self.is_nested = True
                    self.iter1, self.iter2 = i, j
                    self.check_copy(True)
        return self._get_type(self.iter1, self.iter2)

    def _get_type(self, iter1, iter2):
        if self.is_nested and is_mutable(iter1):
            return 'shallow copy' if iter1 is iter2 else 'deep copy'
        for i, j in zip(iter1, iter2):
            if is_mutable(i):
                return 'shallow copy' if i is j else 'deep copy'
        raise NoMutableElementFoundError

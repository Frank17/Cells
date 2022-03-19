from collections.abc import MutableSequence, MutableSet, MutableMapping


class NoMutableElementFoundError(Exception): pass


class Checker:
    def __init__(self, iter1, iter2):
        assert iter1 == iter2, 'Two iterables should have the same value'
        assert iter1, 'Iterables cannot be empty'
        self.iter1 = iter1
        self.iter2 = iter2
    
    def check_copy(self):
        if self.iter1 is self.iter2:
            return 'assignment'
        elif isinstance(self.iter1, dict):
            return self._get_type(self.iter1.values(), self.iter2.values())
        return self._get_type(self.iter1, self.iter2)
    
    def _is_mutable(self, obj):
        return isinstance(obj, (MutableSequence, MutableSet, MutableMapping))
    
    def _get_type(self, iter1, iter2):
        for i, j in zip(iter1, iter2):
            if self._is_mutable(i):
                return 'shallow copy' if i is j else 'deep copy'
        raise NoMutableElementFoundError
     
    
def main():
    iter1 = [1, 2, 3]
    iter2 = iter1
    checker = Checker(iter1, iter2)
    print(checker.check_copy())
    
    
if __name__ == '__main__':
    main()

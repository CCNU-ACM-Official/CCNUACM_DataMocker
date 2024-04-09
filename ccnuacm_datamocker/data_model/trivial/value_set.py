from collections.abc import Iterable

from ccnuacm_datamocker.data_model.base.data_model import DataModel
from ccnuacm_datamocker.common import context

__all__ = [
    "ConstValue",
    "ValueSet",
    "LowercaseCharSet",
    "UppercaseCharSet",
    "AlphabetCharSet",
    "DigitCharSet",
    "BinaryCharSet",
]
__author__ = "JixiangXiong"


class ValueSet(DataModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        accepted_types = (int, float, str, ConstValue)
        for index, x in enumerate(args):
            if not isinstance(x, accepted_types):
                raise ValueError(f"All elements in `ValueSet` must be primitive or ConstValue, but get `{repr(x)}` of "
                                 f"type "
                                 f"`{type(x)}` in the {index}-th of args.")
        self._arr = sorted(set(str(x) for x in args))
        self._size = len(self._arr)

    def __str__(self):
        if self._size == 0:
            return ""
        return str(self._arr[context().random.randint(self._size)])

    def __len__(self):
        return self._size

    def __add__(self, rhs):
        if not isinstance(rhs, ValueSet):
            if not isinstance(rhs, Iterable):
                raise ValueError(f"Cannot add `ValueSet` with `{rhs.__class__.__name__}`.")
            rhs = ValueSet(*self._arr, *rhs)
        return ValueSet(*self._arr, *rhs._arr)

    def __radd__(self, lhs):
        return lhs.__add__(self)


class ConstValue(ValueSet):
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise ValueError("Only one argument is allowed for `ConstValue`.")
        if not args:
            args = [""]
        super().__init__(*args, **kwargs)


class LowercaseCharSet(ValueSet):
    def __init__(self, **kwargs):
        charset = 'abcdefghijklmnopqrstuvwxyz'
        super().__init__(*charset, **kwargs)


class UppercaseCharSet(ValueSet):
    def __init__(self, **kwargs):
        charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        super().__init__(*charset, **kwargs)


class DigitCharSet(ValueSet):
    def __init__(self, **kwargs):
        charset = '0123456789'
        super().__init__(*charset, **kwargs)


class AlphabetCharSet(ValueSet):
    def __init__(self, **kwargs):
        charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        super().__init__(*charset, **kwargs)


class BinaryCharSet(ValueSet):
    def __init__(self, **kwargs):
        charset = '01'
        super().__init__(*charset, **kwargs)

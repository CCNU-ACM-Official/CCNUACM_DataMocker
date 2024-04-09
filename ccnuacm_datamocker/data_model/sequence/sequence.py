from ccnuacm_datamocker.data_model.base.data_model import DataModel
from ccnuacm_datamocker.data_model.trivial.value_set import ConstValue


class Sequence(DataModel):
    def __init__(self, *args, **kwargs):
        length = kwargs.pop("length", None)
        sep = kwargs.pop("sep", " ")
        super().__init__(*args, **kwargs)

        if length is not None:
            if length < 0:
                raise ValueError("Length must be non-negative.")
            if len(args) > 1:
                raise ValueError("Only one argument is allowed for `Sequence`, when length is specified.")
            self._arr = [args[0] if args else ConstValue("")] * length
        else:
            self._arr = list(args)
        self._sep = sep

    def __str__(self):
        return self._sep.join(str(x) for x in self._arr)

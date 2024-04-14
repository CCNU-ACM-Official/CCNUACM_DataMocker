from ccnuacm_datamocker.data_model.base.data_model import DataModel

__all__ = ["Sequence", "RawSequence"]
__author__ = "JixiangXiong"


class Sequence(DataModel):
    def __init__(self, *args, **kwargs):
        sep = kwargs.pop("sep", "\n")
        h_sep = kwargs.pop("h_sep", "\n")
        show_length = kwargs.pop("show_length", False)
        super().__init__(*args, **kwargs)

        self._arr = list(args)
        self._sep = sep
        self._show_length = show_length if show_length is not None else False
        self._h_sep = h_sep

    def __str__(self):
        result = ""
        if self._show_length:
            result = f"{len(self._arr)}{self._h_sep}"
        result += self._sep.join(str(x) for x in self._arr)
        return result

    def brief(self):
        length = len(self._arr)
        result = ""
        if self._show_length:
            result = f"{length}{self._h_sep}"
        if self._sep == "":
            if length > 20:
                return (
                    result
                    + self._sep.join(x.brief() for x in self._arr[:20])
                    + self._sep
                    + "..."
                )
            return result + self._sep.join(x.brief() for x in self._arr)
        if length == 0:
            return result
        if length > 5:
            return (
                result
                + self._sep.join(x.brief() for x in self._arr[:5])
                + self._sep
                + "..."
            )
        return result + self._sep.join(x.brief() for x in self._arr)


class RawSequence(Sequence):
    def __init__(self, *args):
        super().__init__(*args)

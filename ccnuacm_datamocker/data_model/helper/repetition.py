from ccnuacm_datamocker.data_model.base.data_model import DataModel
from ccnuacm_datamocker.data_model.trivial.value_set import ConstValue

__all__ = ["Repetition"]
__author__ = "JixiangXiong"


class Repetition(DataModel):
    def __init__(self, model, **kwargs):
        times = kwargs.pop("times", None)
        sep = kwargs.pop("sep", " ")
        show_times = kwargs.pop("show_times", False)
        h_sep = kwargs.pop("h_sep", "\n")
        super().__init__(model, **kwargs)

        if times is None:
            raise ValueError("Repetition must have `times` specified.")

        from ..trivial.random_dist import RandomInt

        if not isinstance(times, RandomInt | int):
            raise ValueError("Repetition must have `times` specified as an integer.")

        self._times = times
        self._model = model
        self._sep = sep
        self._show_times = show_times if show_times is not None else False
        self._h_sep = h_sep

    def __str__(self):
        result = ""
        length = (
            int(self._times.__str__())
            if isinstance(self._times, DataModel)
            else self._times
        )
        if self._show_times:
            result = f"{length}{self._h_sep}"
        result += self._sep.join(str(self._model) for _ in range(length))
        return result

    def brief(self):
        length = (
            int(self._times.__str__())
            if isinstance(self._times, DataModel)
            else self._times
        )
        result = ""
        if self._show_times:
            result = f"{length}{self._h_sep}"
        if length == 0:
            return result
        if self._sep == "":
            if length > 20:
                return (
                    result
                    + self._sep.join(self._model.brief() for _ in range(20))
                    + self._sep
                    + "..."
                )
            return result + self._sep.join(self._model.brief() for _ in range(length))
        if length > 5:
            return (
                result
                + self._sep.join(self._model.brief() for _ in range(5))
                + self._sep
                + "..."
            )
        return result + self._sep.join(self._model.brief() for _ in range(length))

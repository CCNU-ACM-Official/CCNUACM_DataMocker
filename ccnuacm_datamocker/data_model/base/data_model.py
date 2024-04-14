from ccnuacm_datamocker.common import context
import pprint
import copy

__all__ = ["DataModel"]
__author__ = "JixiangXiong"


class DataModel:
    _alias_cnt = 0

    def __init__(self, *args, **kwargs):
        model_type = self.__class__.__name__

        alias = kwargs.pop("alias", None)
        if alias is None:
            self.__class__._alias_cnt += 1
            alias = f"{model_type}#{self._alias_cnt}"

        context().logger.debug(
            f"Initializing model `{model_type}` named `{alias}` with args: {kwargs}..."
        )

        self._model_type = model_type
        self._alias = alias

        accepted_types = (int, float, str, DataModel, list, tuple)
        if not all(isinstance(x, accepted_types) for x in args):
            raise ValueError(
                f"All elements in `DataModel` must be DataModel or primitive types, but get `{repr(args)}`."
            )

        if kwargs:
            msg = f"Invalid arguments for model `{self.__class__.__name__}`:\n{kwargs}"
            # 合法的参数应当都被剔除了，现在 kwargs 中所有的元素都是不合法的参数
            raise ValueError(msg)
        context().logger.debug(
            f"Successfully init model `{model_type}` named `{alias}`, vars: {vars(self)}"
        )

    def __repr__(self) -> str:
        return f"<{self._model_type}:{self._alias}>@\n{pprint.pformat(vars(self), width=2)}\nbrief:\n{self.brief()}"

    def __str__(self) -> str:
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            for key, value in vars(self).items():
                if value != getattr(other, key):
                    return False
            return True
        return False

    def __hash__(self):
        member_values = tuple(vars(self).values())
        return hash(member_values)

    def run(self):
        return self.__str__()

    def repeat(
        self,
        *,
        times: int = None,
        show_times: bool = None,
        sep=" ",
        h_sep="\n",
    ):
        from ..helper.repetition import Repetition

        if times is None:
            raise ValueError("Repetition must have `times` specified.")
        if show_times is None:
            show_times = False
        return Repetition(
            copy.deepcopy(self),
            times=times,
            show_times=show_times,
            sep=sep,
            h_sep=h_sep,
        )

    def brief(self):
        raise NotImplementedError()

    def show(self):
        print(self.brief())

    def __add__(self, rhs):
        from ..helper.sequence import RawSequence

        return RawSequence(self, rhs)

    def __radd__(self, lhs):
        return lhs.__add__(self)

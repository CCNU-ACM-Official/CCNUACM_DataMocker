from ccnuacm_datamocker.common import context
import pprint

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

        accepted_types = (int, float, str, DataModel)
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
        return (
            f"<{self._model_type}:{self._alias}>@\n{pprint.pformat(vars(self), width=2)}"
        )

    def __str__(self) -> str:
        raise NotImplementedError

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

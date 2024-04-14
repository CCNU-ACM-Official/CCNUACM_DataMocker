from ccnuacm_datamocker.data_model.base.data_model import DataModel
from ccnuacm_datamocker.common import context

__all__ = ["RandomInt", "RandomFloat"]
__author__ = ["JixiangXiong"]


class RandomInt(DataModel):
    def __init__(self, low=0, high=1_000_000_000_000_000_000, **kwargs):
        """
        :param low: The lower bound of the random integer.
        :param high: The upper bound of the random integer.
        description:
        This class is used to generate a random integer between [low, high).
        default:
        low = 0, high = 1_000_000_000_000_000_000
        """
        self._low = low
        self._high = high
        super().__init__(**kwargs)

    def __str__(self):
        return str(context().random.randint(self._low, self._high))

    def brief(self):
        return self.__str__()


class RandomFloat(DataModel):
    def __init__(self, low=0, high=1_000_000_000_000_000_000, **kwargs):
        """
        :param low: The lower bound of the random integer.
        :param high: The upper bound of the random integer.
        description:
        This class is used to generate a random integer between [low, high).
        default:
        low = 0, high = 1_000_000_000_000_000_000
        """
        self._low = low
        self._high = high
        self._precision = kwargs.pop("precision", 2)
        super().__init__(**kwargs)

    def __str__(self):
        return (
            f"{context().random.randfloat(self._low, self._high):.{self._precision}f}"
        )

    def brief(self):
        return self.__str__()
